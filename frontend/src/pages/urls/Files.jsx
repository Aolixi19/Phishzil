import React, { useState } from 'react';
import { Link } from "react-router-dom";

import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

const File = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  // Mock data for recent scan results
  const mockScanResults = [
    {
      id: 1,
      fileName: 'invoice_march.pdf',
      description: 'Malicious link detected',
      status: 'THREAT',
      icon: (
        <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
      ),
      statusColor: 'bg-red-100 text-red-800',
    },
    {
      id: 2,
      fileName: 'report_final.docx',
      description: 'Clean - No threats found',
      status: 'CLEAN',
      icon: (
        <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
      ),
      statusColor: 'bg-green-100 text-green-800',
      checkIcon: (
        <svg className="w-5 h-5 text-green-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
      ),
    },
    {
      id: 3,
      fileName: 'documents.zip',
      description: 'Suspicious macro detected',
      status: 'QUARANTINED',
      icon: (
        <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
      ),
      statusColor: 'bg-orange-100 text-orange-800',
      alertIcon: (
        <svg className="w-5 h-5 text-orange-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
      ),
    },
  ];

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleSelectFiles = () => {
    document.getElementById('fileUploadInput').click();
  };

  const handleScanFolder = () => {
    // Logic for scanning a folder (would typically involve a file system access API or backend)
    console.log('Scan Folder clicked');
    alert('Folder scanning functionality is not implemented in this demo.');
  };

  const handleRecentScans = () => {
    // Logic to navigate to a page showing all recent scans or open a modal
    console.log('Recent Scans clicked');
    alert('Recent scans history functionality is not implemented in this demo.');
  };

  return (
    <div className="flex min-h-screen bg-gray-100 font-inter">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 lg:ml-64 p-4 sm:p-6 lg:p-8">
        {/* Top Bar */}
         <Topbar />

        {/* Breadcrumbs */}
        <nav className="text-sm text-gray-500 mb-6">
          <ol className="list-none p-0 inline-flex">
            <li className="flex items-center">
              <Link to="/" className="text-blue-600 hover:underline">Home</Link>
            </li>

            <li className="ml-2">File Scanner</li>

          </ol>
        </nav>

        {/* Scan Files for Threats Section */}
        <section className="bg-white rounded-xl shadow-md p-6 mb-8">
          <div className="text-center mb-6">
            <div className="inline-block p-3 rounded-full bg-blue-100 text-blue-600 mb-4">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            </div>
            <h2 className="text-lg font-semibold text-gray-800 mb-2">Scan Files for Threats</h2>
            <p className="text-sm text-gray-500">
              Upload files or drag them here to scan for malicious content, embedded links, and macros
            </p>
          </div>

          {/* File Upload Area */}
          <div
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors duration-200
              ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'}
            `}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="fileUploadInput"
              className="hidden"
              onChange={handleFileSelect}
              multiple // Allow multiple files if needed, based on typical file scanner behavior
            />
            <div className="text-gray-500 mb-4">
              <svg className="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              <p className="text-lg font-medium">Drop files here or click to browse</p>
            </div>
            {selectedFile && (
              <p className="text-sm text-gray-700 mb-4">Selected: <span className="font-medium text-blue-600">{selectedFile.name}</span></p>
            )}
            <p className="text-xs text-gray-400">
              Supports: PDF, DOCX, XLSX, ZIP, EXE, APK and more
            </p>
          </div>

          <div className="mt-6 flex flex-col sm:flex-row justify-center space-y-3 sm:space-y-0 sm:space-x-4">
            <button
              onClick={handleSelectFiles}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg flex items-center justify-center space-x-2 hover:bg-blue-700 transition duration-150 shadow-md"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              <span>Select Files</span>
            </button>
            <button
              onClick={handleScanFolder}
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 flex items-center justify-center space-x-2 hover:bg-gray-100 transition duration-150"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
              <span>Scan Folder</span>
            </button>
            <button
              onClick={handleRecentScans}
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 flex items-center justify-center space-x-2 hover:bg-gray-100 transition duration-150"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253"></path></svg>
              <span>Recent Scans</span>
            </button>
          </div>
        </section>

        {/* Recent Scan Results Section */}
        <section className="bg-white rounded-xl shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Recent Scan Results</h2>
            <a href="/reports" className="text-blue-600 text-sm font-medium hover:underline">View All</a>
          </div>

          <div className="space-y-4">
            {mockScanResults.map((result) => (
              <div key={result.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {result.icon}
                  <div>
                    <p className="text-sm font-medium text-gray-800">{result.fileName}</p>
                    <p className="text-xs text-gray-500">{result.description}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${result.statusColor}`}>
                    {result.status}
                  </span>
                  {result.checkIcon}
                  {result.alertIcon}
                  <button className="p-1 rounded-full text-gray-400 hover:bg-gray-200 transition duration-150">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default File;
