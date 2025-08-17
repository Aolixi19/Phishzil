import React, { useState } from "react";
import { Link } from "react-router-dom";

const Signup = () => {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    rememberMe: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form Submitted:", formData);
    // 🚀 Connect to backend API later
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6 font-inter">
      <div className="flex flex-col lg:flex-row bg-white rounded-xl shadow-lg overflow-hidden w-full max-w-6xl">
        
        {/* Left Section */}
        <div className="lg:w-1/2 bg-blue-600 text-white p-12 flex flex-col justify-between relative">
          <div>
            <h1 className="text-4xl font-bold mb-4">Welcome to PhishZil</h1>
            <p className="text-blue-100 mb-8">
              Advanced AI-powered modules working together to provide comprehensive phishing protection.
            </p>
          </div>
          <div>
            <div className="flex text-yellow-400 mb-2">
              {Array(5).fill("⭐").map((star, i) => (
                <span key={i}>{star}</span>
              ))}
            </div>
            <p className="text-blue-100 italic mb-4">
              "We love PhishZil! Our developers were using it for their projects, so we already knew what kind of design they want."
            </p>
            <div className="flex items-center">
              <img
                src="https://placehold.co/40x40/ffffff/000000?text=JD"
                alt="John Doe"
                className="w-10 h-10 rounded-full mr-3 border-2 border-white"
              />
              <div>
                <p className="font-semibold">John Doe</p>
                <p className="text-blue-200 text-sm">Co-Founder, PhishZil.co</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Section - Form */}
        <div className="lg:w-1/2 p-12 bg-white flex flex-col justify-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-4 text-center lg:text-left">
            Join us today 👋
          </h2>
          <p className="text-gray-600 mb-8 text-center lg:text-left">
            PhishZil gives you the blocks and components you need to protect yourself from online threats.
          </p>

          {/* Social Buttons */}
          <div className="space-y-4 mb-8">
            <button className="w-full flex items-center justify-center py-3 px-4 border rounded-lg shadow-sm hover:bg-gray-50">
              <img src="https://img.icons8.com/color/24/google-logo.png" alt="Google" className="mr-3" />
              Sign up with Google
            </button>
            <button className="w-full flex items-center justify-center py-3 px-4 border rounded-lg shadow-sm hover:bg-gray-50">
              <img src="https://img.icons8.com/ios-glyphs/24/github.png" alt="GitHub" className="mr-3" />
              Continue with GitHub
            </button>
          </div>

          {/* Signup Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                First & Last Name
              </label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border rounded-lg focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Remember Me */}
            <div className="flex items-center">
              <input
                type="checkbox"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 border-gray-300 rounded"
              />
              <label className="ml-2 text-sm text-gray-900">Remember me</label>
            </div>

            {/* Submit */}
            <button
              type="submit"
              className="w-full py-3 px-4 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700"
            >
              Create Account
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
