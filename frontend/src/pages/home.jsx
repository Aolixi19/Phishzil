
import React, { useState} from "react";
import { Link } from "react-router-dom";
//import MobileNavbar from "../components/MobileNavbar";

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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="font-sans text-gray-800">
      {/* Navbar */}
      <header className="relative flex items-center justify-between px-4 py-4 bg-white shadow-md sm:px-6 lg:px-10">
        <h1 className="text-xl font-bold text-blue-600">Phishzil™</h1>
        
        {/* Desktop Navigation */}
        <nav className="hidden space-x-6 font-medium text-gray-600 md:flex">
          <a href="#features" className="hover:text-blue-600">Features</a>
          <a href="#architecture" className="hover:text-blue-600">Platforms</a>
          <Link to="/dashboard" className="hover:text-blue-600">
            Dashboard
          </Link>
          <a href="#pricing" className="hover:text-blue-600">Pricing</a>
        </nav>

        {/* Desktop Get Started Button */}
        <Link
          to="/signup"
          className="hidden px-4 py-2 text-white bg-blue-600 rounded-lg md:inline-block hover:bg-blue-700"
        >
          Get Started
        </Link>

        {/* Mobile Menu Button */}
        <button 
          className="p-2 text-gray-600 rounded-md md:hidden hover:text-gray-800 hover:bg-gray-100"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth="2" 
              d={isMobileMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
            />
          </svg>
        </button>

        {/* Mobile Navigation Menu */}
        {isMobileMenuOpen && (
          <div className="absolute left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg md:hidden top-full">
            <div className="flex flex-col p-4 space-y-4">
              <a 
                href="#features" 
                className="py-2 text-gray-600 hover:text-blue-600"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Features
              </a>
              <a 
                href="#architecture" 
                className="py-2 text-gray-600 hover:text-blue-600"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Platforms
              </a>
              <Link 
                to="/dashboard" 
                className="py-2 text-gray-600 hover:text-blue-600"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Dashboard
              </Link>
              <a 
                href="#pricing" 
                className="py-2 text-gray-600 hover:text-blue-600"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Pricing
              </a>
              <Link 
                to="/signup" 
                className="px-4 py-2 mt-4 text-center text-white bg-blue-600 rounded-lg hover:bg-blue-700"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Get Started
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* Hero Section */}
    <section className="px-10 py-20 text-white bg-gradient-to-r from-blue-900 to-blue-600">
      <div className="grid items-center max-w-6xl gap-10 mx-auto md:grid-cols-2">
    
        {/* Left: Text */}
      <div className="text-left">
      <h2 className="mb-6 text-4xl font-bold md:text-5xl">
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
          className="px-6 py-3 font-semibold text-white transition bg-blue-500 rounded-lg hover:bg-blue-400"
        >
          Start Free Trial
        </Link>
        <Link
          to="/demo"
          className="px-6 py-3 font-semibold text-blue-600 transition bg-white rounded-lg hover:bg-gray-100"
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
  <h3 className="mb-4 text-2xl font-semibold">
    Unleash the full power of Phishzil
  </h3>
  <p className="max-w-2xl mx-auto mb-10 text-gray-600">
    Everything you need to protect yourself online from phishing attacks is here.
  </p>

  <div className="grid max-w-4xl grid-cols-1 gap-8 mx-auto md:grid-cols-3">
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
<section id="features" className="py-20 text-center bg-gray-50">
  <h2 className="mb-4 font-semibold tracking-wide text-blue-600 uppercase">
    Features
  </h2>
  <h3 className="mb-6 text-3xl font-bold">Core Protection Modules</h3>
  <p className="max-w-2xl mx-auto mb-12 text-gray-600">
    Advanced AI-powered modules working together to provide comprehensive phishing protection.
  </p>

  <div className="grid max-w-6xl grid-cols-1 gap-8 mx-auto md:grid-cols-3">
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
        className="p-6 transition-transform duration-300 bg-white shadow-md rounded-xl hover:shadow-2xl hover:scale-105"
      >
        <div className="flex items-center justify-center w-20 h-20 mx-auto mb-6 transition-colors duration-300 bg-blue-100 rounded-full hover:bg-blue-200">
          <img src={item.img} alt={item.title} className="object-contain w-12 h-12" />
        </div>
        <h4 className="mb-2 text-lg font-bold text-gray-800">{item.title}</h4>
        <p className="text-gray-600">{item.desc}</p>
      </div>
    ))}
  </div>
