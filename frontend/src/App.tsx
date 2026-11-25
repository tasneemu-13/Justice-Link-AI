import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { Home } from './pages/Home';

function ScrollToTop() {
  const { pathname } = useLocation();
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <div className="min-h-screen flex flex-col bg-[#FDFBF7] text-[#1E232A]">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">About Page Loading...</div>} />
            <Route path="/explorer" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">Judicial Explorer Loading...</div>} />
            <Route path="/intelligence" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">Case Intelligence Loading...</div>} />
            <Route path="/research-lab" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">AI Research Lab Loading...</div>} />
            <Route path="/prioritization" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">Case Prioritization Loading...</div>} />
            <Route path="/methodology" element={<div className="p-16 text-center font-serif text-2xl text-[#6B1D2F]">Research & Methodology Loading...</div>} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
};

export default App;
