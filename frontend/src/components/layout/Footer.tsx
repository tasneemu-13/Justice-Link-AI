import React from 'react';
import { Link } from 'react-router-dom';
import { Scale, ShieldAlert } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#FAF7EE] border-t border-[#DFD7C5] pt-14 pb-8 text-[#4A5568]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Col 1: Brand & Mandate */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-lg bg-[#6B1D2F] flex items-center justify-center text-[#FDFBF7] border border-[#C29B38]/50">
                <Scale className="w-5 h-5 text-[#C29B38]" />
              </div>
              <span className="font-serif text-2xl font-bold tracking-tight text-[#6B1D2F]">
                JUSTICELINK <span className="text-[#9E7D2B]">AI</span>
              </span>
            </div>
            <p className="text-sm text-[#4A5568] leading-relaxed max-w-md">
              A scientific judicial intelligence platform developed to evaluate case duration dynamics, 
              quantify right-censored court pendency, and support transparent, explainable procedural triage 
              within the Indian district judiciary.
            </p>
            <div className="flex items-center space-x-2 text-xs text-[#6B1D2F] font-semibold pt-1">
              <span className="inline-block w-2 h-2 rounded-full bg-[#1E6B2A]"></span>
              <span>Empirical Pilot: Kollam District (ONCourts Digital Court Initiative)</span>
            </div>
          </div>

          {/* Col 2: Navigation */}
          <div>
            <h4 className="font-serif text-sm font-bold text-[#6B1D2F] uppercase tracking-wider mb-4 border-b border-[#DFD7C5] pb-2">
              Platform Modules
            </h4>
            <ul className="space-y-2.5 text-xs font-medium">
              <li>
                <Link to="/explorer" className="hover:text-[#6B1D2F] transition-colors flex items-center">
                  <span className="text-[#C29B38] mr-2">›</span> Judicial Explorer
                </Link>
              </li>
              <li>
                <Link to="/intelligence" className="hover:text-[#6B1D2F] transition-colors flex items-center">
                  <span className="text-[#C29B38] mr-2">›</span> Case Intelligence & Survival
                </Link>
              </li>
              <li>
                <Link to="/research-lab" className="hover:text-[#6B1D2F] transition-colors flex items-center">
                  <span className="text-[#C29B38] mr-2">›</span> AI Research Lab & Estimator
                </Link>
              </li>
              <li>
                <Link to="/prioritization" className="hover:text-[#6B1D2F] transition-colors flex items-center">
                  <span className="text-[#C29B38] mr-2">›</span> Case Prioritization Queue
                </Link>
              </li>
              <li>
                <Link to="/methodology" className="hover:text-[#6B1D2F] transition-colors flex items-center">
                  <span className="text-[#C29B38] mr-2">›</span> Data Dictionary & Reports
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Research & Ethics */}
          <div>
            <h4 className="font-serif text-sm font-bold text-[#6B1D2F] uppercase tracking-wider mb-4 border-b border-[#DFD7C5] pb-2">
              Statutory Boundary
            </h4>
            <div className="bg-[#FFFFFF] border border-[#DFD7C5] p-3 rounded-md text-xs text-[#5A6270] space-y-2">
              <div className="flex items-start space-x-2 text-[#9E7D2B] font-semibold">
                <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5" />
                <span>Decision Support Only</span>
              </div>
              <p className="text-[11px] leading-relaxed">
                JusticeLink AI does not adjudicate guilt, evaluate merits, or substitute for judicial discretion. 
                All outputs are administrative case-flow diagnostics.
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-[#DFD7C5] pt-6 flex flex-col md:flex-row justify-between items-center text-xs text-[#718096]">
          <p>© {new Date().getFullYear()} JusticeLink AI · Indian Judicial Analytics Research. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/about" className="hover:text-[#6B1D2F]">About System</Link>
            <Link to="/methodology" className="hover:text-[#6B1D2F]">Methodology</Link>
            <span className="text-[#C29B38]">Independent Research Platform</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