</section>

{/*  LearnMoreSection */}
<div className="min-h-screen text-gray-800 bg-gray-50 font-inter">
      {/* Top Section: Attachment-Level Threat Neutralization */}
      <section className="relative py-16 overflow-hidden bg-white sm:py-20 lg:py-24">
        <div className="container flex flex-col items-center justify-between gap-12 px-4 mx-auto lg:flex-row">
          {/* Left Side: Illustration/Login Form Outline */}
          <div className="lg:w-1/2 flex justify-center items-center relative h-64 sm:h-80 lg:h-auto lg:min-h-[400px] w-full">
            <div className="relative flex items-center justify-center w-full h-full max-w-md bg-opacity-50 bg-blue-50 rounded-xl">
              <div className="absolute w-12 h-12 bg-blue-200 rounded-full top-4 left-4 opacity-30"></div>
              <div className="absolute w-20 h-20 bg-blue-200 rounded-full bottom-4 right-4 opacity-20"></div>
              <div className="w-64 p-6 bg-white border border-blue-300 rounded-lg shadow-lg">
                <div className="mb-4 text-center">
                  <span className="inline-block p-2 bg-gray-200 rounded-full">
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
                  className="w-full p-2 mb-3 text-sm border border-gray-300 rounded-md"
                />
                <input
                  type="password"
                  placeholder="********"
                  className="w-full p-2 mb-4 text-sm border border-gray-300 rounded-md"
                />
                <button className="w-full py-2 text-white transition duration-150 bg-blue-600 rounded-md hover:bg-blue-700">
                  Login
                </button>
              </div>
            </div>
            <div className="absolute top-0 w-px h-24 bg-blue-300 left-1/4"></div>
            <div className="absolute top-0 w-px h-24 bg-blue-300 right-1/4"></div>
            <div className="absolute w-2 h-2 bg-red-500 rounded-full top-20 left-1/4"></div>
            <div className="absolute w-2 h-2 bg-green-500 rounded-full top-24 right-1/4"></div>
          </div>

          {/* Right Side: Threat Neutralization Features */}
          <div className="text-center lg:w-1/2 lg:text-left">
            <h2 className="mb-6 text-3xl font-bold leading-tight sm:text-4xl lg:text-5xl">
              Attachment-Level Threat Neutralization
            </h2>
            <p className="max-w-xl mx-auto mb-8 text-gray-600 lg:mx-0">
              Advanced protection against malicious files and attachments across all communication platforms.
            </p>

            <div className="space-y-6">
              {/* Feature Item 1 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 text-blue-600 bg-blue-100 rounded-full">
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
                  <h3 className="mb-1 text-lg font-semibold">File Interception Engine</h3>
                  <p className="text-gray-600">Detects and captures incoming files in real-time from all sources.</p>
                </div>
              </div>

              {/* Feature Item 2 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 text-blue-600 bg-blue-100 rounded-full">
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
                  <h3 className="mb-1 text-lg font-semibold">Macro/Link Scrubber</h3>
                  <p className="text-gray-600">Scans and strips dangerous macros and embedded links from documents.</p>
                </div>
              </div>

              {/* Feature Item 3 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 p-2 text-blue-600 bg-blue-100 rounded-full">
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
                  <h3 className="mb-1 text-lg font-semibold">Archive Auto-Scanner</h3>
                  <p className="text-gray-600">Opens ZIP/RAR containers in sandbox and scans internal contents.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom Section: Learn More */}
      <section className="relative py-16 overflow-hidden text-white bg-blue-600 sm:py-20 lg:py-24">
        <div className="container flex flex-col items-center justify-between gap-12 px-4 mx-auto lg:flex-row">
          {/* Left Side: Dashboard Screenshot */}
          <div className="flex justify-center lg:w-1/2">
            <img
              src="https://placehold.co/600x400/3b82f6/ffffff?text=Dashboard+Screenshot"
              alt="Dashboard Screenshot"
              className="h-auto max-w-full rounded-lg shadow-xl"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://placehold.co/600x400/cccccc/333333?text=Dashboard";
              }}
            />
          </div>

          {/* Right Side: Info Cards */}
          <div className="text-center lg:w-1/2 lg:text-left">
            <p className="mb-2 text-sm text-blue-200">How PhishZil works</p>
            <h2 className="mb-6 text-3xl font-bold leading-tight sm:text-4xl lg:text-5xl">
              Learn more about our
            </h2>
            <p className="max-w-xl mx-auto mb-8 text-blue-100 lg:mx-0">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua.
            </p>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
                    {/* Info Card 1 - correct Icon */}
                    <div className="flex flex-col items-center p-6 text-center text-black transition-transform duration-300 bg-white rounded-lg shadow-md hover:shadow-xl hover:scale-105">
                      <div className="p-3 mb-4">
                        <img src={correctImg} alt="Tomb Icon" className="object-contain w-12 h-12" />
                      </div>
                      <h3 className="mb-2 text-lg font-semibold">Trusted Network</h3>
                      <p className="text-sm text-gray-600">
                        A network of trusted partners ensures your data is secure.
                      </p>
                    </div>

                    {/* Info Card 2 - profile Icon */}
                    <div className="flex flex-col items-center p-6 text-center text-black transition-transform duration-300 bg-white rounded-lg shadow-md hover:shadow-xl hover:scale-105">
                      <div className="p-3 mb-4">
                        <img src={profileImg} alt="Correct Icon" className="object-contain w-12 h-12" />
                      </div>
                      <h3 className="mb-2 text-lg font-semibold">Personalized Legal</h3>
                      <p className="text-sm text-gray-600">
                        Our attorneys will work closely with you to develop.
                      </p>
                    </div>

                    {/* Info Card 3 - tomb Icon */}
                    <div className="flex flex-col items-center p-6 text-center text-black transition-transform duration-300 bg-white rounded-lg shadow-md hover:shadow-xl hover:scale-105">
                      <div className="p-3 mb-4">
                        <img src={tombImg} alt="Profile Icon" className="object-contain w-12 h-12" />
                      </div>
                      <h3 className="mb-2 text-lg font-semibold">Client Satisfaction</h3>
                      <p className="text-sm text-gray-600">
                        We're dedicated to going above and beyond to ensure.
                      </p>
                    </div>
                  </div>


            <button className="px-8 py-3 mt-10 font-semibold text-blue-600 transition duration-150 ease-in-out bg-white rounded-lg shadow-md hover:bg-gray-100">
              Learn More
            </button>
          </div>
        </div>
      </section>
    </div>

      

      {/* Platform Support */}
