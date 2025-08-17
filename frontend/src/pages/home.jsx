import React from "react";
import { Link } from "react-router-dom";


import blockImg from "../assets/block.png";
import penImg from "../assets/pen.png";
import wifiImg from "../assets/wifi.png";
import divImg from "../assets/div.png";
import dangerImg from "../assets/danger.png";
import boxImg from "../assets/box.png";
import chainImg from "../assets/chain.png";
import phoneImg from "../assets/phone.png";
import laptopImg from "../assets/laptop.png";
import appleImg from "../assets/apple.png";
import browserImg from "../assets/browser.png";
import containerImg from "../assets/container.png";
import tombImg from "../assets/tomb.png";
import correctImg from "../assets/correct.png";
import profileImg from "../assets/profile.png";




function App() {
  return (
    <div className="font-sans text-gray-800">
      {/* Navbar */}
      <header className="flex justify-between items-center px-10 py-5 bg-white shadow-md">
        <h1 className="text-xl font-bold text-blue-600">Phishzil™</h1>
        <nav className="hidden md:flex space-x-6 text-gray-600 font-medium">
        <a href="#features" className="hover:text-blue-600">Features</a>
        <a href="#architecture" className="hover:text-blue-600">Plateforms</a>
        <Link to="/dashboard" className="hover:text-blue-600">
          Dashboard
        </Link>
        <a href="#pricing" className="hover:text-blue-600">Pricing</a>
        </nav>

        <Link
          to="/signup"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 inline-block"
>
           Get Started
        </Link>
      </header>

      {/* Hero Section */}
    <section className="bg-gradient-to-r from-blue-900 to-blue-600 text-white py-20 px-10">
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-10 items-center">
    
        {/* Left: Text */}
      <div className="text-left">
      <h2 className="text-4xl md:text-5xl font-bold mb-6">
        Real-time AI <br />
        <span className="text-green-400">Phishing</span> Protection
      </h2>

      <p className="max-w-2xl mb-8 text-lg text-gray-200">
        Intercept, detect, and neutralize phishing links and <br />
        malicious attachments across all digital platforms with our <br />
        decentralized AI-powered cybersecurity system.
      </p>

      <div className="flex flex-wrap gap-4">
        {/* ✅ Updated to Link */}
        <Link
          to="/signup"
          className="bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-400 transition"
        >
          Start Free Trial
        </Link>
        <Link
          to="/demo"
          className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Admin Demo
        </Link>
      </div>
    </div>

    {/* Right: Image */}
    <div className="flex justify-center md:justify-end">
      <img 
        src={blockImg} 
        alt="Phishing Protection" 
        className="w-80 md:w-[400px] lg:w-[500px]"
      />
    </div>

  </div>
</section>



      {/* Stats Section */}
<section className="py-16 text-center">
  <h3 className="text-2xl font-semibold mb-4">
    Unleash the full power of Phishzil
  </h3>
  <p className="text-gray-600 mb-10 max-w-2xl mx-auto">
    Everything you need to protect yourself online from phishing attacks is here.
  </p>

  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
    <div>
      <p className="text-3xl font-bold text-blue-600">99.9%</p>
      <p className="text-gray-600">Phish Detection Rate</p>
    </div>
    <div>
      <p className="text-3xl font-bold text-blue-600">50M+</p>
      <p className="text-gray-600">Links Analyzed Daily</p>
    </div>
    <div>
      <p className="text-3xl font-bold text-blue-600">100K+</p>
      <p className="text-gray-600">Processed Emails</p>
    </div>
  </div>
</section>

      {/* Core Protection Modules */}
<section id="features" className="py-20 bg-gray-50 text-center">
  <h2 className="text-blue-600 font-semibold uppercase tracking-wide mb-4">
    Features
  </h2>
  <h3 className="text-3xl font-bold mb-6">Core Protection Modules</h3>
  <p className="text-gray-600 max-w-2xl mx-auto mb-12">
    Advanced AI-powered modules working together to provide comprehensive phishing protection.
  </p>

  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
    {[
      { img: chainImg, title: "Link Interception Engine", desc: "Detects and blocks malicious links before they reach the inbox." },
      { img: divImg, title: "AI Link Classifier", desc: "Analyzes suspicious links with AI models to ensure authenticity." },
      { img: penImg, title: "URL Rewriter/Disarmer", desc: "Rewrites unsafe links into safe sandboxed versions." },
      { img: dangerImg, title: "Visual Warning Overlay", desc: "Provides real-time warnings for suspicious websites." },
      { img: wifiImg, title: "Offline Threat Engine", desc: "Identifies phishing attempts even without active internet." },
      { img: boxImg, title: "SafeView Sandbox", desc: "Allows secure preview of suspicious attachments and emails." },
    ].map((item, i) => (
      <div
        key={i}
        className="bg-white shadow-md rounded-xl p-6 hover:shadow-2xl hover:scale-105 transition-transform duration-300"
      >
        <div className="w-20 h-20 mx-auto mb-6 flex items-center justify-center rounded-full bg-blue-100 hover:bg-blue-200 transition-colors duration-300">
          <img src={item.img} alt={item.title} className="w-12 h-12 object-contain" />
        </div>
        <h4 className="font-bold text-lg mb-2 text-gray-800">{item.title}</h4>
        <p className="text-gray-600">{item.desc}</p>
      </div>
    ))}
  </div>
</section>

{/*  LearnMoreSection */}
<div className="min-h-screen bg-gray-50 font-inter text-gray-800">
      {/* Top Section: Attachment-Level Threat Neutralization */}
      <section className="relative bg-white py-16 sm:py-20 lg:py-24 overflow-hidden">
        <div className="container mx-auto px-4 flex flex-col lg:flex-row items-center justify-between gap-12">
          {/* Left Side: Illustration/Login Form Outline */}
          <div className="lg:w-1/2 flex justify-center items-center relative h-64 sm:h-80 lg:h-auto lg:min-h-[400px] w-full">
            <div className="relative w-full h-full max-w-md bg-blue-50 bg-opacity-50 rounded-xl flex items-center justify-center">
              <div className="absolute top-4 left-4 w-12 h-12 bg-blue-200 rounded-full opacity-30"></div>
              <div className="absolute bottom-4 right-4 w-20 h-20 bg-blue-200 rounded-full opacity-20"></div>
              <div className="border border-blue-300 rounded-lg p-6 w-64 bg-white shadow-lg">
                <div className="mb-4 text-center">
                  <span className="inline-block p-2 rounded-full bg-gray-200">
                    <svg
                      className="w-6 h-6 text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      ></path>
                    </svg>
                  </span>
                </div>
                <input
                  type="text"
                  placeholder="Username"
                  className="w-full p-2 mb-3 border border-gray-300 rounded-md text-sm"
                />
                <input
                  type="password"
                  placeholder="********"
                  className="w-full p-2 mb-4 border border-gray-300 rounded-md text-sm"
                />
                <button className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-150">
                  Login
                </button>
              </div>
            </div>
            <div className="absolute top-0 left-1/4 w-px h-24 bg-blue-300"></div>
            <div className="absolute top-0 right-1/4 w-px h-24 bg-blue-300"></div>
            <div className="absolute top-20 left-1/4 w-2 h-2 bg-red-500 rounded-full"></div>
            <div className="absolute top-24 right-1/4 w-2 h-2 bg-green-500 rounded-full"></div>
          </div>

          {/* Right Side: Threat Neutralization Features */}
          <div className="lg:w-1/2 text-center lg:text-left">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 leading-tight">
              Attachment-Level Threat Neutralization
            </h2>
            <p className="text-gray-600 mb-8 max-w-xl mx-auto lg:mx-0">
              Advanced protection against malicious files and attachments across all communication platforms.
            </p>

            <div className="space-y-6">
              {/* Feature Item 1 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 rounded-full bg-blue-100 text-blue-600">
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    ></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-1">File Interception Engine</h3>
                  <p className="text-gray-600">Detects and captures incoming files in real-time from all sources.</p>
                </div>
              </div>

              {/* Feature Item 2 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 rounded-full bg-blue-100 text-blue-600">
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    ></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-1">Macro/Link Scrubber</h3>
                  <p className="text-gray-600">Scans and strips dangerous macros and embedded links from documents.</p>
                </div>
              </div>

              {/* Feature Item 3 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 rounded-full bg-blue-100 text-blue-600">
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M5 13l4 4L19 7"
                    ></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-1">Archive Auto-Scanner</h3>
                  <p className="text-gray-600">Opens ZIP/RAR containers in sandbox and scans internal contents.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom Section: Learn More */}
      <section className="bg-blue-600 py-16 sm:py-20 lg:py-24 text-white relative overflow-hidden">
        <div className="container mx-auto px-4 flex flex-col lg:flex-row items-center justify-between gap-12">
          {/* Left Side: Dashboard Screenshot */}
          <div className="lg:w-1/2 flex justify-center">
            <img
              src="https://placehold.co/600x400/3b82f6/ffffff?text=Dashboard+Screenshot"
              alt="Dashboard Screenshot"
              className="rounded-lg shadow-xl max-w-full h-auto"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://placehold.co/600x400/cccccc/333333?text=Dashboard";
              }}
            />
          </div>

          {/* Right Side: Info Cards */}
          <div className="lg:w-1/2 text-center lg:text-left">
            <p className="text-blue-200 text-sm mb-2">How PhishZil works</p>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 leading-tight">
              Learn more about our
            </h2>
            <p className="text-blue-100 mb-8 max-w-xl mx-auto lg:mx-0">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Info Card 1 - correct Icon */}
                    <div className="bg-white text-black p-6 rounded-lg shadow-md flex flex-col items-center text-center hover:shadow-xl hover:scale-105 transition-transform duration-300">
                      <div className="p-3  mb-4">
                        <img src={correctImg} alt="Tomb Icon" className="w-12 h-12 object-contain" />
                      </div>
                      <h3 className="font-semibold text-lg mb-2">Trusted Network</h3>
                      <p className="text-gray-600 text-sm">
                        A network of trusted partners ensures your data is secure.
                      </p>
                    </div>

                    {/* Info Card 2 - profile Icon */}
                    <div className="bg-white text-black p-6 rounded-lg shadow-md flex flex-col items-center text-center hover:shadow-xl hover:scale-105 transition-transform duration-300">
                      <div className="p-3  mb-4">
                        <img src={profileImg} alt="Correct Icon" className="w-12 h-12 object-contain" />
                      </div>
                      <h3 className="font-semibold text-lg mb-2">Personalized Legal</h3>
                      <p className="text-gray-600 text-sm">
                        Our attorneys will work closely with you to develop.
                      </p>
                    </div>

                    {/* Info Card 3 - tomb Icon */}
                    <div className="bg-white text-black p-6 rounded-lg shadow-md flex flex-col items-center text-center hover:shadow-xl hover:scale-105 transition-transform duration-300">
                      <div className="p-3  mb-4">
                        <img src={tombImg} alt="Profile Icon" className="w-12 h-12 object-contain" />
                      </div>
                      <h3 className="font-semibold text-lg mb-2">Client Satisfaction</h3>
                      <p className="text-gray-600 text-sm">
                        We're dedicated to going above and beyond to ensure.
                      </p>
                    </div>
                  </div>


            <button className="mt-10 py-3 px-8 bg-white text-blue-600 font-semibold rounded-lg shadow-md hover:bg-gray-100 transition duration-150 ease-in-out">
              Learn More
            </button>
          </div>
        </div>
      </section>
    </div>

      

      {/* Platform Support */}
