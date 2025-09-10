import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

// Import images from assets
import Toy from "../assets/toy.png";
import research from "../assets/research.png";
import Online from "../assets/online.png";
import check from "../assets/check.png";

const stages = [
  {
    title: "Scanning Email",
    subtitle: "Analyzing the provided email for phishing indicators",
    image: Toy,
    steps: ["Initializing scanner", "Extracting headers", "Parsing email content"],
    progress: 0
  },
  {
    title: "Identifying Threat",
    subtitle: "Matching against known phishing templates",
    image: research,
    steps: ["Loading threat patterns", "Matching templates", "Threat detected"],
    progress: 25
  },
  {
    title: "Neutralizing Threat",
    subtitle: "Removing malicious links and attachments",
    image: Online,
    steps: ["Disabling harmful links", "Cleaning attachments", "Sanitizing HTML content"],
    progress: 50
  },
  {
    title: "Securing Inbox",
    subtitle: "Ensuring no residual malicious traces remain",
    image: check,
    steps: ["Scanning local cache", "Verifying email integrity", "Applying security measures"],
    progress: 75
  },
  {
    title: "Analysis Complete",
    subtitle: "Scan results ready",
    image: check, 
    steps: ["Email analyzed and categorized", "Threat signatures identified", "Generating security report"],
    progress: 100,
    final: true
  }
];

const PhEmail = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const scanEmail = location.state?.scanEmail || "No email provided";

  const [stageIndex, setStageIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (stageIndex >= stages.length) {
      // When all stages are complete, show results after a brief delay
      const timeout = setTimeout(() => {
        setShowResults(true);
      }, 1000);
      return () => clearTimeout(timeout);
    }

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

  const threatDetails = [
    'Email phishing attempt detected',
    `File Name: ${scanEmail}`,
    'Risk Level: HIGH',
    'Action Taken: Email quarantined',
    'Detection Time: 0.4 seconds',
    'Suspicious sender: phishing@malicious-domain.com'
  ];

  const handleViewReport = () => {
    // Navigate to the reports page with email scan data
    navigate("/reports", {
      state: {
        scanEmail: scanEmail,
        threatDetails: threatDetails,
        status: "THREAT_DETECTED",
        scanDate: new Date().toLocaleString(),
        scanType: "EMAIL" // Added to distinguish email scans from other types
      }
    });
  };

  // Show results page after scanning completes
  if (showResults) {
    return (
      <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100 font-inter">
        <div className="relative w-full max-w-sm p-8 mx-auto text-center bg-white border-2 border-red-500 shadow-2xl rounded-3xl">
          {/* Top Icon */}
          <div className="flex justify-center mb-6">
            <div className="flex items-center justify-center w-20 h-20 rounded-full shadow-inner bg-red-50">
              <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.368 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
            </div>
          </div>

          {/* Title and Subtitle */}
          <h2 className="mb-2 text-2xl font-bold text-red-500">THREAT DETECTED</h2>
          <p className="mb-6 text-gray-500">An email has been flagged as a phishing threat and was blocked to protect your system.</p>

          {/* Scanned Email */}
          <div className="p-3 mb-4 text-sm text-gray-700 bg-gray-100 rounded-lg">
            <span className="font-medium">Scanned Email:</span> {scanEmail}
          </div>

          {/* Threat Details Box */}
          <div className="p-4 mb-6 text-left border border-red-200 bg-red-50 rounded-xl">
            <p className="mb-2 font-semibold text-red-500">Threat Details:</p>
            <ul className="space-y-1 text-gray-700 list-disc list-inside">
              {threatDetails.map((detail, index) => (
                <li key={index}>{detail}</li>
              ))}
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <button 
              onClick={handleViewReport}
              className="flex items-center justify-center flex-1 px-6 py-3 space-x-2 font-semibold text-white transition-colors duration-200 bg-red-500 rounded-lg hover:bg-red-600"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M18 12h.01"></path>
              </svg>
              <span>View Report</span>
            </button>
            <button 
              onClick={() => navigate("/email-scanner")}
              className="flex items-center justify-center flex-1 px-6 py-3 space-x-2 font-semibold text-gray-700 transition-colors duration-200 bg-gray-200 rounded-lg hover:bg-gray-300"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
              <span>Done</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  const stage = stages[stageIndex] || stages[stages.length - 1];

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100 font-inter">
      <div className="relative w-full max-w-sm p-8 mx-auto text-center bg-white shadow-2xl rounded-3xl">
        
        <div className="mb-4 text-xs text-gray-500 break-all">
          Scanning: <span className="font-medium text-gray-700">{scanEmail}</span>
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
            <span>SCANNING</span>
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
      </div>
    </div>
  );
};

export default PhEmail;