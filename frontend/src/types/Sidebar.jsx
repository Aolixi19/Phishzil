

import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white shadow-lg p-6 flex-shrink-0 flex flex-col justify-between fixed h-full overflow-y-auto z-20">
      <div>
        {/* Logo */}
        <div className="flex items-center mb-8">
          <img
            src="https://placehold.co/32x32/3B82F6/FFFFFF?text=P"
            alt="PhishZil Logo"
            className="w-8 h-8 mr-2 rounded-md"
          />
          <span className="text-xl font-bold text-blue-600">PhishZil™</span>
        </div>

        {/* Button */}
        <button className="w-full bg-blue-600 text-white py-3 rounded-lg flex items-center justify-center space-x-2 mb-6 hover:bg-blue-700 transition duration-150 shadow-md">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          <span>Connect New Account</span>
        </button>

        {/* Navigation */}
        <nav className="space-y-2">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m0 0l7 7 7-7M19 10v10a1 1 0 01-1 1h-3m-7 0h-2a1 1 0 01-1-1V7a1 1 0 011-1h2a1 1 0 011 1v10zm-2 0h-2a1 1 0 01-1-1V7a1 1 0 011-1h2a1 1 0 011 1v10z"
              />
            </svg>
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/safe-view"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.001 12.001 0 002 12c0 2.757 1.299 5.232 3.365 6.931l1.624 1.625a1 1 0 00.707.293h7.408a1 1 0 00.707-.293l1.624-1.625C20.701 17.232 22 14.757 22 12c0-2.091-.707-4.016-1.977-5.556z"
              />
            </svg>
            <span>Safe View Scanner</span>
          </NavLink>

          <NavLink
            to="/url-scanner"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-.758l3.67-3.67m-9.106 10.61a4 4 0 010-5.656l4-4a4 4 0 015.656 0"
              />
            </svg>
            <span>URL Scanner</span>
          </NavLink>

          <NavLink
            to="/email-scanner"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8m-9 13h9A2 2 0 0021 19V5a2 2 0 00-2-2H3a2 2 0 00-2 2v14a2 2 0 002 2z"
              />
            </svg>
            <span>Email Scanner</span>
            <span className="ml-auto bg-blue-100 text-blue-600 text-xs font-medium px-2 py-0.5 rounded-full">
              NEW
            </span>
          </NavLink>

          <NavLink
            to="/file-scanner"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>File Scanner</span>
          </NavLink>

          <NavLink
            to="/reports"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M18 12h.01"
              />
            </svg>
            <span>Reports</span>
          </NavLink>
        </nav>

        {/* Support */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            SUPPORT
          </h3>
          <NavLink
            to="/tickets"
            className={({ isActive }) =>
              `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
                isActive
                  ? "text-blue-600 bg-blue-50 font-semibold"
                  : "text-gray-700 hover:bg-gray-50"
              }`
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M8.228 9.228a4.5 4.5 0 116.364 0M12 14v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>Tickets</span>
            <span className="ml-auto bg-gray-200 text-gray-700 text-xs font-medium px-2 py-0.5 rounded-full">
              15
            </span>
          </NavLink>
        </div>
      </div>

      <div className="mt-96"></div>

      {/* Settings + Logout */}
      <div className="pt-6 border-t border-gray-200">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
              isActive
                ? "text-blue-600 bg-blue-50 font-semibold"
                : "text-gray-700 hover:bg-gray-50"
            }`
          }
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span>Settings</span>
        </NavLink>

        <NavLink
          to="/logout"
          className={({ isActive }) =>
            `flex items-center space-x-3 p-3 rounded-lg transition duration-150 ${
              isActive
                ? "text-blue-600 bg-blue-50 font-semibold"
                : "text-gray-700 hover:bg-gray-50"
            }`
          }
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span>Logout</span>
        </NavLink>
      </div>
    </aside>
  );
}