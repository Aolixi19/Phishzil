import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

//  Import images from assets
import Online from "../assets/online.png";
import chatbot from "../assets/chatbot.png";
import cat from "../assets/cat.png";
import catte from "../assets/catte.png";

const stages = [
  {
    title: "Scanning URL",
    subtitle: "Checking the provided link for suspicious patterns",
    image: Online,
    steps: ["Initializing scanner", "Analyzing URL format", "Querying threat database"],
    progress: 0
  },
  {
    title: "Identifying Threat",
    subtitle: "Matching against known phishing signatures",
    image: chatbot,
    steps: ["Loading threat signatures", "Matching patterns", "Threat identified"],
    progress: 25
  },
  {
    title: "Neutralizing Threat",
    subtitle: "Removing malicious payload from the link",
    image: cat,
    steps: ["Disabling harmful scripts", "Removing redirects", "Cleaning embedded payloads"],
    progress: 50
  },
  {
    title: "Securing Device",
    subtitle: "Ensuring no residual malicious code remains",
    image: cat, // same as Stage 3
    steps: ["Scanning local cache", "Verifying system integrity", "Applying security patches"],
    progress: 75
  },
  {
    title: "Phishing Link Neutralized Successfully!",
    subtitle: "Protecting your device from malicious content",
    image: catte,
    steps: ["URL analyzed and categorized", "Threat signatures identified", "Neutralizing malicious code"],
    progress: 100,
    final: true
  }
];

const Phlink = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const scanUrl = location.state?.scanUrl || "No URL provided";

  const [stageIndex, setStageIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);

  useEffect(() => {
    if (stageIndex >= stages.length) return;

    setCompletedSteps([]);
    const stage = stages[stageIndex];
    setProgress(stage.progress);

    let stepTimeouts = [];
    stage.steps.forEach((step, i) => {
      stepTimeouts.push(
        setTimeout(() => {
          setCompletedSteps(prev => [...prev, step]);
        }, (i + 1) * 800)
      );
    });

    const stageDuration = (stage.steps.length + 1) * 800;
    const timeout = setTimeout(() => {
      setStageIndex(prev => prev + 1);
    }, stageDuration + 500);

    return () => {
      clearTimeout(timeout);
      stepTimeouts.forEach(t => clearTimeout(t));
    };
  }, [stageIndex]);

  const stage = stages[stageIndex] || stages[stages.length - 1];

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100 font-inter">
      <div className="relative w-full max-w-sm p-8 mx-auto text-center bg-white shadow-2xl rounded-3xl">
        
        <div className="mb-4 text-xs text-gray-500 break-all">
          Scanning: <span className="font-medium text-gray-700">{scanUrl}</span>
        </div>

        <div className="flex justify-center mb-6">
          <div className="flex items-center justify-center w-20 h-20 rounded-full shadow-inner bg-red-50">
            <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.001 12.001 0 002 12c0 2.757 1.299 5.232 3.365 6.931l1.624 1.625a1 1 0 00.707.293h7.408a1 1 0 00.707-.293l1.624-1.625C20.701 17.232 22 14.757 22 12c0-2.091-.707-4.016-1.977-5.556z"></path>
            </svg>
          </div>
        </div>

        <h2 className="mb-2 text-2xl font-bold text-gray-800">{stage.title}</h2>
        <p className="mb-8 text-gray-500">{stage.subtitle}</p>

        <div className="flex justify-center mb-8">
          <img
            src={stage.image}
            alt="Stage illustration"
            className="w-full h-auto max-w-xs animate-pulse"
          />
        </div>

        <div className="mb-6">
          <div className="flex items-center justify-between mb-2 text-sm font-medium text-gray-700">
            <span>DISARMING</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full">
            <div
              className="h-2 transition-all duration-500 ease-out bg-red-500 rounded-full"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        <div className="mb-8 text-left">
          {completedSteps.map((step, index) => (
            <div key={index} className="flex items-center py-1 text-sm font-medium text-gray-700">
              <svg className="w-4 h-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
              </svg>
              <span>{step}</span>
            </div>
          ))}
        </div>

        {stage.final && (
          <button
            onClick={() => navigate("/")}
            className="flex items-center justify-center w-full py-3 space-x-2 font-semibold text-white transition-colors duration-200 bg-green-500 rounded-lg hover:bg-green-600"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M18 12h.01"></path>
            </svg>
            <span>Done</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default Phlink;
