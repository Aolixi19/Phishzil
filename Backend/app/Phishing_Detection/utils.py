import re
import hashlib
import urllib.parse
import dns.resolver
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import magic
import whois
from dataclasses import dataclass

@dataclass
class ThreatAssessment:
    is_malicious: bool
    threat_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    confidence_score: float  # 0.0 to 1.0
    threat_types: List[str]
    indicators: List[str]
    recommended_action: str
    details: Dict[str, Any]

def analyze_security_threat(
    url: Optional[str] = None,
    file_path: Optional[str] = None,
    file_content: Optional[bytes] = None,
    message_content: Optional[str] = None,
    sender_info: Optional[Dict] = None,
    context: Optional[str] = None  # 'email', 'sms', 'chat', 'web'
) -> ThreatAssessment:
    """
    Comprehensive security threat analysis function that detects phishing links 
    and malicious attachments across multiple communication channels.
    
    Args:
        url: URL to analyze for phishing indicators
        file_path: Path to file attachment to analyze
        file_content: Raw file content as bytes
        message_content: Text content of message/email
        sender_info: Dict with sender details (email, domain, etc.)
        context: Communication channel context
    
    Returns:
        ThreatAssessment: Comprehensive threat analysis results
    """
    
    threat_indicators = []
    threat_types = []
    risk_scores = []
    details = {}
    
    # URL Analysis
    if url:
        url_analysis = _analyze_url(url)
        threat_indicators.extend(url_analysis['indicators'])
        threat_types.extend(url_analysis['threat_types'])
        risk_scores.append(url_analysis['risk_score'])
        details['url_analysis'] = url_analysis
    
    # File Analysis
    if file_path or file_content:
        file_analysis = _analyze_file(file_path, file_content)
        threat_indicators.extend(file_analysis['indicators'])
        threat_types.extend(file_analysis['threat_types'])
        risk_scores.append(file_analysis['risk_score'])
        details['file_analysis'] = file_analysis
    
    # Content Analysis
    if message_content:
        content_analysis = _analyze_content(message_content, context)
        threat_indicators.extend(content_analysis['indicators'])
        threat_types.extend(content_analysis['threat_types'])
        risk_scores.append(content_analysis['risk_score'])
        details['content_analysis'] = content_analysis
    
    # Sender Analysis
    if sender_info:
        sender_analysis = _analyze_sender(sender_info, context)
        threat_indicators.extend(sender_analysis['indicators'])
        threat_types.extend(sender_analysis['threat_types'])
        risk_scores.append(sender_analysis['risk_score'])
        details['sender_analysis'] = sender_analysis
    
    # Calculate overall threat assessment
    if risk_scores:
        max_risk = max(risk_scores)
        avg_risk = sum(risk_scores) / len(risk_scores)
        confidence_score = min(max_risk + (avg_risk * 0.3), 1.0)
    else:
        confidence_score = 0.0
    
    # Determine threat level and action
    is_malicious = confidence_score >= 0.7
    
    if confidence_score >= 0.9:
        threat_level = 'CRITICAL'
        action = 'BLOCK_IMMEDIATELY'
    elif confidence_score >= 0.7:
        threat_level = 'HIGH'
        action = 'QUARANTINE_AND_ALERT'
    elif confidence_score >= 0.4:
        threat_level = 'MEDIUM'
        action = 'WARN_USER'
    else:
        threat_level = 'LOW'
        action = 'ALLOW_WITH_MONITORING'
    
    return ThreatAssessment(
        is_malicious=is_malicious,
        threat_level=threat_level,
        confidence_score=confidence_score,
        threat_types=list(set(threat_types)),
        indicators=list(set(threat_indicators)),
        recommended_action=action,
        details=details
    )