<section className="px-10 py-20 text-center bg-gray-50">
  <h3 className="mb-6 text-3xl font-bold">Universal Platform Support</h3>
  <p className="mb-10 text-gray-600">
    Deploy Phishzil™ across all your devices and platforms with seamless integration.
  </p>

  <div className="grid max-w-6xl grid-cols-2 gap-6 mx-auto md:grid-cols-5">
    {[
      { img: phoneImg, label: "Android", desc: "Instant permissions" },
      { img: laptopImg, label: "Windows", desc: "Seamless workstation integration" },
      { img: appleImg, label: "macOS", desc: "App-level security integration" },
      { img: browserImg, label: "Browser Extension", desc: "Chrome, Edge, Firefox, Safari" },
      { img: containerImg, label: "Enterprise", desc: "Centralized controls + MDM integration" },
    ].map((item, i) => (
      <div
        key={i}
        className="flex flex-col items-center justify-center p-8 transition-transform duration-300 bg-white border-2 border-blue-500 rounded-lg shadow h-80 hover:shadow-xl hover:scale-105"
      >
        <img
          src={item.img}
          alt={item.label}
          className="object-contain w-20 h-20 mb-4 md:w-28 md:h-28"
        />
        <h4 className="text-lg font-semibold text-gray-800">{item.label}</h4>
        <p className="mt-2 text-sm text-gray-600">{item.desc}</p>
      </div>
    ))}
  </div>
</section>


      {/* Pricing */}
