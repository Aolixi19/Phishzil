import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";

import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

const Emails = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const navigate = useNavigate();

  // Mock data for the email scans table
  const mockEmailScans = [
    {
      sourceUrl: 'https://www.pngwing.com/en/wearc...',
      ipAddress: '104.21.73.185',
      hostingProvider: 'Cloudflare, Inc',
      source: 'Bulk Scan',
      date: '07 February, 2022',
      brand: 'Unknown',
      status: 'Clean',
    },
    {
      sourceUrl: 'https://fttgirl-repacks.site/popular-re...',
      ipAddress: '190.115.31.179',
      hostingProvider: 'DDOS-GUARD CORP',
      source: 'Bulk Scan',
      date: '09 January, 2022',
      brand: 'Unknown',
      status: 'Danger',
    },
    {
      sourceUrl: 'https://www.wps.com/1h3clickids:542...',
      ipAddress: '3.175.34.128',
      hostingProvider: '--',
      source: 'Bulk Scan',
      date: '15 December, 2021',
      brand: 'Unknown',
      status: 'Clean',
    },
    {
      sourceUrl: 'https://usbsmart.site/id1889-0-0.html',
      ipAddress: '190.41.17.106',
      hostingProvider: 'Cloudflare, Inc',
      source: 'Bulk Scan',
      date: '03 November, 2021',
      brand: 'Unknown',
      status: 'Clean',
    },
    {
      sourceUrl: 'https://mail.google.com/mail/u/0/#inbox/FMfc...',
      ipAddress: '172.217.160.1',
      hostingProvider: 'Google LLC',
      source: 'Manual Scan',
      date: '28 October, 2021',
      brand: 'Google',
      status: 'Clean',
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

  const handleClearFile = () => {
    setSelectedFile(null);
  };

  const handleScanFile = () => {
    if (selectedFile) {
      // Navigate to the PhEmail component with the file info
      navigate("/ph-email", { 
        state: { 
          scanEmail: selectedFile.name
        } 
      });
    } else {
      console.log('No file selected to scan.');
      // You could show an alert or notification here
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100 font-inter">
      <Sidebar />
      
      {/* Main Content Area */}
      <main className="flex-1 p-4 lg:ml-64 sm:p-6 lg:p-8">
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
            <li className="text-gray-400">Email Scanner</li>
          </ol>
        </nav>

        {/* Scan Your Emails Section */}
        <section className="p-6 mb-8 bg-white shadow-md rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-800">Scan Your Emails</h2>
              <p className="text-sm text-gray-500">
                Real-time email scanner detecting phishing, scams, and threats by analyzing sender domains, attachments, URLs, and brand impersonation.
              </p>
            </div>
            <button className="p-2 text-blue-500 transition duration-150 rounded-full hover:bg-blue-50">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9.228a4.5 4.5 0 116.364 0M12 14v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </button>
          </div>

          <div className="flex flex-col items-center justify-center mb-6 space-y-4 sm:flex-row sm:justify-start sm:space-y-0 sm:space-x-4">
            <button className="flex items-center px-4 py-2 space-x-2 text-blue-600 transition duration-150 bg-blue-100 rounded-lg hover:bg-blue-200">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8m-9 13h9A2 2 0 0021 19V5a2 2 0 00-2-2H3a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
              <span>Email Checker</span>
            </button>
            <span className="text-sm text-gray-500">240 Emails Scanned</span>
          </div>

          {/* File Upload Area */}
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200
              ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'}
            `}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="emailFile"
              className="hidden"
              onChange={handleFileSelect}
              accept=".eml" // Accept .eml files
            />
            {selectedFile ? (
              <div className="mb-4 text-lg text-gray-700">
                File selected: <span className="font-medium text-blue-600">{selectedFile.name}</span>
              </div>
            ) : (
              <>
                <div className="mb-2 text-gray-500">
                  <svg className="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                  <p className="text-lg font-medium">Upload Email here</p>
                  <p className="text-sm">Drag and Drop or <label htmlFor="emailFile" className="text-blue-600 cursor-pointer hover:underline">Upload</label></p>
                </div>
                <p className="mb-4 text-xs text-gray-400">
                  File format: .eml - file size is under 25 MB
                </p>
                <label htmlFor="emailFile" className="inline-flex items-center justify-center p-3 text-white transition duration-150 bg-blue-500 rounded-full shadow-md cursor-pointer hover:bg-blue-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                </label>
              </>
            )}

            <div className="flex justify-center mt-6 space-x-4">
              <button
                onClick={handleClearFile}
                className="px-6 py-2 text-gray-700 transition duration-150 border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                Clear
              </button>
              <button
                onClick={handleScanFile}
                className="px-6 py-2 text-white transition duration-150 bg-blue-600 rounded-lg hover:bg-blue-700"
              >
                Scan
              </button>
            </div>
          </div>
          <p className="mt-4 text-sm text-center text-blue-600 cursor-pointer hover:underline">
            Learn how to save an email as an .eml file
          </p>
        </section>

        {/* My Email Scans Table Section */}
        <section className="p-6 bg-white shadow-md rounded-xl">
          <div className="flex flex-col items-start justify-between mb-4 sm:flex-row sm:items-center">
            <h2 className="mb-3 text-lg font-semibold text-gray-800 sm:mb-0">My Email Scans</h2>
            <div className="flex items-center space-x-2 text-sm">
              <select className="px-2 py-1 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
                <option>Apr 07, 2025 - Jul 06, 2025</option>
                <option>Last 30 Days</option>
                <option>Last 90 Days</option>
              </select>
              <button className="p-2 text-gray-600 transition duration-150 rounded-md hover:bg-gray-100">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
                </svg>
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Source URL
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    IP Address
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Hosting Provider
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Source
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Brand
                  </th>
                  <th scope="col" className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {mockEmailScans.map((scan, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 text-sm font-medium text-blue-600 whitespace-nowrap hover:underline">
                      <a href={scan.sourceUrl} target="_blank" rel="noopener noreferrer">{scan.sourceUrl}</a>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                      {scan.ipAddress}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                      {scan.hostingProvider}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                      {scan.source}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                      {scan.date}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                      {scan.brand}
                    </td>
                    <td className="px-6 py-4 text-sm whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                        ${scan.status === 'Clean' ? 'bg-green-100 text-green-800' : ''}
                        ${scan.status === 'Danger' ? 'bg-red-100 text-red-800' : ''}
                      `}>
                        {scan.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Emails;