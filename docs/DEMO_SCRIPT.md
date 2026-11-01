# KisanShield: 3-Minute Hackathon Demo Script

**Theme**: Climate & Supply-Chain Resilience for Indian Smallholder Agriculture  
**Presenter Flow**: Mobile Farmer Voice -> Micro-Climate Risk Grid -> Autonomous Relief Agent -> Command Center Audit

---

### [00:00 - 00:45] Act 1: The Smallholder Voice Experience (Layer A)
1. **Introduction**:
   > *"Meet Ramesh Patil, a soybean farmer in Solapur, Maharashtra. In rural India, complex meteorological charts fail smallholders. Ramesh needs immediate, trusted answers in his language."*
2. **Action**:
   - Open KisanShield at `http://localhost:3000`.
   - Select **मराठी (Marathi)** or **हिंदी (Hindi)** from the language dropdown.
   - Click the microphone icon (or trigger text advisory).
3. **Observation**:
   - The system responds in concise, spoken-friendly format (under 80 words).
   - Click **"सलाह सुनें / Read Aloud"** to demonstrate Web Speech TTS playing in native audio.
   - Show the **"Next 7 Days Action Card"** (mulching on Day 1-2, foliar spray on Day 3-4).
   - Point out the **Mandi Intelligence Card**: shows ₹4,650/qtl with an upward trend and the explicit recommendation to **"HOLD"** inventory for 2 weeks to avoid harvest dips.
   - Highlight the **Data Freshness & Provenance** badge citing ICAR guidelines and verified Agmarknet data.

---

### [00:45 - 01:45] Act 2: Micro-Location Climate & Yield Risk Explorer (Layer B)
1. **Transition**:
   > *"Behind Ramesh's advisory is our micro-climate risk engine that analyzes 1–5 km grid cells combining Open-Meteo forecasts, SoilGrids chemistry, Sentinel-2 NDVI anomalies, and NOAA's El Niño ONI index."*
2. **Action**:
   - Click the **"Micro-Climate Risk"** tab.
   - Switch district between **Solapur** (drought-prone Vertisol), **Darbhanga** (flood-prone alluvial plains), and **Cuddalore** (coastal heat).
   - Toggle layers: **Drought Probability**, **Flash-Flood Risk**, **Heatwave Stress**, and **NDVI Vegetation Health**.
   - Move the **Forecast Horizon Slider** from Day 1 to Day 14.
3. **Observation**:
   - Click any micro-grid cell: a popup shows the exact yield impact deviation (e.g., `-17.2%`) along with honest **90% confidence uncertainty intervals** `[-22.4%, -12.0%]`.
   - Point to the **AI Agronomic Mitigation Plan**: suggests drought-hardy crop switching (Rabi Sorghum / Chickpea) and PMFBY weather insurance claim triggers.
   - Highlight the **NOAA ONI Index** widget correlating historical El Niño cycles with monsoon deficits.

---

### [01:45 - 02:45] Act 3: Autonomous Emergency Response & Dynamic Rerouting (Layer C)
1. **Transition**:
   > *"When climate forecasts predict imminent catastrophe, KisanShield doesn't just display a warning—it acts autonomously."*
2. **Action**:
   - Click the **"Emergency Command Center"** tab.
   - Show the live Leaflet map with 8 relief fleet vehicles (water tankers, 4x4 trucks, emergency pumps) and 10 stocked suppliers.
   - Click **"Trigger Flash Flood (Darbhanga)"** in the Disaster Simulator.
3. **Observation**:
   - The autonomous agent executes its 6-step tool loop: evaluates risk cells -> queries inventory -> matches vehicle `BR-07-TR-3301` -> computes safe route -> places dispatch order.
   - Now click **"Simulate Hazard Breach & Reroute"**:
     - A new flood inundation polygon emerges on the map.
     - NetworkX dynamically severs the flooded road and recalculates a safe bypass route in real time.
     - The dispatch order badge updates to **"REROUTED x1"** with green bypass telemetry.
   - Demonstrate **Human-in-the-Loop (HITL)**: for orders exceeding ₹50,000, click **"Approve Dispatch"** to sign off as the District Relief Officer.

---

### [02:45 - 03:00] Act 4: Audit Trail & Resilience Recap
1. **Action**:
   - Expand the **Audit Log Drawer** on the right side.
   - Show judges the complete transparent trace: trigger reason, inputs, tool executions (`compute_safe_route`, `create_dispatch_order`), and timestamps.
2. **Closing Statement**:
   > *"KisanShield bridges the last-mile gap: protecting farmer livelihood with grounded multilingual voice advice, and safeguarding the agricultural supply chain with autonomous, transparent disaster relief."*