<section className="py-20 px-10 text-center bg-gray-50">
  <h3 className="text-3xl font-bold mb-6">Universal Platform Support</h3>
  <p className="text-gray-600 mb-10">
    Deploy Phishzil™ across all your devices and platforms with seamless integration.
  </p>

  <div className="grid grid-cols-2 md:grid-cols-5 gap-6 max-w-6xl mx-auto">
    {[
      { img: phoneImg, label: "Android", desc: "Instant permissions" },
      { img: laptopImg, label: "Windows", desc: "Seamless workstation integration" },
      { img: appleImg, label: "macOS", desc: "App-level security integration" },
      { img: browserImg, label: "Browser Extension", desc: "Chrome, Edge, Firefox, Safari" },
      { img: containerImg, label: "Enterprise", desc: "Centralized controls + MDM integration" },
    ].map((item, i) => (
      <div
        key={i}
        className="bg-white border-2 border-blue-500 rounded-lg p-8 h-80 flex flex-col items-center justify-center shadow hover:shadow-xl hover:scale-105 transition-transform duration-300"
      >
        <img
          src={item.img}
          alt={item.label}
          className="w-20 h-20 md:w-28 md:h-28 object-contain mb-4"
        />
        <h4 className="font-semibold text-lg text-gray-800">{item.label}</h4>
        <p className="text-sm text-gray-600 mt-2">{item.desc}</p>
      </div>
    ))}
  </div>
