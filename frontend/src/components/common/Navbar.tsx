"use client";

import React from 'react';
import { translations, LanguageCode } from '@/locales/i18n';
import { ShieldCheck, Wifi, WifiOff, Globe, Map, Radio, Sparkles } from 'lucide-react';

interface NavbarProps {
  currentTab: 'advisory' | 'risk_map' | 'command_center';
  setTab: (tab: 'advisory' | 'risk_map' | 'command_center') => void;
  language: LanguageCode;
  setLanguage: (lang: LanguageCode) => void;
  lowBandwidth: boolean;
  setLowBandwidth: (val: boolean) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setTab,
  language,
  setLanguage,
  lowBandwidth,
  setLowBandwidth,
}) => {
  const t = translations[language] || translations.en;

  const languages: { code: LanguageCode; label: string }[] = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'हिंदी (Hindi)' },
    { code: 'mr', label: 'मराठी (Marathi)' },
    { code: 'bn', label: 'বাংলা (Bengali)' },
    { code: 'ta', label: 'தமிழ் (Tamil)' },
    { code: 'te', label: 'తెలుగు (Telugu)' },
  ];

  return (
    <header className={`border-b sticky top-0 z-50 ${lowBandwidth ? 'bg-white border-black text-black' : 'bg-slate-900 border-slate-800 text-white backdrop-blur-md bg-opacity-95'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Name */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setTab('advisory')}>
            <div className={`p-2 rounded-xl flex items-center justify-center ${lowBandwidth ? 'bg-black text-white' : 'bg-emerald-500 text-slate-950 font-bold shadow-lg shadow-emerald-500/20'}`}>
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xl tracking-tight text-white">{t.appName}</span>
                <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full ${lowBandwidth ? 'border border-black' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'}`}>
                  India MVP
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden md:block">
                {t.tagline}
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex space-x-1 sm:space-x-2 bg-slate-800/60 p-1 rounded-xl border border-slate-700/50">
            <button
              onClick={() => setTab('advisory')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'advisory'
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{t.tabAdvisory}</span>
            </button>
            <button
              onClick={() => setTab('risk_map')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'risk_map'
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Map className="w-3.5 h-3.5" />
              <span>{t.tabRiskMap}</span>
            </button>
            <button
              onClick={() => setTab('command_center')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'command_center'
                  ? 'bg-rose-600 text-white shadow-md animate-pulse'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Radio className="w-3.5 h-3.5" />
              <span>{t.tabCommandCenter}</span>
            </button>
          </nav>

          {/* Controls: Language & Low Bandwidth Toggle */}
          <div className="flex items-center space-x-3">
            {/* Language Selector */}
            <div className="flex items-center space-x-1 bg-slate-800/80 px-2 py-1 rounded-lg border border-slate-700">
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value as LanguageCode)}
                className="bg-transparent text-xs text-white focus:outline-none cursor-pointer"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code} className="bg-slate-900 text-white">
                    {l.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Low-Bandwidth Toggle */}
            <button
              onClick={() => setLowBandwidth(!lowBandwidth)}
              title={t.lowBandwidth}
              className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors ${
                lowBandwidth
                  ? 'bg-amber-400 text-slate-950 border-amber-300'
                  : 'bg-slate-800 text-slate-300 border-slate-700 hover:text-white'
              }`}
            >
              {lowBandwidth ? <WifiOff className="w-3.5 h-3.5" /> : <Wifi className="w-3.5 h-3.5 text-emerald-400" />}
              <span className="hidden sm:inline">{lowBandwidth ? 'Rural Text' : 'Fast Mode'}</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

