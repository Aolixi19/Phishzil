import React from 'react';

const App = () => {
  const threatDetails = [
    'Phishing attempt detected',
    'Suspicious domain: malicious-site.com',
    'Risk Level: HIGH',
    'Detection Time: 0.3 seconds',
  ];

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100 font-inter">
      <div className="relative w-full max-w-sm p-8 mx-auto text-center bg-white border-2 border-red-500 shadow-2xl rounded-3xl">
        {/* Top Icon */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center justify-center w-20 h-20 rounded-full shadow-inner bg-red-50">
            <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.368 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          </div>
        </div>

        {/* Title and Subtitle */}
        <h2 className="mb-2 text-2xl font-bold text-red-500">THREAT DETECTED</h2>
        <p className="mb-6 text-gray-500">This link was identified as dangerous and has been disabled for your protection.</p>

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
          <button className="flex items-center justify-center flex-1 px-6 py-3 space-x-2 font-semibold text-white transition-colors duration-200 bg-red-500 rounded-lg hover:bg-red-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M18 12h.01"></path></svg>
            <span>View Report</span>
          </button>
          <button className="flex items-center justify-center flex-1 px-6 py-3 space-x-2 font-semibold text-gray-700 transition-colors duration-200 bg-gray-200 rounded-lg hover:bg-gray-300">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            <span>Dismiss</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;
