"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/common/Navbar";
import { FarmerAdvisoryTab } from "@/components/farmer/FarmerAdvisoryTab";
import { MicroRiskTab } from "@/components/risk_map/MicroRiskTab";
import { CommandCenterTab } from "@/components/command_center/CommandCenterTab";
import { LanguageCode } from "@/locales/i18n";

export default function Home() {
  const [currentTab, setCurrentTab] = useState<'advisory' | 'risk_map' | 'command_center'>('advisory');
  const [language, setLanguage] = useState<LanguageCode>('hi'); // Default Hindi for farmer-first demo
  const [lowBandwidth, setLowBandwidth] = useState(false);

  return (
    <div className={`min-h-screen ${lowBandwidth ? 'low-bandwidth-mode bg-white text-black' : 'bg-slate-950 text-slate-100'}`}>
      {/* Universal Top Navigation Header */}
      <Navbar
        currentTab={currentTab}
        setTab={setCurrentTab}
        language={language}
        setLanguage={setLanguage}
        lowBandwidth={lowBandwidth}
        setLowBandwidth={setLowBandwidth}
      />

      {/* Main Layer Views */}
      <main className="pb-16">
        {currentTab === 'advisory' && (
          <FarmerAdvisoryTab
            language={language}
            lowBandwidth={lowBandwidth}
          />
        )}

        {currentTab === 'risk_map' && (
          <MicroRiskTab
            language={language}
            lowBandwidth={lowBandwidth}
          />
        )}

        {currentTab === 'command_center' && (
          <CommandCenterTab
            language={language}
            lowBandwidth={lowBandwidth}
          />
        )}
      </main>

      {/* Low-Bandwidth / Rural Mode Notification Footer */}
      {lowBandwidth && (
        <footer className="fixed bottom-0 left-0 right-0 bg-black text-white text-center py-1.5 text-xs font-mono font-bold tracking-wider z-50">
          [LOW-BANDWIDTH RURAL TEXT MODE ACTIVE: COMPACT PAYLOADS, HIGH CONTRAST, ZERO EXTERNAL CDN]
        </footer>
      )}
    </div>
  );
}

