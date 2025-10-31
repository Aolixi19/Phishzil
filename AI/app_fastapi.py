# app_fastapi.py
import os
import threading
import logging
from typing import List, Dict, Tuple, Any, Optional

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import OrderedDict

# ---------------- Configuration (override with env vars) ----------------
MODEL_ID_DEFAULT = os.getenv("MODEL_ID", "Gamortsey/bert-finetuned-phishing")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "512"))
CACHE_MAX = int(os.getenv("CACHE_MAX", "1000"))
PORT = int(os.getenv("PORT", "8000"))
# comma-separated origins or "*" (default)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
# Preferred cache dir (will be used only if writable). We prioritize HF_HOME env.
DEFAULT_CACHE_DIR = os.getenv("HF_CACHE_DIR") or os.getenv("TRANSFORMERS_CACHE") or "/app/.cache"
# Set number of workers in Docker/gunicorn via env var "WORKERS"
WORKERS = int(os.getenv("WORKERS", "2"))

# ---------------- Logging ----------------
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("phishing-api")

# ---------------- LRU cache implementation ----------------
class LRUCache:
    def __init__(self, maxsize: int = 256):
        self.maxsize = maxsize
        self.lock = threading.Lock()
        self.cache = OrderedDict()

    def get(self, key: str):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            return None

    def set(self, key: str, value: Any):
        with self.lock:
            self.cache[key] = value
            self.cache.move_to_end(key)
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)

    def clear(self):
        with self.lock:
            self.cache.clear()

# global prediction cache
PRED_CACHE = LRUCache(CACHE_MAX)

# ---------------- Model singletons ----------------
_tokenizer = None
_model = None
_device = None
_model_lock = threading.Lock()

# ---------------- Utilities ----------------
def _prepare_text(text: Any) -> str:
    if isinstance(text, list):
        return "\n".join([t.strip() for t in text if t is not None])
    return (text or "").strip()

def _choose_and_prepare_cache_dir(preferred: Optional[str] = None) -> str:
    """
    Choose a writable cache dir in a safe way, set HF_HOME, and clear deprecated envs.
    Preference order:
      1) existing HF_HOME env var
      2) provided preferred argument
      3) /tmp/hf_cache
      4) /tmp
    We DO NOT attempt to chmod directories (some hosts disallow it).
    """
    candidates = []
    # Respect explicit HF_HOME if set
    if os.environ.get("HF_HOME"):
        candidates.append(os.environ.get("HF_HOME"))
    # Preferred (from envs or config)
    if preferred:
        candidates.append(preferred)
    # Fallback writable locations
    candidates.extend(["/tmp/hf_cache", "/tmp"])

    for d in candidates:
        try:
            os.makedirs(d, exist_ok=True)
            # set HF_HOME so transformers uses this directory
            os.environ["HF_HOME"] = d
            # clear deprecated/ambiguous envs to avoid warnings
            os.environ.pop("TRANSFORMERS_CACHE", None)
            os.environ.pop("HF_CACHE_DIR", None)
            logger.info("Using HF cache dir: %s", d)
            return d
        except Exception as e:
            logger.warning("Could not prepare cache dir %s: %s", d, e)

    # Last-resort fallback
    os.environ["HF_HOME"] = "/tmp"
    logger.warning("Falling back to /tmp for HF cache")
    return "/tmp"

# ---------------- Model loading ----------------
def load_model(model_id: str = MODEL_ID_DEFAULT, cache_dir: Optional[str] = None):
    """
    Load (or reuse) the tokenizer and model. Uses a safe cache directory selection
    and passes cache_dir to transformers for explicitness.
    """
    global _tokenizer, _model, _device
    with _model_lock:
        if _model is not None and getattr(_model, "_hf_id", None) == model_id:
            return _tokenizer, _model, _device

        chosen_cache = _choose_and_prepare_cache_dir(cache_dir or DEFAULT_CACHE_DIR)

        use_auth = bool(os.getenv("HF_TOKEN"))
        auth_token = os.getenv("HF_TOKEN") if use_auth else None

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info("Loading model '%s' to device %s (cache_dir=%s)...", model_id, device, chosen_cache)
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                cache_dir=chosen_cache,
                use_auth_token=auth_token,
                trust_remote_code=True,
            )
            model = AutoModelForSequenceClassification.from_pretrained(
                model_id,
                cache_dir=chosen_cache,
                use_auth_token=auth_token,
                trust_remote_code=True,
            )
        except Exception as e:
            logger.exception("Model download/load failed: %s", e)
            raise

        model.to(device)
        model.eval()
        model._hf_id = model_id

        _tokenizer = tokenizer
        _model = model
        _device = device

        logger.info("Model '%s' loaded.", model_id)
        return tokenizer, model, device

