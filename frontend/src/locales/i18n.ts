export type LanguageCode = 'en' | 'hi' | 'bn' | 'mr' | 'ta' | 'te';

export interface TranslationDictionary {
  appName: string;
  tagline: string;
  tabAdvisory: string;
  tabRiskMap: string;
  tabCommandCenter: string;
  lowBandwidth: string;
  selectLanguage: string;
  district: string;
  village: string;
  crop: string;
  acreage: string;
  soilType: string;
  irrigationType: string;
  getAdvisoryBtn: string;
  voiceQueryBtn: string;
  listening: string;
  speakAdvisory: string;
  actionCardTitle: string;
  mandiSignalTitle: string;
  whyTitle: string;
  confidence: string;
  provenance: string;
  riskGridTitle: string;
  layerToggles: string;
  droughtLayer: string;
  floodLayer: string;
  heatLayer: string;
  ndviLayer: string;
  timeSlider: string;
  mitigationPlanTitle: string;
  ensoTitle: string;
  commandCenterTitle: string;
  fleetStatus: string;
  activeOrders: string;
  simulatorTitle: string;
  simulateFlood: string;
  simulateDrought: string;
  simulateReroute: string;
  auditLogTitle: string;
  approveBtn: string;
  smsExportBtn: string;
}

export const translations: Record<LanguageCode, TranslationDictionary> = {
  en: {
    appName: "KisanShield",
    tagline: "Climate-Resilient Agri Advisory + Autonomous Relief Engine",
    tabAdvisory: "Farmer Advisory",
    tabRiskMap: "Micro-Climate Risk",
    tabCommandCenter: "Emergency Command Center",
    lowBandwidth: "Low-Bandwidth Mode",
    selectLanguage: "Language",
    district: "District",
    village: "Village",
    crop: "Crop",
    acreage: "Land Size (Acres)",
    soilType: "Soil Type",
    irrigationType: "Irrigation Type",
    getAdvisoryBtn: "Generate Advisory",
    voiceQueryBtn: "Speak in Your Language",
    listening: "Listening... Speak now",
    speakAdvisory: "Read Aloud",
    actionCardTitle: "Next 7 Days Action Card",
    mandiSignalTitle: "Mandi Price Intelligence & Sell/Hold Signal",
    whyTitle: "Why This Advisory?",
    confidence: "Confidence Level",
    provenance: "Data Freshness & Provenance",
    riskGridTitle: "Hyper-Local Risk Grid (1–5 km)",
    layerToggles: "Hazard Layers",
    droughtLayer: "Drought Probability",
    floodLayer: "Flash-Flood Risk",
    heatLayer: "Heatwave Stress",
    ndviLayer: "NDVI Vegetation Stress",
    timeSlider: "Forecast Horizon (Days)",
    mitigationPlanTitle: "AI Agronomic Mitigation Plan",
    ensoTitle: "ENSO Oceanic Niño Index (ONI)",
    commandCenterTitle: "Autonomous Relief Logistics Command Center",
    fleetStatus: "Live Relief Fleet Telemetry",
    activeOrders: "Emergency Dispatch Orders",
    simulatorTitle: "Disaster Event Simulator",
    simulateFlood: "Trigger Flash Flood (Darbhanga)",
    simulateDrought: "Trigger Severe Drought (Solapur)",
    simulateReroute: "Simulate Hazard Breach & Reroute",
    auditLogTitle: "Agent Tool-Calling Audit Trail",
    approveBtn: "Approve Dispatch",
    smsExportBtn: "Export Offline SMS Card"
  },
  hi: {
    appName: "किसानशील्ड",
    tagline: "जलवायु-सक्षम कृषि सलाह + स्वायत्त राहत प्रणाली",
    tabAdvisory: "किसान सलाह",
    tabRiskMap: "सूक्ष्म-जलवायु जोखिम",
    tabCommandCenter: "आपातकालीन राहत केंद्र",
    lowBandwidth: "कम-बैंडविड्थ मोड",
    selectLanguage: "भाषा",
    district: "जिला",
    village: "गांव",
    crop: "फसल",
    acreage: "जमीन (एकड़)",
    soilType: "मिट्टी का प्रकार",
    irrigationType: "सिंचाई का साधन",
    getAdvisoryBtn: "सलाह प्राप्त करें",
    voiceQueryBtn: "अपनी भाषा में बोलें",
    listening: "सुन रहे हैं... बोलिए",
    speakAdvisory: "सलाह सुनें",
    actionCardTitle: "अगले 7 दिनों की कार्य योजना",
    mandiSignalTitle: "मंडी भाव व बिक्री संकेत",
    whyTitle: "यह सलाह क्यों?",
    confidence: "सटीकता स्तर",
    provenance: "डेटा स्रोत व ताज़गी",
    riskGridTitle: "अति-स्थानीय जोखिम ग्रिड (1–5 किमी)",
    layerToggles: "आपदा परतें",
    droughtLayer: "सूखा संभावना",
    floodLayer: "बाढ़ जोखिम",
    heatLayer: "लू / ताप तनाव",
    ndviLayer: "वनस्पति स्वास्थ्य (NDVI)",
    timeSlider: "पूर्वानुमान दिन",
    mitigationPlanTitle: "कृषि सुरक्षा व अनुकूलन योजना",
    ensoTitle: "अल नीनो / ला नीना सूचकांक (ONI)",
    commandCenterTitle: "स्वायत्त राहत रसद नियंत्रण कक्ष",
    fleetStatus: "राहत वाहनों की लाइव स्थिति",
    activeOrders: "आपातकालीन आपूर्ति आदेश",
    simulatorTitle: "आपदा सिमुलेटर",
    simulateFlood: "बाढ़ सिमुलेट करें (दरभंगा)",
    simulateDrought: "सूखा सिमुलेट करें (सोलापुर)",
    simulateReroute: "मार्ग अवरोध व पुनः मार्ग निर्धारण",
    auditLogTitle: "एजेंट ऑडिट लॉग",
    approveBtn: "आदेश स्वीकृत करें",
    smsExportBtn: "ऑफ़लाइन SMS कार्ड डाउनलोड करें"
  },
  bn: {
    appName: "কিষাণশিল্ড",
    tagline: "জলবায়ু-সহনশীল কৃষি পরামর্শ ও স্বায়ত্তশাসিত ত্রাণ ইঞ্জিন",
    tabAdvisory: "কৃষক পরামর্শ",
    tabRiskMap: "জলবায়ু ঝুঁকি মানচিত্র",
    tabCommandCenter: "জরুরি ত্রাণ কমান্ড সেন্টার",
    lowBandwidth: "কম-ব্যান্ডউইথ মোড",
    selectLanguage: "ভাষা",
    district: "জেলা",
    village: "গ্রাম",
    crop: "ফসল",
    acreage: "জমির পরিমাণ (একর)",
    soilType: "মাটির ধরন",
    irrigationType: "সেচের ব্যবস্থা",
    getAdvisoryBtn: "পরামর্শ পান",
    voiceQueryBtn: "আপনার ভাষায় বলুন",
    listening: "শুনছি... বলুন",
    speakAdvisory: "পরামর্শ শুনুন",
    actionCardTitle: "পরবর্তী ৭ দিনের কর্মপরিকল্পনা",
    mandiSignalTitle: "মান্ডি দর ও বিক্রি সংকেত",
    whyTitle: "কেন এই পরামর্শ?",
    confidence: "নির্ভুলতার স্তর",
    provenance: "উৎস ও তথ্যের সতেজতা",
    riskGridTitle: "স্থানীয় ঝুঁকি গ্রিড (১–৫ কিমি)",
    layerToggles: "ঝুঁকি স্তর",
    droughtLayer: "খরা সম্ভাবনা",
    floodLayer: "বন্যা ঝুঁকি",
    heatLayer: "তাপপ্রবাহ চাপ",
    ndviLayer: "সবুজায়ন সূচক (NDVI)",
    timeSlider: "পূর্বাভাস সময়সীমা",
    mitigationPlanTitle: "কৃষি সুরক্ষা পরিকল্পনা",
    ensoTitle: "এল নিনো / লা নিনা সূচক (ONI)",
    commandCenterTitle: "ত্রাণ লজিস্টিক কমান্ড সেন্টার",
    fleetStatus: "ত্রাণ যানের অবস্থান",
    activeOrders: "সক্রিয় সরবরাহ আদেশ",
    simulatorTitle: "দুর্যোগ সিমুলেটর",
    simulateFlood: "বন্যা সিমুলেশন (দ্বারভাঙা)",
    simulateDrought: "খরা সিমুলেশন (সোলাপুর)",
    simulateReroute: "পথ পরিবর্তন সিমুলেশন",
    auditLogTitle: "এজেন্ট অডিট লগ",
    approveBtn: "অনুমোদন করুন",
    smsExportBtn: "অফলাইন SMS কার্ড"
  },
  mr: {
    appName: "किसानशील्ड",
    tagline: "हवामान-सक्षम कृषी सल्ला व स्वायत्त आपत्कालीन मदत प्रणाली",
    tabAdvisory: "शेतकरी सल्ला",
    tabRiskMap: "हवामान व पीक जोखीम",
    tabCommandCenter: "आपत्कालीन नियंत्रण कक्ष",
    lowBandwidth: "कमी-बँडविड्थ मोड",
    selectLanguage: "भाषा",
    district: "जिल्हा",
    village: "गाव",
    crop: "पीक",
    acreage: "जमीन (एकर)",
    soilType: "मातीचा प्रकार",
    irrigationType: "सिंचनाचा प्रकार",
    getAdvisoryBtn: "सल्ला मिळवा",
    voiceQueryBtn: "मराठीत बोला",
    listening: "ऐकत आहे... बोला",
    speakAdvisory: "सल्ला ऐका",
    actionCardTitle: "पुढील ७ दिवसांचे कृती कार्ड",
    mandiSignalTitle: "बाजारभाव व विक्री/साठा सिग्नल",
    whyTitle: "हा सल्ला का?",
    confidence: "विश्वासार्हता पातळी",
    provenance: "माहिती स्रोत व ताजेपणा",
    riskGridTitle: "अति-स्थानिक जोखीम ग्रिड (१–५ किमी)",
    layerToggles: "आपत्ती थर",
    droughtLayer: "दुष्काळ संभाव्यता",
    floodLayer: "पूर जोखीम",
    heatLayer: "उष्णतेचा ताण",
    ndviLayer: "पीक आरोग्य (NDVI)",
    timeSlider: "पूर्वानुमान दिवस",
    mitigationPlanTitle: "कृषी उपाययोजना आराखडा",
    ensoTitle: "एल निनो / ला निना स्थिती (ONI)",
    commandCenterTitle: "स्वायत्त मदत व वाहतूक नियंत्रण कक्ष",
    fleetStatus: "मदत वाहनांची थेट स्थिती",
    activeOrders: "तातडीचे पुरवठा आदेश",
    simulatorTitle: "आपत्ती सिम्युलेटर",
    simulateFlood: "पूर आपत्ती सिम्युलेट करा (दरभंगा)",
    simulateDrought: "दुष्काळ सिम्युलेट करा (सोलापूर)",
    simulateReroute: "मार्ग अडथळा व पर्यायी मार्ग",
    auditLogTitle: "ऑडिट लॉग",
    approveBtn: "मंजूरी द्या",
    smsExportBtn: "ऑफलाइन SMS कार्ड"
  },
  ta: {
    appName: "கிசான்ஷீல்ட்",
    tagline: "காலநிலை தாங்கும் வேளாண் ஆலோசனை + தன்னியக்க நிவாரண இயந்திரம்",
    tabAdvisory: "விவசாயி ஆலோசனை",
    tabRiskMap: "நுண் காலநிலை இடர் வரைபடம்",
    tabCommandCenter: "நிவாரண கட்டுப்பாட்டு மையம்",
    lowBandwidth: "குறைந்த இணைய வேகம்",
    selectLanguage: "மொழி",
    district: "மாவட்டம்",
    village: "கிராமம்",
    crop: "பயிர்",
    acreage: "நிலப்பரப்பு (ஏக்கர்)",
    soilType: "மண் வகை",
    irrigationType: "பாசன முறை",
    getAdvisoryBtn: "ஆலோசனை பெறுக",
    voiceQueryBtn: "குரல் மூலம் பேசுக",
    listening: "கேட்கிறது... பேசவும்",
    speakAdvisory: "ஒலி வடிவில் கேட்க",
    actionCardTitle: "அடுத்த 7 நாட்கள் செயல் அட்டை",
    mandiSignalTitle: "சந்தை விலை மற்றும் விற்பனை சமிஞ்கை",
    whyTitle: "இந்த ஆலோசனையின் காரணம்",
    confidence: "நம்பகத்தன்மை",
    provenance: "தரவு ஆதாரம்",
    riskGridTitle: "நுண் இடர் கட்டமைப்பு (1–5 கி.மீ)",
    layerToggles: "இடர் அடுக்குகள்",
    droughtLayer: "வறட்சி சாத்தியம்",
    floodLayer: "வெள்ள இடர்",
    heatLayer: "வெப்ப அலை அழுத்தம்",
    ndviLayer: "பயிர் பசுமை குறியீடு (NDVI)",
    timeSlider: "முன்னறிவிப்பு நாட்கள்",
    mitigationPlanTitle: "பயிர் பாதுகாப்பு திட்டம்",
    ensoTitle: "எல் நினோ / லா நினா குறியீடு (ONI)",
    commandCenterTitle: "தன்னியக்க நிவாரண கட்டுப்பாட்டு மையம்",
    fleetStatus: "நிவாரண வாகனங்களின் நிலை",
    activeOrders: "அவசர நிவாரண ஆணைகள்",
    simulatorTitle: "பேரிடர் மாதிரி கருவி",
    simulateFlood: "வெள்ள மாதிரி (தர்பாங்கா)",
    simulateDrought: "வறட்சி மாதிரி (சோலாப்பூர்)",
    simulateReroute: "மறுபாதை மாற்றுதல்",
    auditLogTitle: "செயல்பாட்டு பதிவு",
    approveBtn: "ஒப்புதல் அளி",
    smsExportBtn: "SMS அட்டை சேமி"
  },
  te: {
    appName: "కిసాన్‌షీల్డ్",
    tagline: "వాతావరణ తట్టుకునే వ్యవసాయ సలహా + స్వయంప్రతిపత్తి సహాయ ఇంజిన్",
    tabAdvisory: "రైతు సలహా",
    tabRiskMap: "సూక్ష్మ వాతావరణ ముప్పు",
    tabCommandCenter: "అత్యవసర కమాండ్ సెంటర్",
    lowBandwidth: "తక్కువ ఇంటర్నెట్ మోడ్",
    selectLanguage: "భాష",
    district: "జిల్లా",
    village: "గ్రామం",
    crop: "పంట",
    acreage: "భూమి విస్తీర్ణం (ఎకరాలు)",
    soilType: "నేల రకం",
    irrigationType: "నీటిపారుదల పద్ధతి",
    getAdvisoryBtn: "సలహా పొందండి",
    voiceQueryBtn: "మీ భాషలో మాట్లాడండి",
    listening: "వింటున్నాము... మాట్లాడండి",
    speakAdvisory: "సలహా వినండి",
    actionCardTitle: "రాబోయే 7 రోజుల ప్రణాళిక",
    mandiSignalTitle: "మార్కెట్ ధర & అమ్మకం సూచన",
    whyTitle: "ఈ సలహా ఎందుకు?",
    confidence: "ఖచ్చితత్వం",
    provenance: "డేటా మూలం",
    riskGridTitle: "సూక్ష్మ రిస్క్ గ్రిడ్ (1–5 కి.మీ)",
    layerToggles: "ముప్పు లేయర్లు",
    droughtLayer: "కరువు సంభావ్యత",
    floodLayer: "వరద ముప్పు",
    heatLayer: "ఎండవేడిమి ఒత్తిడి",
    ndviLayer: "పైరు ఆరోగ్యం (NDVI)",
    timeSlider: "అంచనా రోజులు",
    mitigationPlanTitle: "పంట సంరక్షణ ప్రణాళిక",
    ensoTitle: "ఎల్ నినో / లా నినా సూచిక (ONI)",
    commandCenterTitle: "అత్యవసర సరఫరా కమాండ్ సెంటర్",
    fleetStatus: "వాహనాల తాజా సమాచారం",
    activeOrders: "సరఫరా ఆదేశాలు",
    simulatorTitle: "విపత్తు సిమ్యులేటర్",
    simulateFlood: "వరద ముప్పు సృష్టించు (దర్భంగా)",
    simulateDrought: "కరువు ముప్పు సృష్టించు (సోలాపూర్)",
    simulateReroute: "రహదారి మళ్లింపు",
    auditLogTitle: "ఆడిట్ లాగ్",
    approveBtn: "ఆమోదించండి",
    smsExportBtn: "ఆఫ్‌లైన్ SMS కార్డ్"
  }
};

