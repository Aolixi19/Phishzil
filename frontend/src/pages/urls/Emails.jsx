import React, { useState } from 'react';
import { Link } from "react-router-dom";

import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";




const Emails = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

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
      // Logic to send file for scanning
      console.log('Scanning file:', selectedFile.name);
      // In a real app, you'd send this file to a backend API
      // For now, just clear the file after "scanning"
      setSelectedFile(null);
    } else {
      console.log('No file selected to scan.');
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100 font-inter">
     <Sidebar />
      

      {/* Main Content Area */}
      <main className="flex-1 lg:ml-64 p-4 sm:p-6 lg:p-8">
        <Topbar />
        
        

        {/* Breadcrumbs */}
        <nav className="text-sm text-gray-500 mb-6">
          <ol className="list-none p-0 inline-flex">
            <li className="flex items-center">
              <Link to="/" className="text-blue-600 hover:underline">Home</Link>
            </li>

            <li className="ml-2">Email Scanner</li>

          </ol>
        </nav>

        {/* Scan Your Emails Section */}
        <section className="bg-white rounded-xl shadow-md p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-800">Scan Your Emails</h2>
              <p className="text-sm text-gray-500">
                Real-time email scanner detecting phishing, scams, and threats by analyzing sender domains, attachments, URLs, and brand impersonation.
              </p>
            </div>
            <button className="p-2 rounded-full text-blue-500 hover:bg-blue-50 transition duration-150">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9.228a4.5 4.5 0 116.364 0M12 14v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </button>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center sm:justify-start space-y-4 sm:space-y-0 sm:space-x-4 mb-6">
            <button className="bg-blue-100 text-blue-600 px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-200 transition duration-150">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8m-9 13h9A2 2 0 0021 19V5a2 2 0 00-2-2H3a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
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
              <div className="text-gray-700 text-lg mb-4">
                File selected: <span className="font-medium text-blue-600">{selectedFile.name}</span>
              </div>
            ) : (
              <>
                <div className="text-gray-500 mb-2">
                  <svg className="mx-auto w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                  <p className="text-lg font-medium">Upload Email here</p>
                  <p className="text-sm">Drag and Drop or <label htmlFor="emailFile" className="text-blue-600 cursor-pointer hover:underline">Upload</label></p>
                </div>
                <p className="text-xs text-gray-400 mb-4">
                  File format: .eml - file size is under 25 MB
                </p>
                <label htmlFor="emailFile" className="inline-flex items-center justify-center p-3 rounded-full bg-blue-500 text-white cursor-pointer shadow-md hover:bg-blue-600 transition duration-150">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                </label>
              </>
            )}

            <div className="mt-6 flex justify-center space-x-4">
              <button
                onClick={handleClearFile}
                className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100 transition duration-150"
              >
                Clear
              </button>
              <button
                onClick={handleScanFile}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-150"
              >
                Scan
              </button>
            </div>
          </div>
          <p className="text-sm text-blue-600 text-center mt-4 hover:underline cursor-pointer">
            Learn how to save an email as an .eml file
          </p>
        </section>

        {/* My Email Scans Table Section */}
        <section className="bg-white rounded-xl shadow-md p-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-3 sm:mb-0">My Email Scans</h2>
            <div className="flex items-center space-x-2 text-sm">
              <select className="border border-gray-300 rounded-md py-1 px-2 focus:ring-blue-500 focus:border-blue-500">
                <option>Apr 07, 2025 - Jul 06, 2025</option>
                <option>Last 30 Days</option>
                <option>Last 90 Days</option>
              </select>
              <button className="p-2 rounded-md text-gray-600 hover:bg-gray-100 transition duration-150">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source URL
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    IP Address
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Hosting Provider
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Brand
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {mockEmailScans.map((scan, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600 hover:underline">
                      <a href={scan.sourceUrl} target="_blank" rel="noopener noreferrer">{scan.sourceUrl}</a>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.ipAddress}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.hostingProvider}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.source}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {scan.brand}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
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
