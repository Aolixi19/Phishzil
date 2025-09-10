import React, { useState, Link } from 'react';
//import { Link, useLocation } from 'react-router-dom';

const MobileNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  //const location = useLocation();

  const navigationItems = [
    { path: '#features', name: 'Features', isAnchor: true },
    { path: '#architecture', name: 'Platforms', isAnchor: true },
    { path: '/dashboard', name: 'Dashboard', isAnchor: false },
    { path: '#pricing', name: 'Pricing', isAnchor: true },
  ];

  const handleNavigation = (item) => {
    if (item.isAnchor) {
      // For anchor links, scroll to section and close menu
      const element = document.querySelector(item.path);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setIsOpen(false);
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 md:hidden">
      {/* Mobile menu button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-center w-full p-3 font-semibold text-white bg-blue-600"
      >
        <span className="mr-2">☰</span>
        Menu
      </button>

      {/* Mobile navigation items */}
      {isOpen && (
        <div className="bg-white">
          {navigationItems.map((item) => (
            item.isAnchor ? (
              <a
                key={item.path}
                href={item.path}
                onClick={() => handleNavigation(item)}
                className="flex items-center p-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50"
              >
                {item.name}
              </a>
            ) : (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => handleNavigation(item)}
                className="flex items-center p-4 text-gray-700 border-b border-gray-100 hover:bg-gray-50"
              >
                {item.name}
              </Link>
            )
          ))}
          <Link
            to="/signup"
            onClick={() => setIsOpen(false)}
            className="flex items-center justify-center p-4 font-semibold text-white bg-blue-600 hover:bg-blue-700"
          >
            Get Started
          </Link>
        </div>
      )}
    </div>
  );
};

export default MobileNavbar;