def _analyze_url(url: str) -> Dict[str, Any]:
    """Analyze URL for phishing and malicious indicators."""
    indicators = []
    threat_types = []
    risk_score = 0.0
    
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        # Suspicious URL patterns
        suspicious_patterns = [
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP address
            r'[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+\.',  # Multiple hyphens
            r'[a-zA-Z]{20,}',  # Very long domain parts
            r'bit\.ly|tinyurl|t\.co|goo\.gl|short\.link',  # URL shorteners
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, domain):
                indicators.append(f"Suspicious URL pattern: {pattern}")
                risk_score += 0.3
        
        # Domain spoofing detection
        legitimate_domains = [
            'google.com', 'amazon.com', 'microsoft.com', 'apple.com',
            'paypal.com', 'ebay.com', 'facebook.com', 'twitter.com'
        ]
        
        for legit_domain in legitimate_domains:
            if _is_domain_spoofing(domain, legit_domain):
                indicators.append(f"Possible domain spoofing of {legit_domain}")
                threat_types.append('DOMAIN_SPOOFING')
                risk_score += 0.8
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.buzz', '.click']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            indicators.append("Suspicious top-level domain")
            risk_score += 0.4
        
        # Domain age check (simulated)
        domain_age = _check_domain_age(domain)
        if domain_age < 30:  # Less than 30 days old
            indicators.append("Recently registered domain")
            risk_score += 0.5
        
        # SSL certificate check
        ssl_status = _check_ssl_certificate(domain)
        if not ssl_status['valid']:
            indicators.append("Invalid or missing SSL certificate")
            risk_score += 0.3
        
        # URL length and complexity
        if len(url) > 200:
            indicators.append("Unusually long URL")
            risk_score += 0.2
        
        if url.count('.') > 4:
            indicators.append("Excessive subdomains")
            risk_score += 0.3
        
        # Check for URL encoding obfuscation
        if '%' in url and len(re.findall(r'%[0-9A-Fa-f]{2}', url)) > 3:
            indicators.append("URL encoding obfuscation")
            risk_score += 0.4
        
    except Exception as e:
        indicators.append(f"URL parsing error: {str(e)}")
        risk_score += 0.2
    
    return {
        'indicators': indicators,
        'threat_types': threat_types,
        'risk_score': min(risk_score, 1.0),
        'domain': domain if 'domain' in locals() else None
    }

def _analyze_file(file_path: Optional[str], file_content: Optional[bytes]) -> Dict[str, Any]:
    """Analyze file attachment for malicious indicators."""
    indicators = []
    threat_types = []
    risk_score = 0.0
    
    try:
        # Get file content
        if file_path:
            with open(file_path, 'rb') as f:
                content = f.read()
            filename = file_path.split('/')[-1]
        else:
            content = file_content
            filename = "unknown"
        
        # File type detection
        try:
            file_type = magic.from_buffer(content, mime=True)
        except:
            file_type = "unknown"
        
        # Suspicious file extensions
        suspicious_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.vbs', 
            '.js', '.jar', '.ps1', '.msi', '.deb', '.rpm'
        ]
        
        if any(filename.lower().endswith(ext) for ext in suspicious_extensions):
            indicators.append(f"Suspicious file extension: {filename}")
            threat_types.append('MALICIOUS_EXECUTABLE')
            risk_score += 0.8
        
        # Double extension check
        if filename.count('.') > 1:
            parts = filename.split('.')
            if len(parts) > 2 and parts[-1].lower() in ['exe', 'scr', 'bat']:
                indicators.append("Double file extension detected")
                threat_types.append('EXTENSION_SPOOFING')
                risk_score += 0.9
        
        # Macro-enabled Office documents
        macro_types = [
            'application/vnd.ms-excel.sheet.macroEnabled.12',
            'application/vnd.ms-word.document.macroEnabled.12',
            'application/vnd.ms-powerpoint.presentation.macroEnabled.12'
        ]
        
        if file_type in macro_types:
            indicators.append("Macro-enabled Office document")
            threat_types.append('MACRO_MALWARE')
            risk_score += 0.6
        
        # File size anomalies
        if len(content) > 50 * 1024 * 1024:  # > 50MB
            indicators.append("Unusually large file size")
            risk_score += 0.2
        elif len(content) < 100 and filename.lower().endswith(('.pdf', '.doc', '.docx')):
            indicators.append("Suspiciously small file for type")
            risk_score += 0.4
        
        # Entropy analysis (simplified)
        entropy = _calculate_entropy(content[:1024])  # First 1KB
        if entropy > 7.5:  # High entropy suggests encryption/packing
            indicators.append("High entropy content (possibly packed/encrypted)")
            threat_types.append('PACKED_EXECUTABLE')
            risk_score += 0.5
        
        # Archive analysis
        if file_type in ['application/zip', 'application/x-rar']:
            archive_analysis = _analyze_archive(content)
            indicators.extend(archive_analysis['indicators'])
            threat_types.extend(archive_analysis['threat_types'])
            risk_score += archive_analysis['risk_score']
        
        # Basic signature detection (simplified)
        malicious_signatures = [
            b'eval(', b'document.write', b'shell.application',
            b'WScript.Shell', b'powershell', b'cmd.exe'
        ]
        
        for sig in malicious_signatures:
            if sig in content:
                indicators.append(f"Malicious signature detected: {sig.decode('utf-8', errors='ignore')}")
                threat_types.append('MALICIOUS_CODE')
                risk_score += 0.7
        
    except Exception as e:
        indicators.append(f"File analysis error: {str(e)}")
        risk_score += 0.1
    
    return {
        'indicators': indicators,
        'threat_types': threat_types,
        'risk_score': min(risk_score, 1.0),
        'file_type': file_type if 'file_type' in locals() else None,
        'filename': filename if 'filename' in locals() else None
    }