# ---------------- Prediction helpers ----------------
def predict_raw(text: str, model_id: str = MODEL_ID_DEFAULT) -> Tuple[Dict[str, float], int]:
    """
    Return (probs_dict, pred_idx).
    Uses an in-memory LRU cache to speed repeated requests.
    """
    text = _prepare_text(text)
    key = f"{model_id}::{text}"
    cached = PRED_CACHE.get(key)
    if cached is not None:
        return cached

    tokenizer, model, device = load_model(model_id)
    enc = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        out = model(**enc)
        logits = out.logits
        probs = F.softmax(logits, dim=-1).cpu().numpy().flatten()

    # infer labels from model config if possible
    if getattr(model.config, "id2label", None):
        labels = [model.config.id2label[i] for i in sorted(model.config.id2label.keys())]
    else:
        labels = ["legitimate", "phishing"]

    probs_dict = {labels[i]: float(probs[i]) for i in range(len(probs))}
    pred_idx = int(np.argmax(probs))

    PRED_CACHE.set(key, (probs_dict, pred_idx))
    return probs_dict, pred_idx

def predict_batch(texts: List[str], model_id: str = MODEL_ID_DEFAULT) -> List[Dict[str, Any]]:
    results = []
    for t in texts:
        probs, idx = predict_raw(t, model_id)
        top_label = max(probs.items(), key=lambda kv: kv[1])[0]
        top_conf = probs[top_label]
        results.append({"label": top_label, "confidence": float(top_conf), "probs": probs})
    return results

# ---------------- FastAPI app and schemas ----------------
app = FastAPI(title="Phishing classifier API")

# CORS
origins = [o.strip() for o in ALLOWED_ORIGINS.split(",")] if ALLOWED_ORIGINS != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str
    model_id: Optional[str] = None

class BatchRequest(BaseModel):
    texts: List[str]
    model_id: Optional[str] = None

@app.on_event("startup")
def startup_event():
    """
    Warm the default model in a background thread to avoid blocking startup.
    This keeps the process healthy even if model download fails initially.
    """
    def _warm():
        try:
            load_model(MODEL_ID_DEFAULT)
        except Exception as e:
            logger.warning("Warning: model load at startup failed: %s", e)
    t = threading.Thread(target=_warm, daemon=True)
    t.start()
    logger.info("Startup complete; warm-up background thread started.")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    """Return readiness based on whether the model is loaded."""
    loaded = _model is not None
    return {"ready": bool(loaded), "model_loaded": bool(loaded)}

@app.post("/predict")
def predict(req: PredictRequest):
    text = _prepare_text(req.text)
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    model_id = req.model_id or MODEL_ID_DEFAULT
    try:
        probs, pred_idx = predict_raw(text, model_id)
        top_label = max(probs.items(), key=lambda kv: kv[1])[0]
        top_conf = probs[top_label]
        return {
            "model_id": model_id,
            "label": top_label,
            "confidence": float(top_conf),
            "probs": probs,
            "pred_idx": int(pred_idx),
        }
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_batch")
def predict_batch_endpoint(req: BatchRequest):
    texts = req.texts or []
    if not texts:
        raise HTTPException(status_code=400, detail="Empty texts list")
    model_id = req.model_id or MODEL_ID_DEFAULT
    try:
        res = predict_batch(texts, model_id)
        return {"model_id": model_id, "results": res}
    except Exception as e:
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reload")
def reload_model(model_id: Optional[str] = None):
    model_id = model_id or MODEL_ID_DEFAULT
    try:
        load_model(model_id)
        PRED_CACHE.clear()
        return {"reloaded": model_id}
    except Exception as e:
        logger.exception("Reload failed")
        raise HTTPException(status_code=500, detail=str(e))

# simple global exception handler to return JSON on unexpected errors
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception("Unhandled error during request: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")
