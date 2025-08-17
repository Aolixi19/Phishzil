import React, { useState } from 'react';
import { Link } from "react-router-dom";

const Login = () => {
  const [rememberMe, setRememberMe] = useState(false);

  const handleCheckboxChange = () => {
    setRememberMe(!rememberMe);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 sm:p-6 lg:p-8 font-inter">
      <div className="flex flex-col lg:flex-row bg-white rounded-xl shadow-lg overflow-hidden w-full max-w-6xl">
        
        {/* Left Section - Welcome */}
        <div className="lg:w-1/2 bg-blue-600 text-white p-8 sm:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none">
          <div className="relative z-10">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4 leading-tight">
              Welcome to our community
            </h1>
            <p className="text-blue-100 text-base sm:text-lg mb-8">
              Advanced AI-powered modules working together to provide comprehensive phishing protection
            </p>

            {/* Testimonial */}
            <div className="mt-12 sm:mt-16 lg:mt-24">
              <div className="flex text-yellow-400 mb-2">
                <span>&#9733;</span>
                <span>&#9733;</span>
                <span>&#9733;</span>
                <span>&#9733;</span>
                <span>&#9733;</span>
              </div>
              <p className="text-blue-100 italic text-base sm:text-lg leading-relaxed mb-6">
                "We love PhishZil! Our developers were using it for their projects, so we already knew what kind of design they want."
              </p>
              <div className="flex items-center">
                <img
                  src="https://placehold.co/40x40/ffffff/000000?text=JD"
                  alt="John Doe"
                  className="w-10 h-10 rounded-full mr-3 border-2 border-white"
                  onError={(e) => { e.target.onerror = null; e.target.src = "https://placehold.co/40x40/cccccc/333333?text=User"; }}
                />
                <div>
                  <p className="font-semibold text-white text-sm">John Doe</p>
                  <p className="text-blue-200 text-xs">Co-Founder, PhishZil.co</p>
                </div>
              </div>
            </div>
          </div>
          <div className="absolute bottom-[-50px] right-[-50px] w-48 h-48 bg-blue-700 opacity-20 rounded-full"></div>
          <div className="absolute bottom-[-100px] right-[-100px] w-64 h-64 bg-blue-700 opacity-10 rounded-full"></div>
        </div>

        {/* Right Section - Login Form */}
        <div className="lg:w-1/2 p-8 sm:p-12 lg:p-16 bg-white flex flex-col justify-center rounded-b-xl lg:rounded-r-xl lg:rounded-bl-none">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-4 text-center lg:text-left">
            Welcome back!
          </h2>
          <p className="text-gray-600 mb-8 text-center lg:text-left">
            PhishZil gives you the blocks and components you need to protect yourself from online threats
          </p>

          {/* Form Fields */}
          <div className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email address
              </label>
              <input
                type="email"
                id="email"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="i.e. davon@mail.com"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                id="password"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="********"
              />
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="rememberMe"
                  name="rememberMe"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={handleCheckboxChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="rememberMe" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>
              <Link to="/forgot-password" className="font-medium text-blue-600 hover:text-blue-500">
                Forgot password?
              </Link>
            </div>

            {/* Sign In Button */}
            <button
              type="submit"
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out"
            >
              Login
            </button>
          </div>

          <p className="mt-6 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link to="/signup" className="font-medium text-blue-600 hover:text-blue-500">
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
