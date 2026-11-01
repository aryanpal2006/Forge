# KisanShield System Architecture & Data Flow

KisanShield is an enterprise-grade, climate-resilient agriculture intelligence and autonomous emergency logistics engine tailored for Indian smallholder farmers and district disaster management authorities.

---

## 1. High-Level System Architecture

```mermaid
flowchart TD
    subgraph DataCore ["Unified Data Core & Resilient Ingestion"]
        OM["Open-Meteo REST (Live Forecast)"]
        NASA["NASA POWER / IMD (30-Yr Climatology)"]
        NOAA["NOAA ONI Index (ENSO Tracker)"]
        SG["SoilGrids API (Soil Chemistry)"]
        S2["Copernicus Sentinel-2 (NDVI Tiles)"]
        AG["data.gov.in Agmarknet (Mandi Prices)"]
        Cache["Resilient Disk & Memory Cache + Bundled Fallbacks"]
        OM & NASA & NOAA & SG & S2 & AG --> Cache
    end

    subgraph LayerB ["Layer B: Micro-Location Risk & Yield Engine"]
        GridGen["1–5 km Hexagonal/Rect Grid Generator"]
        M_Drought["30-Day SPI Drought Probability Model"]
        M_Flood["Rainfall Intensity & DEM Slope Flood Model"]
        M_Heat["Crop Thermal Exceedance Heat Index"]
        M_Yield["Yield Deviation Model (90% CI Bands)"]
        Cache --> GridGen
        GridGen --> M_Drought & M_Flood & M_Heat & M_Yield
        GeoJSON["GeoJSON Risk Grid (/api/v1/risk/grid)"]
        M_Drought & M_Flood & M_Heat & M_Yield --> GeoJSON
    end

    subgraph LayerA ["Layer A: Multilingual Agri Advisory"]
        KB["ICAR Agronomic Knowledge Base (Markdown)"]
        RAG["RAG-Lite Top-K Rule Citation"]
        LLM["Grounded Gemini LLM / Deterministic Generator"]
        Guard["Grounding Guardrail (Zero Hallucination Validator)"]
        Voice["Web Speech STT / TTS Engine"]
        KB --> RAG
        Cache --> LLM
        RAG --> LLM
        LLM --> Guard
        Guard --> Voice
    end

    subgraph LayerC ["Layer C: Autonomous Relief Logistics Engine"]
        Sensors["Mock Suppliers, Fleet Telemetry, Road Graph"]
        AgentLoop["Tool-Calling Orchestration Loop (APScheduler)"]
        Router["NetworkX Dynamic Router (Hazard Polygon Avoidance)"]
        HITL["Human-in-the-Loop Officer Gate"]
        DB["SQLite / PostGIS Audit Ledger"]
        Sensors --> AgentLoop
        GeoJSON --> AgentLoop
        AgentLoop --> Router
        Router --> HITL
        HITL --> DB
    end

    subgraph Frontend ["Next.js 14 Responsive PWA UI"]
        UI_A["Farmer Portal (Chat, Voice, 7-Day Actions)"]
        UI_B["Micro-Climate Risk Explorer (Leaflet, Sliders, ENSO)"]
        UI_C["Command Center (Fleet Telemetry, Simulator, Reroutes)"]
    end

    Voice --> UI_A
    GeoJSON --> UI_B
    DB --> UI_C
    Router --> UI_C
```

---

## 2. Dynamic Mid-Transit Hazard Rerouting Flow (Layer C)

```mermaid
sequenceDiagram
    autonumber
    actor Officer as District Relief Officer
    participant Simulator as Disaster Simulator
    participant Agent as Autonomous Relief Agent
    participant Router as NetworkX Dynamic Router
    participant Fleet as Fleet Telemetry (BR-07-TR-3301)
    participant Audit as Audit Trail DB

    Simulator->>Agent: Inundation Event Detected (Darbhanga Kosi Breach)
    Agent->>Router: compute_safe_route(Origin, Destination, ActiveHazard)
    Router-->>Agent: Primary Safe Route (14.0 km)
    Agent->>Fleet: Dispatch Emergency De-Watering Pumps
    Fleet-->>Agent: In-Transit (Tracking: KS-DAR-63626)
    
    Note over Simulator,Agent: Mid-Transit Breach Emerges Across Active Corridor
    Simulator->>Agent: trigger_mid_transit_rerouting(Order_ID, NewHazardBbox)
    Agent->>Router: Recalculate shortest path severing inundated edge
    Router-->>Agent: Alternative Safe Bypass Route Computed (22.0 km)
    Agent->>Fleet: Transmit Real-Time Dynamic Reroute
    Agent->>Audit: Record Trigger, Blocked Edges, and New Route
    Officer->>Audit: Inspect Decision Transparency & Telemetry
```

---

## 3. Data Flow & Provenance Badging

Every alert and advisory in KisanShield explicitly carries provenance metadata:
1. **Weather**: Open-Meteo 7-day live API with 1-hour in-memory cache and bundled NASA POWER/IMD historical fallbacks.
2. **Mandi Prices**: data.gov.in Agmarknet API parsed with 15-day moving average and trend signals (`HOLD` vs `SELL NOW`).
3. **Soil Attributes**: SoilGrids REST endpoint with regional default profiles (Vertisols, Alluvial, Coastal).
4. **Satellite Vegetation**: Sentinel-2 MSI NDVI raster tiles with negative anomaly stress detection.
5. **Macro-Climate**: NOAA Oceanic Niño Index (ONI) tracking El Niño / La Niña phases and regional correlation coefficients.

