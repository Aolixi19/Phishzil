import React, { useState } from "react";
import Topbar from "../../types/Topbar";
import Sidebar from "../../types/Sidebar";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  BarChart,
  Bar,
} from "recharts";

import {
  Flag,
  Link as LinkIcon,
  FileText,
  Users,
  AlertTriangle,
} from "lucide-react";

// Main App Component
const Dashboard = () => {
  const [activeMenu, setActiveMenu] = useState("Dashboard");
  const [activeTimeFilter, setActiveTimeFilter] = useState("12 Months");

  // Data
  const mockData = {
    metrics: [
      { title: "Threats Blocked", value: "1,247", color: "bg-red-500", icon: <Flag /> },
      { title: "Links Analyzed", value: "45,892", color: "bg-blue-500", icon: <LinkIcon /> },
      { title: "Files Scanned", value: "12,456", color: "bg-green-500", icon: <FileText /> },
      { title: "Protected Users", value: "2,847", color: "bg-purple-500", icon: <Users /> },
    ],
    phishingReport: [
      { month: "Feb", value: 20 },
      { month: "Mar", value: 35 },
      { month: "Apr", value: 40 },
      { month: "May", value: 30 },
      { month: "Jun", value: 45 },
      { month: "Jul", value: 38 },
      { month: "Aug", value: 50 },
      { month: "Sep", value: 42 },
      { month: "Oct", value: 55 },
      { month: "Nov", value: 48 },
      { month: "Dec", value: 60 },
      { month: "Jan", value: 52 },
    ],
    threatSources: [
      { name: "URL Links", value: 143382 },
      { name: "Emails", value: 87974 },
      { name: "Files Scanned", value: 45211 },
      { name: "Whatsapp", value: 21893 },
    ],
    threatAnalysis: [
      { day: "Mon", value: 30 },
      { day: "Tue", value: 50 },
      { day: "Wed", value: 40 },
      { day: "Thu", value: 70 },
      { day: "Fri", value: 80 },
      { day: "Sat", value: 55 },
      { day: "Sun", value: 60 },
    ],
  };

  // Stat card
  const StatCard = ({ title, value, color, icon }) => (
    <div className={`flex items-center justify-between p-6 rounded-2xl text-white shadow-lg ${color}`}>
      <div>
        <h3 className="mb-1 text-sm font-medium">{title}</h3>
        <p className="text-3xl font-bold">{value}</p>
      </div>
      {icon}
    </div>
  );

  // Main content switch
  const renderContent = () => {
    switch (activeMenu) {
      case "Dashboard":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-900">
              Hey Mariana - How can we help you today?
            </h1>

            {/* Metrics */}
            <div className="grid grid-cols-1 gap-6 mb-8 sm:grid-cols-2 lg:grid-cols-4">
              {mockData.metrics.map((metric, idx) => (
                <StatCard key={idx} {...metric} />
              ))}
            </div>

            {/* Charts + panels */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              {/* Phishing Report */}
              <div className="p-6 bg-white shadow-md lg:col-span-2 rounded-xl">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-800">Phishing Report</h2>
                  <div className="flex space-x-2 text-sm">
                    {["12 Months", "6 Months", "30 Days", "7 Days"].map((filter) => (
                      <button
                        key={filter}
                        onClick={() => setActiveTimeFilter(filter)}
                        className={`px-3 py-1 rounded-md ${
                          activeTimeFilter === filter
                            ? "bg-gray-200 text-gray-800"
                            : "text-gray-600 hover:bg-gray-100"
                        }`}
                      >
                        {filter}
                      </button>
                    ))}
                    <button className="flex items-center px-3 py-1 space-x-1 text-gray-600 bg-gray-100 rounded-md">
                      <FileText size={16} />
                      <span>Export PDF</span>
                    </button>
                  </div>
                </div>
                <div className="relative h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={mockData.phishingReport}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#6366F1"
                        strokeWidth={2}
                        dot={{ r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                  <div className="absolute text-sm text-center text-gray-400 transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
                    June 2021 <br /> 45 Phishing link blocked
                  </div>
                </div>
              </div>

              {/* Recent Threats */}
              <div className="p-6 bg-white shadow-md rounded-xl">
                <h2 className="mb-4 text-lg font-semibold text-gray-800">Recent Threats</h2>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                    <div className="flex items-center space-x-3">
                      <AlertTriangle />
                      <div>
                        <p className="font-semibold text-gray-800">Phishing Email</p>
                        <p className="text-sm text-gray-500">suspicious-bank-link.com</p>
                      </div>
                    </div>
                    <span className="px-2 py-1 text-xs font-medium text-red-700 bg-red-100 rounded-full">Blocked</span>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                    <div className="flex items-center space-x-3">
                      <FileText />
                      <div>
                        <p className="font-semibold text-gray-800">Malicious PDF</p>
                        <p className="text-sm text-gray-500">invoice.pdf</p>
                      </div>
                    </div>
                    <span className="px-2 py-1 text-xs font-medium text-yellow-700 bg-yellow-100 rounded-full">Quarantined</span>
                  </div>
                </div>
              </div>

              {/* Threat Sources */}
              <div className="p-6 bg-white shadow-md lg:col-span-2 rounded-xl">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-700">Threat Sources</h2>
                  <button className="px-3 py-1 text-sm text-gray-500 bg-gray-100 rounded-md">Last 7 Days</button>
                </div>
                <ul className="space-y-4">
                  {mockData.threatSources.map((item, index) => (
                    <li key={index}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-gray-700">{item.name}</span>
                        <span className="text-sm text-gray-500">{item.value.toLocaleString()}</span>
                      </div>
                      <div className="w-full h-2 bg-gray-200 rounded-full">
                        <div
                          className="h-2 bg-blue-500 rounded-full"
                          style={{ width: `${(item.value / mockData.threatSources[0].value) * 100}%` }}
                        ></div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Threat Analysis */}
              <div className="p-6 bg-white shadow-md rounded-xl">
                <h2 className="mb-4 text-lg font-semibold text-gray-700">Threat Analysis</h2>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={mockData.threatAnalysis}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#3B82F6" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        );

      case "URL Scanner":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-800">URL Scanner</h1>
            <div className="flex flex-col items-center justify-center p-12 space-y-4 bg-white shadow-md rounded-xl">
              <svg className="w-20 h-20 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
              </svg>
              <h2 className="text-xl font-semibold text-gray-700">Scan a URL for threats</h2>
              <p className="max-w-lg text-center text-gray-500">
                Enter a URL below to scan it for malicious links, phishing attempts, and other security threats.
              </p>
              <div className="flex items-center w-full max-w-xl space-x-2">
                <input
                  type="text"
                  placeholder="Paste URL here..."
                  className="flex-1 px-4 py-3 text-gray-700 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button className="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
                  Scan
                </button>
              </div>
            </div>
          </div>
        );

      case "Email Scanner":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-800">Email Scanner</h1>
            <div className="flex flex-col items-center justify-center p-12 space-y-4 bg-white shadow-md rounded-xl">
              <svg className="w-20 h-20 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
              <h2 className="text-xl font-semibold text-gray-700">Scan an email for threats</h2>
              <textarea
                placeholder="Paste email content here..."
                className="w-full h-48 max-w-xl px-4 py-3 text-gray-700 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              ></textarea>
              <button className="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
                Scan Email
              </button>
            </div>
          </div>
        );

      case "File Scanner":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-800">File Scanner</h1>
            <div className="flex flex-col items-center justify-center p-12 space-y-4 bg-white shadow-md rounded-xl">
              <svg className="w-20 h-20 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <h2 className="text-xl font-semibold text-gray-700">Scan a file for viruses and malware</h2>
              <div className="w-full max-w-xl p-6 text-center border-2 border-gray-300 border-dashed rounded-lg cursor-pointer hover:border-blue-500">
                <p className="text-gray-500">Drag and drop your file here, or click to browse</p>
                <input type="file" className="hidden" id="file-upload" />
              </div>
              <button className="px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
                Upload and Scan
              </button>
            </div>
          </div>
        );

      case "Reports":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-800">Threat Reports</h1>
            <div className="flex flex-col p-6 bg-white shadow-md rounded-xl">
              <p className="text-gray-500">Detailed reports of all scans and threats will be displayed here.</p>
            </div>
          </div>
        );

      case "Tickets":
        return (
          <div className="p-8">
            <h1 className="mb-6 text-2xl font-semibold text-gray-800">Support Tickets</h1>
            <div className="flex flex-col p-6 bg-white shadow-md rounded-xl">
              <p className="text-gray-500">Your support tickets will be listed here.</p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
  <div className="flex min-h-screen text-gray-800 bg-gray-100 font-inter">
    {/* Sidebar fixed width */}
    <div className="w-64">
      <Sidebar activeMenu={activeMenu} setActiveMenu={setActiveMenu} />
    </div>

    {/* Main area (Topbar + Content) */}
    <div className="flex-1 flex flex-col">
      {/* Topbar always on top */}
      <Topbar />

      {/* Page Content aligned below Topbar */}
      <div className="flex-1 p-6 overflow-auto">
        {renderContent()}
      </div>
    </div>
  </div>
);

};

export default Dashboard;
