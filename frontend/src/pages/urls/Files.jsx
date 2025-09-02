import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";

import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

const File = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

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
        <svg className="w-5 h-5 ml-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
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
        <svg className="w-5 h-5 ml-2 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
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

  const handleScanFile = () => {
    if (selectedFile) {
      // Navigate to the PhFile component with the file info
      navigate("/ph-file", { 
        state: { 
          scanFile: selectedFile.name
        } 
      });
    } else {
      console.log('No file selected to scan.');
      alert('Please select a file to scan first.');
    }
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
      <main className="flex-1 p-4 lg:ml-64 sm:p-6 lg:p-8">
        {/* Top Bar */}
         <Topbar />

        {/* Breadcrumbs */}
        <nav className="mb-6 text-sm text-gray-500">
          <ol className="inline-flex p-0 list-none">
            <li className="flex items-center">
              <Link to="/" className="text-blue-600 hover:underline">Home</Link>
              <svg className="w-3 h-3 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </li>
            <li className="text-gray-400">File Scanner</li>
          </ol>
        </nav>

        {/* Scan Files for Threats Section */}
        <section className="p-6 mb-8 bg-white shadow-md rounded-xl">
          <div className="mb-6 text-center">
            <div className="inline-block p-3 mb-4 text-blue-600 bg-blue-100 rounded-full">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            </div>
            <h2 className="mb-2 text-lg font-semibold text-gray-800">Scan Files for Threats</h2>
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
            <div className="mb-4 text-gray-500">
              <svg className="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              <p className="text-lg font-medium">Drop files here or click to browse</p>
            </div>
            {selectedFile && (
              <p className="mb-4 text-sm text-gray-700">Selected: <span className="font-medium text-blue-600">{selectedFile.name}</span></p>
            )}
            <p className="text-xs text-gray-400">
              Supports: PDF, DOCX, XLSX, ZIP, EXE, APK and more
            </p>
          </div>

          <div className="flex flex-col justify-center mt-6 space-y-3 sm:flex-row sm:space-y-0 sm:space-x-4">
            <button
              onClick={handleSelectFiles}
              className="flex items-center justify-center px-6 py-3 space-x-2 text-white transition duration-150 bg-blue-600 rounded-lg shadow-md hover:bg-blue-700"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              <span>Select Files</span>
            </button>
            <button
              onClick={handleScanFile}
              className="flex items-center justify-center px-6 py-3 space-x-2 text-white transition duration-150 bg-green-600 rounded-lg shadow-md hover:bg-green-700"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.001 12.001 0 002 12c0 2.757 1.299 5.232 3.365 6.931l1.624 1.625a1 1 0 00.707.293h7.408a1 1 0 00.707-.293l1.624-1.625C20.701 17.232 22 14.757 22 12c0-2.091-.707-4.016-1.977-5.556z"></path></svg>
              <span>Scan File</span>
            </button>
            <button
              onClick={handleScanFolder}
              className="flex items-center justify-center px-6 py-3 space-x-2 text-gray-700 transition duration-150 border border-gray-300 rounded-lg hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
              <span>Scan Folder</span>
            </button>
            <button
              onClick={handleRecentScans}
              className="flex items-center justify-center px-6 py-3 space-x-2 text-gray-700 transition duration-150 border border-gray-300 rounded-lg hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18s-3.332.477-4.5 1.253"></path></svg>
              <span>Recent Scans</span>
            </button>
          </div>
        </section>

        {/* Recent Scan Results Section */}
        <section className="p-6 bg-white shadow-md rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Recent Scan Results</h2>
            <a href="/reports" className="text-sm font-medium text-blue-600 hover:underline">View All</a>
          </div>

          <div className="space-y-4">
            {mockScanResults.map((result) => (
              <div key={result.id} className="flex items-center justify-between p-4 rounded-lg bg-gray-50">
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
                  <button className="p-1 text-gray-400 transition duration-150 rounded-full hover:bg-gray-200">
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