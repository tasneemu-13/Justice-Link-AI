import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  ArrowRight, 
  Compass, 
  Activity, 
  Cpu, 
  ListOrdered, 
  FileText, 
  MapPin, 
  Building2, 
  TrendingUp, 
  ShieldCheck 
} from 'lucide-react';
import { Court3DVisualizer } from '../components/architecture/Court3DVisualizer';
import { api } from '../services/api';
import type { EdaSummary, ModelMetric } from '../types';

export const Home: React.FC = () => {
  const [summary, setSummary] = useState<EdaSummary | null>(null);
  const [bestModel, setBestModel] = useState<ModelMetric | null>(null);

  useEffect(() => {
    api.getEdaSummary().then(setSummary);
    api.getMetrics().then((metrics) => {
      const top = metrics.find((m) => m.model_name.includes('Lasso')) || metrics[0];
      setBestModel(top);
    });
  }, []);

  const totalCases = summary?.total_cases ?? 1284;
  const avgDuration = summary?.disposed_duration_mean ? Math.round(summary.disposed_duration_mean * 10) / 10 : 166.2;
  const bestMae = bestModel?.test_mae ? Math.round(bestModel.test_mae * 10) / 10 : 63.5;

  return (
    <div className="space-y-24 pb-20">
      {/* 1. HERO SECTION */}
      <section className="relative pt-12 pb-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Hero Left: Editorial Vision */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center space-x-2 bg-[#EFE9DC] border border-[#C29B38]/50 px-3 py-1 rounded-full text-xs font-semibold text-[#6B1D2F]">
              <span className="w-2 h-2 rounded-full bg-[#6B1D2F] animate-pulse"></span>
              <span>SCIENTIFIC JUDICIAL INFORMATICS · KERALA DISTRICT COURTS PILOT</span>
            </div>

            <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold text-[#6B1D2F] leading-[1.15] tracking-tight">
              Reimagining Judicial Intelligence Through <span className="text-[#9E7D2B]">AI</span>.
            </h1>

            <p className="font-editorial text-xl text-[#374151] italic leading-relaxed max-w-2xl">
              An explainable machine learning platform engineered to evaluate systemic judicial pendency, 
              quantify case duration trajectories, and support transparent procedural triage for district courts.
            </p>

            <p className="text-sm text-[#5A6270] leading-relaxed max-w-xl">
              JusticeLink AI bridges official court discovery metadata and empirical case records. Calibrated on 1,284 verified 
              filings under the Kollam ONCourts initiative, it provides research-grade, non-merit procedural decision support.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap gap-4 pt-4">
              <Link
                to="/explorer"
                className="inline-flex items-center px-6 py-3.5 rounded-md text-sm font-semibold text-white bg-[#6B1D2F] hover:bg-[#80182A] shadow-sm border border-[#521422] transition-all group"
              >
                <span>Explore Platform</span>
                <ArrowRight className="ml-2 w-4 h-4 text-[#C29B38] group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/methodology"
                className="inline-flex items-center px-6 py-3.5 rounded-md text-sm font-semibold text-[#6B1D2F] bg-[#FAF7EE] hover:bg-[#EFE9DC] border border-[#DFD7C5] transition-all"
              >
                Discover Our Research
              </Link>
            </div>

            {/* Quick Proof Strip */}
            <div className="pt-6 grid grid-cols-3 gap-4 border-t border-[#DFD7C5]">
              <div>
                <div className="font-serif text-2xl font-bold text-[#6B1D2F]">{totalCases.toLocaleString()}</div>
                <div className="text-xs text-[#5A6270]">Verified Pilot Filings</div>
              </div>
              <div>
                <div className="font-serif text-2xl font-bold text-[#6B1D2F]">{avgDuration} d</div>
                <div className="text-xs text-[#5A6270]">Avg Completed Duration</div>
              </div>
              <div>
                <div className="font-serif text-2xl font-bold text-[#1E6B2A]">{bestMae} d</div>
                <div className="text-xs text-[#5A6270]">Top Model MAE (Lasso)</div>
              </div>
            </div>
          </div>

          {/* Hero Right: 3D High Court Architecture Twin */}
          <div className="lg:col-span-5">
            <Court3DVisualizer className="h-[460px]" />
          </div>
        </div>
      </section>

      {/* 2. PLATFORM MANDATE & RESEARCH INTEGRITY */}
      <section className="bg-[#FAF7EE] border-y border-[#DFD7C5] py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-4 mb-12">
            <span className="text-xs uppercase font-bold text-[#9E7D2B] tracking-wider">
              METHODOLOGICAL FOUNDATIONS
            </span>
            <h2 className="font-serif text-3xl font-bold text-[#6B1D2F]">
              Five Pillars of Judicial Decision Support
            </h2>
            <p className="text-sm text-[#4A5568] leading-relaxed">
              JusticeLink AI adheres to strict empirical guidelines: zero fabricated records, rigorous right-censoring treatment, 
              and complete transparency into algorithmic influence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {[
              {
                icon: MapPin,
                title: "Administrative Discovery",
                desc: "Cataloging 180 court complexes across all 14 Kerala districts while keeping discovery separate from trained corpora.",
              },
              {
                icon: TrendingUp,
                title: "Survival Modeling",
                desc: "Non-parametric Kaplan-Meier analysis accounting for 1,006 right-censored pending cases without survivorship bias.",
              },
              {
                icon: Cpu,
                title: "Benchmarked ML Suite",
                desc: "Evaluating 7 distinct algorithms (OLS, Ridge, Lasso, Trees, Random Forests) under 5-fold cross-validation.",
              },
              {
                icon: ListOrdered,
                title: "Explainable Prioritization",
                desc: "Multi-factor procedural triage identifying delayed matters with human-auditable text factor explanations.",
              },
              {
                icon: ShieldCheck,
                title: "Decision Support Only",
                desc: "No automated judicial decrees, no guilt assessment, and zero proxy bias from protected personal litigant identities.",
              },
            ].map((pillar, idx) => (
              <div 
                key={idx} 
                className="bg-[#FFFFFF] border border-[#DFD7C5] rounded-lg p-5 shadow-xs hover:border-[#6B1D2F]/60 transition-all space-y-3"
              >
                <div className="w-9 h-9 rounded-md bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                  <pillar.icon className="w-5 h-5 text-[#9E7D2B]" />
                </div>
                <h3 className="font-serif text-base font-bold text-[#6B1D2F]">
                  {pillar.title}
                </h3>
                <p className="text-xs text-[#4A5568] leading-relaxed">
                  {pillar.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 3. EXPLORE THE PLATFORM (EDITORIAL MODULE CARDS) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between border-b border-[#DFD7C5] pb-6">
          <div>
            <span className="text-xs uppercase font-bold text-[#9E7D2B] tracking-wider">
              INTERACTIVE RESEARCH CAPABILITIES
            </span>
            <h2 className="font-serif text-3xl font-bold text-[#6B1D2F] mt-1">
              Explore the Platform Modules
            </h2>
          </div>
          <p className="text-xs text-[#5A6270] max-w-md mt-2 md:mt-0">
            Select a specialized interface below to interact with court maps, survival curves, duration estimators, and review queues.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Card 1: Judicial Explorer */}
          <div className="group bg-[#FFFFFF] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#6B1D2F]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <Compass className="w-6 h-6 text-[#9E7D2B]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                India Judicial Explorer
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Geographic discovery across states and districts. Drill down into Kerala's 14 judicial districts and 180 court complexes with verified CNR identifier lookups.
              </p>
              <div className="text-[11px] font-semibold text-[#9E7D2B] bg-[#FAF7EE] p-2 rounded border border-[#DFD7C5]">
                Includes: 1,239 multi-district CNR lookup keys
              </div>
            </div>
            <Link
              to="/explorer"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              Launch Geographic Explorer <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>

          {/* Card 2: Case Intelligence */}
          <div className="group bg-[#FFFFFF] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#C29B38]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <Activity className="w-6 h-6 text-[#C29B38]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                Case Intelligence & Survival
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Empirical pendency analysis and Kaplan-Meier non-parametric survival function. Evaluates disposal duration distributions and monthly filing velocity.
              </p>
              <div className="text-[11px] font-semibold text-[#6B1D2F] bg-[#FAF7EE] p-2 rounded border border-[#DFD7C5]">
                Includes: Right-censored duration distributions
              </div>
            </div>
            <Link
              to="/intelligence"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              View Backlog Analytics <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>

          {/* Card 3: AI Research Lab */}
          <div className="group bg-[#FFFFFF] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#6B1D2F]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <Cpu className="w-6 h-6 text-[#9E7D2B]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                AI Research Lab & Benchmarks
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Standardized benchmarking matrix across 7 ML algorithms. Features actual vs. predicted diagnostics, Gini feature importance, and interactive case duration estimator.
              </p>
              <div className="text-[11px] font-semibold text-[#1E6B2A] bg-[#E8F5E9] p-2 rounded border border-[#A5D6A7]">
                Best: Lasso MAE 63.49d (-25.5% vs baseline)
              </div>
            </div>
            <Link
              to="/research-lab"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              Access ML Studio <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>

          {/* Card 4: Case Prioritization */}
          <div className="group bg-[#FFFFFF] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#C29B38]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <ListOrdered className="w-6 h-6 text-[#C29B38]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                Case Prioritization Queue
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Explainable procedural queue prioritizing 1,006 pending matters for administrative triage. Each case provides auditable factor attributions and review actions.
              </p>
              <div className="text-[11px] font-semibold text-[#6B1D2F] bg-[#FAF7EE] p-2 rounded border border-[#DFD7C5]">
                Includes: NDCG@50 & Top-50 Concordance metrics
              </div>
            </div>
            <Link
              to="/prioritization"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              Open Prioritization Queue <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>

          {/* Card 5: Research & Methodology */}
          <div className="group bg-[#FFFFFF] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#6B1D2F]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FAF7EE] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <FileText className="w-6 h-6 text-[#9E7D2B]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                Research & Methodology
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Full academic specifications: Data Dictionary, mathematical equations, cross-validation protocols, and one-click downloadable research reports and datasets.
              </p>
              <div className="text-[11px] font-semibold text-[#718096] bg-[#FAF7EE] p-2 rounded border border-[#DFD7C5]">
                Includes: Full markdown & CSV asset downloads
              </div>
            </div>
            <Link
              to="/methodology"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              Review Methodology <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>

          {/* Card 6: About the System */}
          <div className="group bg-[#FAF7EE] border border-[#DFD7C5] rounded-xl p-6 hover:shadow-md transition-all flex flex-col justify-between border-t-4 border-t-[#9E7D2B]">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-lg bg-[#FFFFFF] border border-[#DFD7C5] flex items-center justify-center text-[#6B1D2F]">
                <Building2 className="w-6 h-6 text-[#C29B38]" />
              </div>
              <h3 className="font-serif text-xl font-bold text-[#6B1D2F]">
                About the System
              </h3>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                Institutional background, problem definition, why judicial case analytics matter for court administration, and our responsible AI framework.
              </p>
              <div className="text-[11px] font-semibold text-[#9E7D2B] bg-[#FFFFFF] p-2 rounded border border-[#DFD7C5]">
                Reference: Indian High Courts & eCourts Portal
              </div>
            </div>
            <Link
              to="/about"
              className="mt-6 inline-flex items-center text-xs font-bold text-[#6B1D2F] group-hover:text-[#80182A]"
            >
              Read Institutional Mandate <ArrowRight className="w-3.5 h-3.5 ml-1 text-[#9E7D2B]" />
            </Link>
          </div>
        </div>
      </section>

      {/* 4. VERIFIED BENCHMARK SUMMARY STRIP */}
      <section className="bg-[#FAF7EE] border-t border-[#DFD7C5] py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-5 space-y-3">
              <span className="text-xs uppercase font-bold text-[#9E7D2B] tracking-wider">
                EMPIRICAL VERIFICATION
              </span>
              <h2 className="font-serif text-2xl sm:text-3xl font-bold text-[#6B1D2F]">
                Real District Court Data · Zero Synthetic Fabrication
              </h2>
              <p className="text-xs text-[#4A5568] leading-relaxed">
                All metrics are computed strictly on genuine district court filings. Pending matters are never assigned synthetic 
                disposal dates, preventing statistical leakage.
              </p>
            </div>
            <div className="lg:col-span-7 grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-[#FFFFFF] border border-[#DFD7C5] p-4 rounded-lg text-center">
                <div className="font-serif text-2xl font-bold text-[#6B1D2F]">100%</div>
                <div className="text-[11px] text-[#5A6270] mt-1 font-medium">Valid Identifiers (KL-*)</div>
              </div>
              <div className="bg-[#FFFFFF] border border-[#DFD7C5] p-4 rounded-lg text-center">
                <div className="font-serif text-2xl font-bold text-[#6B1D2F]">0</div>
                <div className="text-[11px] text-[#5A6270] mt-1 font-medium">Date Anomaly Violations</div>
              </div>
              <div className="bg-[#FFFFFF] border border-[#DFD7C5] p-4 rounded-lg text-center">
                <div className="font-serif text-2xl font-bold text-[#6B1D2F]">180</div>
                <div className="text-[11px] text-[#5A6270] mt-1 font-medium">Kerala Court Complexes</div>
              </div>
              <div className="bg-[#FFFFFF] border border-[#DFD7C5] p-4 rounded-lg text-center">
                <div className="font-serif text-2xl font-bold text-[#1E6B2A]">34.3%</div>
                <div className="text-[11px] text-[#5A6270] mt-1 font-medium">Variance Explained (R²)</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
