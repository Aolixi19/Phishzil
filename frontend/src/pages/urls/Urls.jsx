import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom"; //  Added useNavigate
import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

const Urls = () => {
  const [urlToScan, setUrlToScan] = useState('');

  const navigate = useNavigate(); //  Added navigate hook

  // Mock data for the URL scans table
  const mockUrlScans = [
    {
      id: 1,
      sourceUrl: 'https://www.pngwing.com/en/wearc...',
      ipAddress: '104.21.73.185',
      hostingProvider: 'Cloudflare, Inc',
      source: 'Bulk Scan',
      date: '07 February, 2022',
      brand: 'Unknown',
      status: 'Clean',
    },
    {
      id: 2,
      sourceUrl: 'https://fttgirl-repacks.site/popular-re...',
      ipAddress: '190.115.31.179',
      hostingProvider: 'DDOS-GUARD CORP',
      source: 'Bulk Scan',
      date: '09 January, 2022',
      brand: 'Unknown',
      status: 'Danger',
    },
    {
      id: 3,
      sourceUrl: 'https://www.wps.com/1h3clickids:542...',
      ipAddress: '3.175.34.128',
      hostingProvider: '--',
      source: 'Bulk Scan',
      date: '15 December, 2021',
      brand: 'Unknown',
      status: 'Clean',
    },
    {
      id: 4,
      sourceUrl: 'https://chatgpt.com/c/686590c1-9ef...',
      ipAddress: '104.21.45.186',
      hostingProvider: 'Cloudflare, Inc',
      source: 'Bulk Scan',
      date: '14 November, 2021',
      brand: 'Unknown',
      status: 'Pending',
    },
    {
      id: 5,
      sourceUrl: 'https://www.freepik.com/search?col...',
      ipAddress: '190.115.41.182',
      hostingProvider: '--',
      source: 'Bulk Scan',
      date: '15 October, 2021',
      brand: 'Unknown',
      status: 'Clean',
    },
  ];

  const handleScanUrl = () => {
    if (urlToScan.trim()) {
      console.log('Scanning URL:', urlToScan);

      //  Navigate to phlink.jsx and start Stage 1 at 0%
      navigate("/phlink", { 
        state: { 
          url: urlToScan,
          stage1Progress: 0, // Start Stage 1 animation from 0%
          stage2Progress: 0, // Stage 2 initial state
          stage3Progress: 0  // Stage 3 initial state
        } 
      });

      setUrlToScan(''); // Clear input after scan
    } else {
      alert('Please enter a URL to scan.');
    }
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
            </li>

            <li  className="ml-2">URL Scanner</li>
          </ol>
        </nav>

        {/* Scan URLs Section */}
        <section className="p-6 mb-8 bg-white shadow-md rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-800">Scan URLs</h2>
              <p className="text-sm text-gray-500">
                A real-time URL scanner that provides detailed threat intelligence.
              </p>
            </div>
            <button className="p-2 text-blue-500 transition duration-150 rounded-full hover:bg-blue-50">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9.228a4.5 4.5 0 116.364 0M12 14v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </button>
          </div>

          <div className="flex flex-col items-center justify-center mb-6 space-y-4 sm:flex-row sm:justify-start sm:space-y-0 sm:space-x-4">
            <button className="flex items-center px-4 py-2 space-x-2 text-blue-600 transition duration-150 bg-blue-100 rounded-lg hover:bg-blue-200">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-.758l3.67-3.67m-9.106 10.61a4 4 0 010-5.656l4-4a4 4 0 015.656 0"></path></svg>
              <span>Phishing Link (URL) Checker</span>
            </button>
            <span className="text-sm text-gray-500">240 Links Scanned</span>
          </div>

          {/* URL Input and Scan Button */}
          <div className="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
            <input
              type="text"
              placeholder="Search or scan a URL"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={urlToScan}
              onChange={(e) => setUrlToScan(e.target.value)}
            />
            <button
              onClick={handleScanUrl}
              className="px-6 py-3 text-white transition duration-150 bg-blue-600 rounded-lg shadow-md hover:bg-blue-700"
            >
              Scan
            </button>
          </div>
        </section>

        {/* My URL Scans Table Section */}
        <section className="p-6 bg-white shadow-md rounded-xl">
          <div className="flex flex-col items-start justify-between mb-4 sm:flex-row sm:items-center">
            <h2 className="mb-3 text-lg font-semibold text-gray-800 sm:mb-0">My URL Scans</h2>
            <div className="flex items-center space-x-2 text-sm">
              <select className="px-2 py-1 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
                <option>Apr 07, 2025 - Jul 06, 2025</option>
                <option>Last 30 Days</option>
                <option>Last 90 Days</option>
              </select>
              <button className="p-2 text-gray-600 transition duration-150 rounded-md hover:bg-gray-100">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
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
                {mockUrlScans.map((scan) => (
                  <tr key={scan.id}>
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
                        ${scan.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' : ''}
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

export default Urls;
