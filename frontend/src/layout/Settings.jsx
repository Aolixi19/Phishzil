import React, { useState } from "react";
import { Mail, MessageSquare, Bell } from "lucide-react";
import { FaWhatsapp } from "react-icons/fa";


import { NavLink } from "react-router-dom";
import Topbar from "../types/Topbar";
import Sidebar from "../types/Sidebar";

const Settings = () => {
  // State for each toggle switch and dropdown
  const [realTimeProtection, setRealTimeProtection] = useState(true);
  const [autoUpdate, setAutoUpdate] = useState(true);
  const [offlineMode, setOfflineMode] = useState(false);
  const [protectionLevel, setProtectionLevel] = useState("High (Recommended)");
  const [urlRewriting, setUrlRewriting] = useState(true);
  const [safeViewSandbox, setSafeViewSandbox] = useState(true);
  const [macroScrubbing, setMacroScrubbing] = useState(true);
  const [executableGuard, setExecutableGuard] = useState(true);
  const [archiveScanner, setArchiveScanner] = useState(true);
  const [monitorEmail, setMonitorEmail] = useState(true);
  const [monitorSMS, setMonitorSMS] = useState(true);
  const [monitorWhatsApp, setMonitorWhatsApp] = useState(true);
  const [systemNotifications, setSystemNotifications] = useState(true);
  const [smsTextMessages, setSmsTextMessages] = useState(true);
  const [emailClients, setEmailClients] = useState(true);
  const [messagingApps, setMessagingApps] = useState(true);
  const [systemLevelNotifications, setSystemLevelNotifications] = useState(true);

  const ToggleSwitch = ({ label, description, checked, onChange }) => {
    // Generate a safe ID - use label text if string, otherwise generate random ID
    const id = typeof label === 'string' 
      ? `toggle-${label.replace(/\s+/g, '-').toLowerCase()}`
      : `toggle-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className="flex items-center justify-between py-3 border-b border-gray-200 last:border-b-0">
        <div>
          {typeof label === 'string' ? (
            <p className="font-medium text-gray-800">{label}</p>
          ) : (
            <div className="font-medium text-gray-800">{label}</div>
          )}
          {description && (
            <p className="text-sm text-gray-500">{description}</p>
          )}
        </div>
        <label htmlFor={id} className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            id={id}
            className="sr-only peer"
            checked={checked}
            onChange={onChange}
          />
          <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:bg-blue-600 transition-colors duration-200">
            <div className="absolute top-[2px] left-[2px] bg-white border border-gray-300 rounded-full h-5 w-5 transition-transform duration-200 peer-checked:translate-x-5"></div>
          </div>
        </label>
      </div>
    );
  };

  const handleResetToDefault = () => {
    setRealTimeProtection(true);
    setAutoUpdate(true);
    setOfflineMode(false);
    setProtectionLevel("High (Recommended)");
    setUrlRewriting(true);
    setSafeViewSandbox(true);
    setMacroScrubbing(true);
    setExecutableGuard(true);
    setArchiveScanner(true);
    setMonitorEmail(true);
    setMonitorSMS(true);
    setMonitorWhatsApp(true);
    setSystemNotifications(true);
    setSmsTextMessages(true);
    setEmailClients(true);
    setMessagingApps(true);
    setSystemLevelNotifications(true);
    alert("Settings reset to default!");
  };

  const handleSaveChanges = () => {
    const settings = {
      realTimeProtection,
      autoUpdate,
      offlineMode,
      protectionLevel,
      urlRewriting,
      safeViewSandbox,
      macroScrubbing,
      executableGuard,
      archiveScanner,
      monitorEmail,
      monitorSMS,
      monitorWhatsApp,
      systemNotifications,
      smsTextMessages,
      emailClients,
      messagingApps,
      systemLevelNotifications,
    };
    console.log("Saving settings:", settings);
    alert("Settings saved successfully!");
  };

  return (
    <div className="flex min-h-screen bg-gray-100 font-inter">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 p-4 lg:ml-64 sm:p-6 lg:p-8">
        {/* Top Bar */}
        <Topbar />

        {/* Settings Header */}
        <div className="flex flex-col items-start justify-between mb-6 sm:flex-row sm:items-center">
          <div>
            <h1 className="mb-4 text-4xl font-bold text-gray-900">Settings</h1>
            <p className="text-base text-gray-600">
              Configure your PhishZil™ protection settings and preferences
            </p>
          </div>
        </div>

        {/* Settings Tabs */}
        <div className="mb-8 border-b border-gray-200">
          <nav className="flex -mb-px space-x-12" aria-label="Tabs">
            <NavLink
              to="/settings/general"
              className={({ isActive }) =>
                isActive
                  ? "border-b-4 border-blue-500 text-blue-600 px-1 pb-4 text-xl font-bold"
                  : "border-b-4 border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 px-1 pb-4 text-xl font-bold"
              }
            >
              General
            </NavLink>
            <NavLink
              to="/settings/protection"
              className={({ isActive }) =>
                isActive
                  ? "border-b-4 border-blue-500 text-blue-600 px-1 pb-4 text-xl font-bold"
                  : "border-b-4 border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 px-1 pb-4 text-xl font-bold"
              }
            >
              Protection
            </NavLink>
            <NavLink
              to="/settings/notifications"
              className={({ isActive }) =>
                isActive
                  ? "border-b-4 border-blue-500 text-blue-600 px-1 pb-4 text-xl font-bold"
                  : "border-b-4 border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 px-1 pb-4 text-xl font-bold"
              }
            >
              Notifications
            </NavLink>
            <NavLink
              to="/settings/advanced"
              className={({ isActive }) =>
                isActive
                  ? "border-b-4 border-blue-500 text-blue-600 px-1 pb-4 text-xl font-bold"
                  : "border-b-4 border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 px-1 pb-4 text-xl font-bold"
              }
            >
              Advanced
            </NavLink>
          </nav>
        </div>

        {/* Settings Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-8">
          {/* General Settings */}
          <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-md">
            <h3 className="mb-4 text-lg font-semibold text-gray-800">
              General Settings
            </h3>
            <div className="space-y-4">
              <ToggleSwitch
                label="Real-time Protection"
                description="Enable continuous monitoring"
                checked={realTimeProtection}
                onChange={() => setRealTimeProtection(!realTimeProtection)}
              />
              <ToggleSwitch
                label="Auto-Update"
                description="Automatic threat signature updates"
                checked={autoUpdate}
                onChange={() => setAutoUpdate(!autoUpdate)}
              />
              <ToggleSwitch
                label="Offline Mode"
                description="Enable offline threat detection"
                checked={offlineMode}
                onChange={() => setOfflineMode(!offlineMode)}
              />
            </div>
          </div>

          {/* Link Protection */}
          <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-md">
            <h3 className="mb-4 text-lg font-semibold text-gray-800">
              Link Protection
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b border-gray-200">
                <p className="font-medium text-gray-800">Protection Level</p>
                <select
                  className="px-2 py-1 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  value={protectionLevel}
                  onChange={(e) => setProtectionLevel(e.target.value)}
                >
                  <option>High (Recommended)</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>
              </div>
              <ToggleSwitch
                label="URL Rewriting"
                description="Automatically disarm malicious links"
                checked={urlRewriting}
                onChange={() => setUrlRewriting(!urlRewriting)}
              />
              <ToggleSwitch
                label="SafeView Sandbox"
                description="Open suspicious links in sandbox"
                checked={safeViewSandbox}
                onChange={() => setSafeViewSandbox(!safeViewSandbox)}
              />
            </div>
          </div>

          {/* Attachment Protection */}
          <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-md">
            <h3 className="mb-4 text-lg font-semibold text-gray-800">
              Attachment Protection
            </h3>
            <div className="space-y-4">
              <ToggleSwitch
                label="Macro Scrubbing"
                description="Remove dangerous macros from files"
                checked={macroScrubbing}
                onChange={() => setMacroScrubbing(!macroScrubbing)}
              />
              <ToggleSwitch
                label="Executable Guard"
                description="Block risky executable files"
                checked={executableGuard}
                onChange={() => setExecutableGuard(!executableGuard)}
              />
              <ToggleSwitch
                label="Archive Scanner"
                description="Scan ZIP/RAR contents automatically"
                checked={archiveScanner}
                onChange={() => setArchiveScanner(!archiveScanner)}
              />
            </div>
          </div>

          {/* Monitoring Sources */}
          <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-md">
            <h3 className="mb-4 text-lg font-semibold text-gray-800">
              Monitoring Sources
            </h3>
            <div className="space-y-4">
              <ToggleSwitch
                label={
                  <span className="flex items-center gap-2">
                    <Mail className="w-5 h-5 text-gray-600" /> Email
                  </span>
                }
                checked={monitorEmail}
                onChange={() => setMonitorEmail(!monitorEmail)}
              />
              <ToggleSwitch
                label={
                  <span className="flex items-center gap-2">
                    <MessageSquare className="w-5 h-5 text-gray-600" /> SMS
                  </span>
                }
                checked={monitorSMS}
                onChange={() => setMonitorSMS(!monitorSMS)}
              />
              <ToggleSwitch
                label={
                  <span className="flex items-center gap-2">
                    <FaWhatsapp className="w-5 h-5 text-green-500" /> WhatsApp

                  </span>
                }
                checked={monitorWhatsApp}
                onChange={() => setMonitorWhatsApp(!monitorWhatsApp)}
              />
              <ToggleSwitch
                label={
                  <span className="flex items-center gap-2">
                    <Bell className="w-5 h-5 text-gray-600" /> System Notifications
                  </span>
                }
                checked={systemNotifications}
                onChange={() => setSystemNotifications(!systemNotifications)}
              />
            </div>
          </div>
        </div>

        {/* Link Interception & System Notifications Section */}
        <section className="p-6 mt-8 mb-8 bg-white shadow-md rounded-xl">
         

          {/* Link Interception Engine */}
          <div className="mb-6">
            <h4 className="mb-2 font-semibold text-gray-700">Link Interception Engine</h4>
            <div className="space-y-4">
              <ToggleSwitch
                label="SMS/Text Messages"
                description="Monitor links in text messages"
                checked={smsTextMessages}
                onChange={() => setSmsTextMessages(!smsTextMessages)}
              />
              <ToggleSwitch
                label="Email Clients"
                description="Scan email links and attachments"
                checked={emailClients}
                onChange={() => setEmailClients(!emailClients)}
              />
              <ToggleSwitch
                label="Messaging Apps"
                description="WhatsApp, Telegram, Signal"
                checked={messagingApps}
                onChange={() => setMessagingApps(!messagingApps)}
              />
            </div>
          </div>

          {/* System Notifications */}
          <div>
            <h4 className="mb-2 font-semibold text-gray-700">System Notifications</h4>
            <div className="space-y-4">
              <ToggleSwitch
                label="Monitor system-level notifications"
                checked={systemLevelNotifications}
                onChange={() => setSystemLevelNotifications(!systemLevelNotifications)}
              />
            </div>
          </div>
        </section>

        {/* Action Buttons */}
        <div className="flex justify-end mt-8 space-x-4">
          <button
            onClick={handleResetToDefault}
            className="px-6 py-3 text-gray-700 transition duration-150 border border-gray-300 rounded-lg hover:bg-gray-100"
          >
            Reset to Default
          </button>
          <button
            onClick={handleSaveChanges}
            className="px-6 py-3 text-white transition duration-150 bg-blue-600 rounded-lg shadow-md hover:bg-blue-700"
          >
            Save Changes
          </button>
        </div>
      </main>
    </div>
  );
};

export default Settings;