import React, { useState } from 'react';
import { Link } from "react-router-dom";
import { FaWhatsapp,  FaChrome, FaEnvelope, FaCommentAlt  } from "react-icons/fa";
import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

const Reports = () => {
  // Mock data for the reports
  const mockMetrics = [
    { title: 'Threats Blocked', value: '247', color: 'bg-red-500', icon: (
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 18.364A9 9 0 0012 3a9 9 0 00-6.364 15.364M12 10v4m0 0l-2-2m2 2l2-2"></path></svg>
      )},
    { title: 'Links Scanned', value: '1,429', color: 'bg-blue-500', icon: (
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-.758l3.67-3.67m-9.106 10.61a4 4 0 010-5.656l4-4a4 4 0 015.656 0"></path></svg>
      )},
    { title: 'Files Quarantined', value: '18', color: 'bg-yellow-500', icon: (
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
      )},
    { title: 'Safe Actions', value: '98.2%', color: 'bg-green-500', icon: (
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.001 12.001 0 002 12c0 2.757 1.299 5.232 3.365 6.931l1.624 1.625a1 1 0 00.707.293h7.408a1 1 0 00.707-.293l1.624-1.625C20.701 17.232 22 14.757 22 12c0-2.091-.707-4.016-1.977-5.556z"></path></svg>
      )},
  ];

  // Mock data for recent activity table
  const mockRecentActivity = [
  {
    timestamp: 'Today, 2:34 PM',
    sourceIcon: (
      <FaWhatsapp className="w-5 h-5 text-green-500" style={{ minWidth: '20px', minHeight: '20px' }} />
    ),
    source: 'WhatsApp',
    type: 'Phishing Link',
    threat: 'bit.ly/fake-bank...',
    action: 'Blocked',
    status: 'High Risk',
    statusColor: 'bg-red-100 text-red-800',
  },
  {
    timestamp: 'Today, 1:15 PM',
    sourceIcon: (
      <FaEnvelope className="w-5 h-5 text-blue-500" style={{ minWidth: '20px', minHeight: '20px' }} />
    ),
    source: 'Email',
    type: 'Malicious File',
    threat: 'invoice.pdf.exe',
    action: 'Quarantined',
    status: 'Critical',
    statusColor: 'bg-red-100 text-red-800',
  },
  {
    timestamp: 'Today, 11:42 AM',
    sourceIcon: (
      <FaCommentAlt className="w-5 h-5 text-gray-500" style={{ minWidth: '20px', minHeight: '20px' }} />
    ),
    source: 'SMS',
    type: 'Suspicious URL',
    threat: 'tinylurl.com/prize...',
    action: 'Blocked',
    status: 'Medium Risk',
    statusColor: 'bg-yellow-100 text-yellow-800',
  },
  {
    timestamp: 'Yesterday, 4:22 PM',
    sourceIcon: (
      <FaChrome className="w-5 h-5 text-purple-500" style={{ minWidth: '20px', minHeight: '20px' }} />
    ),
    source: 'Browser',
    type: 'Safe Link',
    threat: 'amazon.com/deals',
    action: 'Allowed',
    status: 'Safe',
    statusColor: 'bg-green-100 text-green-800',
  },
];


  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 4; // As per the image, showing 4 results

  const totalPages = Math.ceil(mockRecentActivity.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentActivity = mockRecentActivity.slice(startIndex, endIndex);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
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

            <li className="ml-2">Security Reports</li>

          </ol>
        </nav>

        {/* Security Reports Header and Actions */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Security Reports</h1>
            <p className="text-gray-600 text-sm">Monitor threats and protection activity</p>
          </div>
          <div className="flex space-x-3 mt-4 sm:mt-0">
            <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 flex items-center space-x-2 hover:bg-gray-50 transition duration-150 shadow-sm">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-2-2m2 2l2-2m-6 9H6a2 2 0 01-2-2V7a2 2 0 012-2h10a2 2 0 012 2v3m-4 3l-4 4m-4 0h8"></path></svg>
              <span>Export</span>
            </button>
            <button className="px-4 py-2 bg-red-500 text-white rounded-lg flex items-center space-x-2 hover:bg-red-600 transition duration-150 shadow-sm">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004 12v.621c0 2.4 1.383 4.477 3.365 5.542A9.957 9.957 0 0012 21c4.418 0 8-3.582 8-8V9.414A1.99 1.99 0 0018.586 8H15m-2.5 0h-3.879a1 1 0 00-.707.293l-2.414 2.414A1 1 0 006.25 12H4"></path></svg>
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {mockMetrics.map((metric, index) => (
            <div key={index} className={`rounded-xl p-6 text-white flex flex-col items-start justify-between ${metric.color} shadow-md`}>
              <div className="flex items-center justify-between w-full mb-4">
                <h3 className="text-sm font-medium">{metric.title}</h3>
                {metric.icon}
              </div>
              <p className="text-4xl font-bold">{metric.value}</p>
            </div>
          ))}
        </div>

        {/* Filters and Search */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8 flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4">
          <select className="flex-1 w-full sm:w-auto border border-gray-300 rounded-lg py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            <option>All Sources</option>
            <option>WhatsApp</option>
            <option>Email</option>
            <option>SMS</option>
            <option>Browser</option>
          </select>
          <select className="flex-1 w-full sm:w-auto border border-gray-300 rounded-lg py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            <option>All Types</option>
            <option>Phishing Link</option>
            <option>Malicious File</option>
            <option>Suspicious URL</option>
            <option>Safe Link</option>
          </select>
          <select className="flex-1 w-full sm:w-auto border border-gray-300 rounded-lg py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            <option>Last 7 days</option>
            <option>Last 30 days</option>
            <option>Last 90 days</option>
            <option>All Time</option>
          </select>
          <input
            type="text"
            placeholder="Search reports..."
            className="flex-2 w-full sm:w-auto border border-gray-300 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Recent Activity Table */}
        <section className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Threat
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Action
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Details
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {currentActivity.map((activity, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {activity.timestamp}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 flex items-center space-x-2">
                      {activity.sourceIcon}
                      <span>{activity.source}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {activity.type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {activity.threat}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {activity.action}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${activity.statusColor}`}>
                        {activity.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <a href="Reports" className="text-blue-600 hover:underline">View Details</a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-6">
            <div className="text-sm text-gray-700">
              Showing {startIndex + 1} to {Math.min(endIndex, mockRecentActivity.length)} of {mockRecentActivity.length} results
            </div>
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              {[...Array(totalPages)].map((_, i) => (
                <button
                  key={i + 1}
                  onClick={() => handlePageChange(i + 1)}
                  className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium
                    ${currentPage === i + 1 ? 'z-10 bg-blue-50 border-blue-500 text-blue-600' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'}
                  `}
                >
                  {i + 1}
                </button>
              ))}
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </nav>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Reports;