def _analyze_content(content: str, context: Optional[str]) -> Dict[str, Any]:
    """Analyze message content for social engineering and phishing indicators."""
    indicators = []
    threat_types = []
    risk_score = 0.0
    
    # Urgency keywords
    urgency_patterns = [
        r'urgent(ly)?', r'immediate(ly)?', r'expire[sd]?', r'suspend(ed)?',
        r'verify (now|immediately)', r'act (now|fast)', r'limited time',
        r'within \d+ hours?', r'deadline', r'final (notice|warning)'
    ]
    
    urgency_matches = sum(1 for pattern in urgency_patterns 
                         if re.search(pattern, content, re.IGNORECASE))
    
    if urgency_matches >= 2:
        indicators.append("Multiple urgency indicators detected")
        threat_types.append('SOCIAL_ENGINEERING')
        risk_score += 0.6
    elif urgency_matches >= 1:
        indicators.append("Urgency language detected")
        risk_score += 0.3
    
    # Credential harvesting patterns
    credential_patterns = [
        r'(verify|confirm|update).*(password|account|credentials)',
        r'click here to (login|sign in|verify)',
        r'suspended.*(account|service)',
        r'security (alert|warning|breach)',
        r'unauthorized (access|activity)'
    ]
    
    for pattern in credential_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            indicators.append(f"Credential harvesting pattern: {pattern}")
            threat_types.append('CREDENTIAL_HARVESTING')
            risk_score += 0.7
    
    # Financial fraud indicators
    financial_patterns = [
        r'(won|prize|lottery|inheritance)', r'transfer.*money',
        r'bank.*details', r'wire transfer', r'western union',
        r'advance fee', r'processing fee', r'tax payment'
    ]
    
    financial_matches = sum(1 for pattern in financial_patterns 
                           if re.search(pattern, content, re.IGNORECASE))
    
    if financial_matches >= 2:
        indicators.append("Financial fraud indicators")
        threat_types.append('FINANCIAL_FRAUD')
        risk_score += 0.8
    
    # Authority impersonation
    authority_patterns = [
        r'(IT|technical) (support|department|team)',
        r'(security|admin|administrator) (team|department)',
        r'(bank|government|IRS|police)',
        r'microsoft|google|apple (support|security)'
    ]
    
    for pattern in authority_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            indicators.append("Authority impersonation detected")
            threat_types.append('AUTHORITY_IMPERSONATION')
            risk_score += 0.5
    
    # Poor grammar/spelling (simplified check)
    grammar_issues = len(re.findall(r'\b[a-z]+[A-Z][a-z]*\b', content))  # CamelCase in middle of words
    if grammar_issues > 3:
        indicators.append("Multiple grammar/spelling inconsistencies")
        risk_score += 0.2
    
    # Generic greetings (often used in mass phishing)
    generic_greetings = ['dear customer', 'dear user', 'dear sir/madam', 'valued customer']
    if any(greeting in content.lower() for greeting in generic_greetings):
        indicators.append("Generic greeting used")
        risk_score += 0.2
    
    # Context-specific analysis
    if context == 'sms':
        # SMS-specific patterns
        if re.search(r'click.*link.*verify', content, re.IGNORECASE):
            indicators.append("SMS phishing pattern detected")
            threat_types.append('SMS_PHISHING')
            risk_score += 0.7
    
    elif context == 'email':
        # Email-specific patterns
        if 'unsubscribe' not in content.lower() and len(content) < 200:
            indicators.append("Short email without unsubscribe (possible phishing)")
            risk_score += 0.3
    
    return {
        'indicators': indicators,
        'threat_types': threat_types,
        'risk_score': min(risk_score, 1.0)
    }