</section>


      {/* Pricing */}
<section id="pricing" className="bg-white py-20 px-6 md:px-16">
  <div className="text-center mb-12">
    <h3 className="text-3xl font-bold text-gray-800 mb-4">
      The right plan can change <br />
      <span className="text-blue-600">your work life</span>
    </h3>
    <p className="text-gray-600 mb-6">Choose a plan that’s right for you</p>

    {/* Billing Toggle */}
    <div className="flex justify-center items-center space-x-6 mb-10">
      <label className="flex items-center space-x-2 cursor-pointer">
        <input type="radio" name="billing" defaultChecked className="form-radio text-blue-600" />
        <span className="text-gray-700 font-medium">Monthly Plan</span>
      </label>
      <label className="flex items-center space-x-2 cursor-pointer">
        <input type="radio" name="billing" className="form-radio text-blue-600" />
        <span className="text-gray-700 font-medium">
          Yearly Plan <span className="text-blue-600 font-semibold">(Save 25%)</span>
        </span>
      </label>
    </div>
  </div>

  <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
    <div className="border rounded-2xl p-8 shadow hover:shadow-lg">
      <h4 className="text-xl font-semibold mb-4">Personal</h4>
      <p className="text-4xl font-bold mb-2">$9.99</p>
      <p className="text-gray-500 mb-6">/month</p>
      <button className="w-full bg-blue-600 text-white py-2 rounded-lg mb-6">Get Started Now</button>
      <ul className="space-y-3 text-gray-600">
        <li>✔️ Visual Phish Detection</li>
        <li>✔️ Basic Link Scanning</li>
        <li>✔️ File Screening</li>
        <li>✔️ Mobile Protection</li>
        <li>✔️ Offline Threat Detection</li>
      </ul>
    </div>

    <div className="border rounded-2xl p-8 shadow-lg bg-blue-600 text-white scale-105">
      <h4 className="text-xl font-semibold mb-4">Family</h4>
      <p className="text-4xl font-bold mb-2">$19.99</p>
      <p className="mb-6">/month</p>
      <button className="w-full bg-white text-blue-600 py-2 rounded-lg mb-6 font-semibold">Get Started Now</button>
      <ul className="space-y-3">
        <li>✔️ 5 User Accounts</li>
        <li>✔️ Social Media Scanning</li>
        <li>✔️ Advanced Link Interception</li>
        <li>✔️ Email Threat Analysis</li>
        <li>✔️ Sandbox File Screening</li>
      </ul>
    </div>

    <div className="border rounded-2xl p-8 shadow hover:shadow-lg">
      <h4 className="text-xl font-semibold mb-4">Enterprise</h4>
      <p className="text-4xl font-bold mb-2">$49.99</p>
      <p className="text-gray-500 mb-6">/month</p>
      <button className="w-full bg-blue-600 text-white py-2 rounded-lg mb-6">Get Started Now</button>
      <ul className="space-y-3 text-gray-600">
        <li>✔️ Unlimited Endpoints</li>
        <li>✔️ AI Detection</li>
        <li>✔️ Central Dashboard</li>
        <li>✔️ Outlook/Gmail Integration</li>
        <li>✔️ API Integration</li>
        <li>✔️ Security Reports</li>
      </ul>
    </div>
  </div>
