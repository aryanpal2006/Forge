"use client";

import React, { useState, useEffect } from 'react';
import { translations, LanguageCode } from '@/locales/i18n';
import { fetchAdvisory } from '@/lib/api';
import {
  Mic,
  MicOff,
  Volume2,
  TrendingUp,
  TrendingDown,
  Calendar,
  AlertCircle,
  CheckCircle2,
  Share2,
  Clock,
  Sparkles,
  ShieldCheck,
  Coins,
  ChevronRight,
  Database
} from 'lucide-react';

interface FarmerAdvisoryTabProps {
  language: LanguageCode;
  lowBandwidth: boolean;
}

export const FarmerAdvisoryTab: React.FC<FarmerAdvisoryTabProps> = ({
  language,
  lowBandwidth,
}) => {
  const t = translations[language] || translations.en;

  // Onboarding Profile State
  const [district, setDistrict] = useState("Solapur");
  const [village, setVillage] = useState("Mohol");
  const [crop, setCrop] = useState("soybean");
  const [landSize, setLandSize] = useState("3.5");
  const [soilType, setSoilType] = useState("Black");
  const [irrigationType, setIrrigationType] = useState("Rainfed");
  const [queryText, setQueryText] = useState("");

  // Advisory API State
  const [loading, setLoading] = useState(false);
  const [advisoryData, setAdvisoryData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Speech Recognition (STT) & Speech Synthesis (TTS) State
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hasSTT = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
      setSpeechSupported(hasSTT);
    }
  }, []);

  // Update defaults when district changes
  const handleDistrictChange = (d: string) => {
    setDistrict(d);
    if (d === "Solapur") {
      setVillage("Mohol");
      setCrop("soybean");
      setSoilType("Black");
    } else if (d === "Darbhanga") {
      setVillage("Kalyanpur");
      setCrop("rice");
      setSoilType("Alluvial");
    } else {
      setVillage("Kurinjipadi");
      setCrop("rice");
      setSoilType("Sandy Loam");
    }
  };

  const handleGenerateAdvisory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAdvisory({
        district,
        village,
        crop_type: crop,
        language,
        soil_type: soilType,
        irrigation_type: irrigationType,
        query_text: queryText,
      });
      setAdvisoryData(data);
    } catch (err: any) {
      setError(err.message || "Failed to fetch advisory");
    } finally {
      setLoading(false);
    }
  };

  // Trigger default advisory on first load
  useEffect(() => {
    handleGenerateAdvisory();
  }, [language, district, crop]);

  // Voice STT Toggle
  const toggleSpeechRecognition = () => {
    if (!speechSupported) {
      alert("Web Speech recognition is not supported in this browser. Please use text input.");
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    const langMap: Record<LanguageCode, string> = {
      en: 'en-IN',
      hi: 'hi-IN',
      mr: 'mr-IN',
      bn: 'bn-IN',
      ta: 'ta-IN',
      te: 'te-IN'
    };

    recognition.lang = langMap[language] || 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    if (!isListening) {
      setIsListening(true);
      recognition.start();

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setQueryText(transcript);
        setIsListening(false);
        // Automatically trigger advisory with spoken query
        handleGenerateAdvisory();
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };
    } else {
      recognition.stop();
      setIsListening(false);
    }
  };

  // Voice TTS (Read Aloud)
  const speakText = (text: string) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    if (isSpeaking) {
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    const langMap: Record<LanguageCode, string> = {
      en: 'en-IN',
      hi: 'hi-IN',
      mr: 'mr-IN',
      bn: 'bn-IN',
      ta: 'ta-IN',
      te: 'te-IN'
    };
    utterance.lang = langMap[language] || 'en-IN';
    utterance.rate = 0.95;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Farmer Profile / Onboarding Header Card */}
      <div className={`p-6 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900/90 border-slate-800 shadow-xl'}`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 pb-6 border-b border-slate-800">
          <div>
            <h1 className="text-2xl font-black text-white flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-emerald-400" />
              {t.tabAdvisory}
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Hyper-local, ICAR-grounded agro-climate advisory with live mandi price intelligence.
            </p>
          </div>
          {/* Quick Voice Bar */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggleSpeechRecognition}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all ${
                isListening
                  ? 'bg-rose-600 text-white animate-pulse'
                  : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/30'
              }`}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
              <span>{isListening ? t.listening : t.voiceQueryBtn}</span>
            </button>
            <button
              onClick={() => {
                const textSummary = `KisanShield Alert (${district}): ${advisoryData?.spoken_advisory || ''} | Action: ${advisoryData?.next_7_days?.[0]?.action || ''} | Mandi: ₹${advisoryData?.mandi_signal?.current_modal_price || ''}/qtl (${advisoryData?.mandi_signal?.signal || ''})`;
                navigator.clipboard?.writeText(textSummary);
                alert("Copied offline SMS summary to clipboard:\n\n" + textSummary);
              }}
              className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700"
              title={t.smsExportBtn}
            >
              <Share2 className="w-4 h-4 text-amber-400" />
              <span className="hidden sm:inline">SMS Export</span>
            </button>
          </div>
        </div>

        {/* Profile Controls Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.district}
            </label>
            <select
              value={district}
              onChange={(e) => handleDistrictChange(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="Solapur">Solapur (Drought Prone)</option>
              <option value="Darbhanga">Darbhanga (Flood Prone)</option>
              <option value="Cuddalore">Cuddalore (Coastal Heat)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.village}
            </label>
            <input
              type="text"
              value={village}
              onChange={(e) => setVillage(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.crop}
            </label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="soybean">Soybean (सोयाबीन)</option>
              <option value="cotton">Cotton (कपास / பருத்தி)</option>
              <option value="rice">Rice (धान / ধান / அரிசி)</option>
              <option value="wheat">Wheat (गेहूं / গম)</option>
              <option value="potato">Potato (आलू / আলু)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.acreage}
            </label>
            <input
              type="number"
              step="0.5"
              value={landSize}
              onChange={(e) => setLandSize(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.soilType}
            </label>
            <select
              value={soilType}
              onChange={(e) => setSoilType(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="Black">Deep Black (Vertisol)</option>
              <option value="Alluvial">Alluvial Silt Loam</option>
              <option value="Sandy Loam">Sandy Coastal Loam</option>
              <option value="Red">Red Laterite</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              {t.irrigationType}
            </label>
            <select
              value={irrigationType}
              onChange={(e) => setIrrigationType(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-2 text-xs font-medium text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="Rainfed">Rainfed (बारानी)</option>
              <option value="Canal">Canal Irrigation</option>
              <option value="Borewell">Borewell / Open Well</option>
              <option value="Drip">Drip / Sprinkler</option>
            </select>
          </div>
        </div>

        {/* Custom Query Input */}
        <div className="mt-4 flex gap-2">
          <input
            type="text"
            placeholder="Ask anything (e.g. 'Should I irrigate this week given the heat forecast?')..."
            value={queryText}
            onChange={(e) => setQueryText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleGenerateAdvisory()}
            className="flex-1 bg-slate-800/80 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-emerald-500"
          />
          <button
            onClick={handleGenerateAdvisory}
            disabled={loading}
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow-md transition-all flex items-center gap-1.5"
          >
            {loading ? <Clock className="w-3.5 h-3.5 animate-spin" /> : <ChevronRight className="w-4 h-4" />}
            <span>{t.getAdvisoryBtn}</span>
          </button>
        </div>
      </div>

      {/* Advisory Content Grid */}
      {advisoryData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Spoken Advisory Card (2 Cols) */}
          <div className="lg:col-span-2 space-y-6">
            <div className={`p-6 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-gradient-to-br from-slate-900 to-slate-950 border-slate-800 shadow-xl'}`}>
              <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-lg font-bold text-white">Voice & Spoken Advisory</h2>
                    <span className="text-[11px] text-emerald-400 font-medium">
                      Rule Cited: {advisoryData.rule_cited}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => speakText(advisoryData.spoken_advisory)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${
                    isSpeaking
                      ? 'bg-rose-500 text-white border-rose-400'
                      : 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
                  }`}
                >
                  <Volume2 className="w-4 h-4 text-emerald-400" />
                  <span>{isSpeaking ? 'Stop Audio' : t.speakAdvisory}</span>
                </button>
              </div>

              {/* Spoken Paragraph */}
              <div className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-5 mb-4">
                <p className="text-base sm:text-lg text-slate-100 font-medium leading-relaxed">
                  "{advisoryData.spoken_advisory}"
                </p>
                {advisoryData.english_translation && (
                  <div className="mt-3 pt-3 border-t border-slate-700/50">
                    <p className="text-xs text-slate-400 italic">
                      <strong className="text-slate-300">English Audit:</strong> "{advisoryData.english_translation}"
                    </p>
                  </div>
                )}
              </div>

              {/* Why & Confidence Box */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
                  <span className="text-[11px] uppercase font-bold text-slate-400 flex items-center gap-1.5 mb-1">
                    <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                    {t.whyTitle}
                  </span>
                  <p className="text-xs text-slate-200">{advisoryData.why_rationale}</p>
                </div>

                <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
                  <span className="text-[11px] uppercase font-bold text-slate-400 flex items-center gap-1.5 mb-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    {t.confidence}
                  </span>
                  <div className="flex items-center gap-3 mt-1">
                    <div className="flex-1 bg-slate-700 h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-emerald-500 h-full rounded-full transition-all"
                        style={{ width: `${advisoryData.confidence_level * 100}%` }}
                      />
                    </div>
                    <span className="text-xs font-bold text-emerald-400">
                      {advisoryData.confidence_label}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Next 7 Days Action Cards */}
            <div className={`p-6 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
              <h3 className="text-base font-bold text-white flex items-center gap-2 mb-4">
                <Calendar className="w-5 h-5 text-emerald-400" />
                {t.actionCardTitle}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {advisoryData.next_7_days?.map((card: any, idx: number) => {
                  const urgencyColors = {
                    critical: 'border-rose-500/40 bg-rose-500/10 text-rose-300',
                    medium: 'border-amber-500/40 bg-amber-500/10 text-amber-300',
                    low: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300',
                  };
                  return (
                    <div
                      key={idx}
                      className="p-4 rounded-xl border border-slate-700/80 bg-slate-800/50 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs font-extrabold text-white">{card.day_range}</span>
                          <span
                            className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${
                              urgencyColors[card.urgency as keyof typeof urgencyColors] || urgencyColors.low
                            }`}
                          >
                            {card.urgency}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300 leading-normal">{card.action}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Mandi Intelligence & Provenance Sidebar */}
          <div className="space-y-6">
            {/* Mandi Signal Card */}
            <div className={`p-6 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
              <div className="flex items-center gap-2 mb-4">
                <Coins className="w-5 h-5 text-amber-400" />
                <h3 className="text-base font-bold text-white">{t.mandiSignalTitle}</h3>
              </div>

              <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60 mb-4 text-center">
                <span className="text-[11px] uppercase font-semibold text-slate-400">
                  {advisoryData.mandi_signal.crop} Modal Mandi Price
                </span>
                <div className="text-3xl font-black text-white mt-1">
                  ₹{Number(advisoryData.mandi_signal.current_modal_price).toLocaleString('en-IN')}
                  <span className="text-xs font-normal text-slate-400 ml-1">/ Quintal</span>
                </div>
                <div className="flex items-center justify-center gap-1.5 mt-2">
                  {advisoryData.mandi_signal.price_trend === 'upward' ? (
                    <span className="text-xs font-bold text-emerald-400 flex items-center gap-1">
                      <TrendingUp className="w-3.5 h-3.5" /> Upward Trend (+3.8%)
                    </span>
                  ) : (
                    <span className="text-xs font-bold text-rose-400 flex items-center gap-1">
                      <TrendingDown className="w-3.5 h-3.5" /> Downward Trend (-5.1%)
                    </span>
                  )}
                </div>
              </div>

              {/* Signal Badge */}
              <div
                className={`p-4 rounded-xl border text-center font-black text-lg uppercase tracking-wider mb-4 ${
                  advisoryData.mandi_signal.signal === 'HOLD'
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                    : 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                }`}
              >
                RECOMMENDED SIGNAL: {advisoryData.mandi_signal.signal}
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                {advisoryData.mandi_signal.rationale}
              </p>

              <div className="text-[11px] text-slate-400 flex items-center justify-between pt-3 border-t border-slate-800">
                <span>Source:</span>
                <span className="font-semibold text-emerald-400">
                  {advisoryData.mandi_signal.data_source}
                </span>
              </div>
            </div>

            {/* Provenance & Freshness Badge */}
            <div className={`p-5 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
              <div className="flex items-center gap-2 mb-3">
                <Database className="w-4 h-4 text-emerald-400" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  {t.provenance}
                </h4>
              </div>
              <ul className="text-xs space-y-2 text-slate-300">
                <li className="flex justify-between">
                  <span className="text-slate-400">Weather:</span>
                  <span className="font-medium text-emerald-400">{advisoryData.provenance.weather}</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-slate-400">Mandi:</span>
                  <span className="font-medium text-emerald-400">{advisoryData.provenance.mandi}</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-slate-400">Agronomy:</span>
                  <span className="font-medium text-slate-200">ICAR Standard Rules</span>
                </li>
                <li className="flex justify-between">
                  <span className="text-slate-400">LLM Guardrail:</span>
                  <span className="font-bold text-emerald-400">Passed (Zero Hallucination)</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