def _analyze_sender(sender_info: Dict, context: Optional[str]) -> Dict[str, Any]:
    """Analyze sender information for spoofing and reputation issues."""
    indicators = []
    threat_types = []
    risk_score = 0.0
    
    sender_email = sender_info.get('email', '')
    sender_domain = sender_info.get('domain', '')
    display_name = sender_info.get('display_name', '')
    
    # Email spoofing detection
    if sender_email and display_name:
        # Check if display name suggests different organization
        display_domain_matches = re.findall(r'@([a-zA-Z0-9.-]+)', display_name)
        if display_domain_matches:
            display_domain = display_domain_matches[0].lower()
            actual_domain = sender_domain.lower()
            if display_domain != actual_domain:
                indicators.append("Display name domain mismatch")
                threat_types.append('EMAIL_SPOOFING')
                risk_score += 0.8
    
    # Check for suspicious sender patterns
    if sender_email:
        # Random character patterns
        if re.search(r'[a-z]{2,}[0-9]{3,}@', sender_email):
            indicators.append("Suspicious sender email pattern")
            risk_score += 0.3
        
        # Free email providers for business context
        free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        if any(provider in sender_email for provider in free_providers):
            if context == 'business' or 'invoice' in display_name.lower():
                indicators.append("Business communication from free email provider")
                risk_score += 0.4
    
    # Domain reputation check (simulated)
    if sender_domain:
        domain_reputation = _check_domain_reputation(sender_domain)
        if domain_reputation['score'] < 0.3:
            indicators.append("Poor sender domain reputation")
            threat_types.append('MALICIOUS_DOMAIN')
            risk_score += 0.6
    
    return {
        'indicators': indicators,
        'threat_types': threat_types,
        'risk_score': min(risk_score, 1.0)
    }

# Helper functions (simplified implementations)

def _is_domain_spoofing(domain: str, legitimate: str) -> bool:
    """Check if domain is spoofing a legitimate domain."""
    # Levenshtein distance check (simplified)
    if abs(len(domain) - len(legitimate)) <= 2:
        differences = sum(c1 != c2 for c1, c2 in zip(domain, legitimate))
        return differences <= 2 and domain != legitimate
    return False

def _check_domain_age(domain: str) -> int:
    """Check domain registration age (returns days, simplified)."""
    try:
        # This would use WHOIS lookup in real implementation
        # Simulated response for demo
        return 100  # Default to 100 days
    except:
        return 0

def _check_ssl_certificate(domain: str) -> Dict[str, Any]:
    """Check SSL certificate validity (simplified)."""
    # Simulated SSL check
    return {'valid': True, 'issuer': 'Unknown'}
import math
def _calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of data."""
    if not data:
        return 0
    
    # Count frequency of each byte
    frequency = {}
    for byte in data:
        frequency[byte] = frequency.get(byte, 0) + 1
    
    # Calculate Shannon entropy
    entropy = 0
    length = len(data)
    
    for count in frequency.values():
        if count > 0:
            p = count / length
            entropy -= p * math.log2(p)
    
    return entropy

def _analyze_archive(content: bytes) -> Dict[str, Any]:
    """Analyze archive files for malicious content (simplified)."""
    # Simplified archive analysis
    indicators = []
    threat_types = []
    risk_score = 0.0
    
    # Check for password protection indicators
    if b'encrypted' in content[:1024]:
        indicators.append("Password-protected archive")
        threat_types.append('EVASION_TECHNIQUE')
        risk_score += 0.5
    
    return {
        'indicators': indicators,
        'threat_types': threat_types,
        'risk_score': risk_score
    }

def _check_domain_reputation(domain: str) -> Dict[str, Any]:
    """Check domain reputation (simplified)."""
    # Simulated reputation check
    return {'score': 0.8, 'category': 'clean'}

# Example usage:
if __name__ == "__main__":
    # Test with suspicious URL
    result = analyze_security_threat(
        url="http://arnazon-security.tk/login?verify=true&user=12345",
        message_content="URGENT: Your Amazon account has been suspended. Click here to verify immediately!",
        sender_info={'email': 'security123@gmail.com', 'display_name': 'Amazon Security'},
        context='email'
    )
    
    print(f"Threat Level: {result.threat_level}")
    print(f"Confidence: {result.confidence_score:.2f}")
    print(f"Action: {result.recommended_action}")
    print(f"Indicators: {result.indicators}")