</section>

      


    {/* footer */}
    <footer className="bg-gray-900 text-gray-300 py-12 px-6 md:px-16">
      <div className="grid md:grid-cols-4 gap-10 max-w-6xl mx-auto">
        {/* About */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">About Phishzil</h3>
          <p className="text-sm mb-4">
            Protecting businesses and individuals from phishing threats with real-time AI‑powered solutions.
          </p>
          <div className="flex space-x-4">
            {/* External links stay <a> with real URLs */}
            <a href="https://phishzil.com" target="_blank" rel="noopener noreferrer" className="hover:text-white">🌐</a>
            <a href="https://twitter.com/yourhandle" target="_blank" rel="noopener noreferrer" className="hover:text-white">🐦</a>
            <a href="https://facebook.com/yourpage" target="_blank" rel="noopener noreferrer" className="hover:text-white">📘</a>
            <a href="https://youtube.com/yourchannel" target="_blank" rel="noopener noreferrer" className="hover:text-white">▶️</a>
          </div>
        </div>

        {/* Company */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Company</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/about" className="hover:text-white">About</Link></li>
            <li><Link to="/careers" className="hover:text-white">Careers</Link></li>
            <li><Link to="/press" className="hover:text-white">Press</Link></li>
            <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
          </ul>
        </div>

        {/* Help */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Help</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/support" className="hover:text-white">Support</Link></li>
            <li><Link to="/docs" className="hover:text-white">Documentation</Link></li>
            <li><Link to="/faqs" className="hover:text-white">FAQs</Link></li>
            <li><Link to="/privacy" className="hover:text-white">Privacy Policy</Link></li>
          </ul>
        </div>

        {/* Resources */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/blog" className="hover:text-white">Blog</Link></li>
            <li><Link to="/whitepapers" className="hover:text-white">Whitepapers</Link></li>
            <li><Link to="/case-studies" className="hover:text-white">Case Studies</Link></li>
            <li><Link to="/newsletter" className="hover:text-white">Newsletter</Link></li>
          </ul>
        </div>
      </div>

      {/* Bottom Note */}
      <div className="text-center mt-10 text-gray-500 text-sm">
        © {new Date().getFullYear()} Phishzil™. All rights reserved.
      </div>
    </footer>
 



      
      
    </div>
  );
}

export default App;
