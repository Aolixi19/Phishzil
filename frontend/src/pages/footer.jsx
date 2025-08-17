import React from "react";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
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
  );
}
