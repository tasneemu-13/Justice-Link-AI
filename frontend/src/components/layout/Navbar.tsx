import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Scale, Menu, X, ArrowUpRight } from 'lucide-react';

export const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Judicial Explorer', path: '/explorer' },
    { name: 'Case Intelligence', path: '/intelligence' },
    { name: 'AI Research Lab', path: '/research-lab' },
    { name: 'Case Prioritization', path: '/prioritization' },
    { name: 'Research & Methodology', path: '/methodology' },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="sticky top-0 z-50 bg-[#FDFBF7]/95 backdrop-blur-md border-b border-[#DFD7C5]">
      {/* Top Institutional Notification Ribbon */}
      <div className="bg-[#6B1D2F] text-[#FDFBF7] px-4 sm:px-8 py-1.5 text-xs flex justify-between items-center border-b border-[#C29B38]">
        <div className="flex items-center space-x-3">
          <span className="font-semibold tracking-wider flex items-center">
            <span className="mr-1.5">🏛️</span> JUSTICELINK AI · न्याय सेतु
          </span>
          <span className="hidden md:inline text-[#C29B38]">|</span>
          <span className="hidden md:inline text-[#E8E1D3] text-[11px]">
            National Judicial Case Intelligence & Explainable AI Research Platform
          </span>
        </div>
        <div className="flex items-center space-x-3 text-[11px]">
          <span className="bg-[#80182A] text-[#FDFBF7] px-2 py-0.5 rounded border border-[#C29B38]/40">
            Active Research Pilot: Kerala (Kollam NI-138)
          </span>
          <span className="text-[#C29B38] font-serif">eCourts Aligned</span>
        </div>
      </div>

      {/* Main Horizontal Navbar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo & Brand Identity */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-11 h-11 rounded-lg bg-[#6B1D2F] flex items-center justify-center text-[#FDFBF7] shadow-sm border border-[#9E7D2B]/40 group-hover:bg-[#80182A] transition-colors">
              <Scale className="w-6 h-6 text-[#C29B38]" />
            </div>
            <div className="flex flex-col">
              <span className="font-serif text-xl sm:text-2xl font-bold tracking-tight text-[#6B1D2F]">
                JUSTICELINK <span className="text-[#9E7D2B]">AI</span>
              </span>
              <span className="text-[10px] uppercase tracking-widest text-[#5A6270] font-medium -mt-1">
                Judicial Informatics
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden xl:flex items-center space-x-1 lg:space-x-2">
            {navLinks.map((link) => {
              const active = isActive(link.path);
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`px-3 py-2 rounded-md text-xs font-semibold tracking-wide transition-all ${
                    active
                      ? 'text-[#6B1D2F] bg-[#EFE9DC] border-b-2 border-[#6B1D2F]'
                      : 'text-[#3D4451] hover:text-[#6B1D2F] hover:bg-[#F8F5EE]'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Action CTA */}
          <div className="hidden sm:flex items-center space-x-3">
            <Link
              to="/explorer"
              className="inline-flex items-center px-4 py-2 border border-[#9E7D2B] text-xs font-semibold rounded-md shadow-xs text-[#FDFBF7] bg-[#6B1D2F] hover:bg-[#80182A] transition-all"
            >
              Explore Platform
              <ArrowUpRight className="ml-1.5 w-3.5 h-3.5 text-[#C29B38]" />
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center xl:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-md text-[#6B1D2F] hover:bg-[#EFE9DC] focus:outline-hidden"
              aria-label="Toggle navigation"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {isOpen && (
        <div className="xl:hidden bg-[#F8F5EE] border-b border-[#DFD7C5] px-4 pt-2 pb-6 space-y-1">
          {navLinks.map((link) => {
            const active = isActive(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setIsOpen(false)}
                className={`block px-3 py-2 rounded-md text-sm font-medium ${
                  active
                    ? 'text-[#6B1D2F] bg-[#EFE9DC] font-bold'
                    : 'text-[#4A5568] hover:text-[#6B1D2F] hover:bg-[#EFE9DC]'
                }`}
              >
                {link.name}
              </Link>
            );
          })}
          <div className="pt-3">
            <Link
              to="/explorer"
              onClick={() => setIsOpen(false)}
              className="block w-full text-center px-4 py-2.5 bg-[#6B1D2F] text-white rounded-md text-sm font-semibold"
            >
              Explore Platform
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};
