import React, { useState } from "react";
//import { Link } from "react-router-dom";
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
  Legend,
} from "recharts";

// Mock data
const mockData = {
  metrics: [
    { title: "Threats Blocked", value: "1,247", color: "bg-red-500" },
    { title: "Links Analyzed", value: "45,892", color: "bg-blue-500" },
    { title: "Files Scanned", value: "12,456", color: "bg-green-500" },
    { title: "Protected Users", value: "2,847", color: "bg-purple-500" },
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

const Dashboard = () => {
  const [activeTimeFilter, setActiveTimeFilter] = useState("12 Months");

  return (
    <div className="flex min-h-screen bg-gray-100 font-inter">
        <Sidebar />
      

      {/* Main Content */}
      <main className="flex-1 lg:ml-64 p-6">
         <Topbar />
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">
          Hey Mariana - How can we help you today?
        </h1>

        {/* Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {mockData.metrics.map((metric, idx) => (
            <div
              key={idx}
              className={`p-6 rounded-xl shadow-md text-white ${metric.color}`}
            >
              <h3 className="text-sm font-medium">{metric.title}</h3>
              <p className="text-4xl font-bold mt-2">{metric.value}</p>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Phishing Report */}
          <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-800">
                Phishing Report
              </h2>
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
              </div>
            </div>
            <ResponsiveContainer width="100%" height={250}>
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
          </div>

          {/* Threat Analysis */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Threat Analysis
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={mockData.threatAnalysis}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#3B82F6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