<section id="pricing" className="px-6 py-20 bg-white md:px-16">
  <div className="mb-12 text-center">
    <h3 className="mb-4 text-3xl font-bold text-gray-800">
      The right plan can change <br />
      <span className="text-blue-600">your work life</span>
    </h3>
    <p className="mb-6 text-gray-600">Choose a plan that’s right for you</p>

    {/* Billing Toggle */}
    <div className="flex items-center justify-center mb-10 space-x-6">
      <label className="flex items-center space-x-2 cursor-pointer">
        <input type="radio" name="billing" defaultChecked className="text-blue-600 form-radio" />
        <span className="font-medium text-gray-700">Monthly Plan</span>
      </label>
      <label className="flex items-center space-x-2 cursor-pointer">
        <input type="radio" name="billing" className="text-blue-600 form-radio" />
        <span className="font-medium text-gray-700">
          Yearly Plan <span className="font-semibold text-blue-600">(Save 25%)</span>
        </span>
      </label>
    </div>
  </div>

  <div className="grid max-w-6xl gap-8 mx-auto md:grid-cols-3">
    <div className="p-8 border shadow rounded-2xl hover:shadow-lg">
      <h4 className="mb-4 text-xl font-semibold">Personal</h4>
      <p className="mb-2 text-4xl font-bold">$9.99</p>
      <p className="mb-6 text-gray-500">/month</p>
      <button className="w-full py-2 mb-6 text-white bg-blue-600 rounded-lg">Get Started Now</button>
      <ul className="space-y-3 text-gray-600">
        <li>✔️ Visual Phish Detection</li>
        <li>✔️ Basic Link Scanning</li>
        <li>✔️ File Screening</li>
        <li>✔️ Mobile Protection</li>
        <li>✔️ Offline Threat Detection</li>
      </ul>
    </div>

    <div className="p-8 text-white scale-105 bg-blue-600 border shadow-lg rounded-2xl">
      <h4 className="mb-4 text-xl font-semibold">Family</h4>
      <p className="mb-2 text-4xl font-bold">$19.99</p>
      <p className="mb-6">/month</p>
      <button className="w-full py-2 mb-6 font-semibold text-blue-600 bg-white rounded-lg">Get Started Now</button>
      <ul className="space-y-3">
        <li>✔️ 5 User Accounts</li>
        <li>✔️ Social Media Scanning</li>
        <li>✔️ Advanced Link Interception</li>
        <li>✔️ Email Threat Analysis</li>
        <li>✔️ Sandbox File Screening</li>
      </ul>
    </div>

    <div className="p-8 border shadow rounded-2xl hover:shadow-lg">
      <h4 className="mb-4 text-xl font-semibold">Enterprise</h4>
      <p className="mb-2 text-4xl font-bold">$49.99</p>
      <p className="mb-6 text-gray-500">/month</p>
      <button className="w-full py-2 mb-6 text-white bg-blue-600 rounded-lg">Get Started Now</button>
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
    <footer className="px-6 py-12 text-gray-300 bg-gray-900 md:px-16">
      <div className="grid max-w-6xl gap-10 mx-auto md:grid-cols-4">
        {/* About */}
        <div>
          <h3 className="mb-4 text-lg font-semibold text-white">About Phishzil</h3>
          <p className="mb-4 text-sm">
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
          <h3 className="mb-4 text-lg font-semibold text-white">Company</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/about" className="hover:text-white">About</Link></li>
            <li><Link to="/careers" className="hover:text-white">Careers</Link></li>
            <li><Link to="/press" className="hover:text-white">Press</Link></li>
            <li><Link to="/contact" className="hover:text-white">Contact</Link></li>
          </ul>
        </div>

        {/* Help */}
        <div>
          <h3 className="mb-4 text-lg font-semibold text-white">Help</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/support" className="hover:text-white">Support</Link></li>
            <li><Link to="/docs" className="hover:text-white">Documentation</Link></li>
            <li><Link to="/faqs" className="hover:text-white">FAQs</Link></li>
            <li><Link to="/privacy" className="hover:text-white">Privacy Policy</Link></li>
          </ul>
        </div>

        {/* Resources */}
        <div>
          <h3 className="mb-4 text-lg font-semibold text-white">Resources</h3>
          <ul className="space-y-2 text-sm">
            <li><Link to="/blog" className="hover:text-white">Blog</Link></li>
            <li><Link to="/whitepapers" className="hover:text-white">Whitepapers</Link></li>
            <li><Link to="/case-studies" className="hover:text-white">Case Studies</Link></li>
            <li><Link to="/newsletter" className="hover:text-white">Newsletter</Link></li>
          </ul>
        </div>
      </div>

      {/* Bottom Note */}
      <div className="mt-10 text-sm text-center text-gray-500">
        © {new Date().getFullYear()} Phishzil™. All rights reserved.
      </div>
    </footer>
 



      
      
    </div>
  );
}

export default App;
