"use client";

import React, { useState, useEffect } from 'react';
import { translations, LanguageCode } from '@/locales/i18n';
import {
  fetchFleet,
  fetchOrders,
  fetchAuditLogs,
  simulateEmergency,
  triggerReroute,
  approveOrder,
} from '@/lib/api';
import { LeafletCommandMap } from '@/components/command_center/LeafletCommandMap';
import {
  Radio,
  Truck,
  AlertTriangle,
  Play,
  RotateCw,
  CheckCircle,
  Clock,
  Terminal,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  MapPin,
  ExternalLink
} from 'lucide-react';

interface CommandCenterTabProps {
  language: LanguageCode;
  lowBandwidth: boolean;
}

export const CommandCenterTab: React.FC<CommandCenterTabProps> = ({
  language,
  lowBandwidth,
}) => {
  const t = translations[language] || translations.en;

  const [district, setDistrict] = useState("darbhanga");
  const [fleet, setFleet] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [activeHazardBbox, setActiveHazardBbox] = useState<number[] | null>(null);

  // Expanded audit log state
  const [expandedLogId, setExpandedLogId] = useState<number | null>(null);

  const refreshData = async () => {
    try {
      const [f, o, a] = await Promise.all([
        fetchFleet(),
        fetchOrders(district),
        fetchAuditLogs(district),
      ]);
      setFleet(f);
      setOrders(o);
      setAuditLogs(a);
    } catch (err) {
      console.error("Failed to refresh command center data:", err);
    }
  };

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 12000); // Poll telemetry every 12s
    return () => clearInterval(interval);
  }, [district]);

  // Handler: Trigger Flash Flood Simulation
  const handleTriggerFlood = async () => {
    setSimulating(true);
    setDistrict("darbhanga");
    try {
      const res = await simulateEmergency("darbhanga", "FLASH_FLOOD", 0.90);
      alert(`Simulation Triggered: Flash flood detected in Darbhanga!\n\nAgent Plan: Assigned relief equipment and dispatched order ${res.dispatch_order?.tracking_number}.`);
      await refreshData();
    } catch (err: any) {
      alert("Simulation failed: " + err.message);
    } finally {
      setSimulating(false);
    }
  };

  // Handler: Trigger Severe Drought Simulation
  const handleTriggerDrought = async () => {
    setSimulating(true);
    setDistrict("solapur");
    try {
      const res = await simulateEmergency("solapur", "SEVERE_DROUGHT", 0.85);
      alert(`Simulation Triggered: Severe drought spell detected in Solapur!\n\nAgent Plan: Dispatched potable water tanker ${res.dispatch_order?.tracking_number} to Mohol.`);
      await refreshData();
    } catch (err: any) {
      alert("Simulation failed: " + err.message);
    } finally {
      setSimulating(false);
    }
  };

  // Handler: Simulate Mid-Transit Hazard Breach & Dynamic Rerouting
  const handleTriggerReroute = async () => {
    setSimulating(true);
    try {
      // Inundated hazard polygon coordinates
      const floodBbox = [85.90, 26.13, 85.93, 26.16];
      setActiveHazardBbox(floodBbox);
      const res = await triggerReroute(orders[0]?.id, district);
      alert(`Dynamic Rerouting Triggered!\n\nNew hazard polygon emerged across active road corridor. NetworkX recalculated safe bypass route (${res.new_distance_km} km) avoiding inundated segments.`);
      await refreshData();
    } catch (err: any) {
      alert("Reroute trigger failed: " + err.message);
    } finally {
      setSimulating(false);
    }
  };

  // Handler: Human-in-the-Loop Officer Approval
  const handleApproveOrder = async (orderId: string) => {
    try {
      await approveOrder(orderId);
      alert(`Order ${orderId} approved by District Relief Officer! Status set to DISPATCHED.`);
      await refreshData();
    } catch (err: any) {
      alert("Approval failed: " + err.message);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Command Center Header Card */}
      <div className={`p-6 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
              </span>
              <h1 className="text-2xl font-black text-white flex items-center gap-2">
                {t.commandCenterTitle}
              </h1>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Autonomous multi-agent logistics orchestrator with dynamic hazard avoidance and human-in-the-loop governance.
            </p>
          </div>

          {/* District View Selector & Refresh */}
          <div className="flex items-center gap-2">
            <select
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-rose-500"
            >
              <option value="darbhanga">Darbhanga Flood Zone (BR)</option>
              <option value="solapur">Solapur Drought Zone (MH)</option>
              <option value="cuddalore">Cuddalore Coastal Zone (TN)</option>
            </select>

            <button
              onClick={refreshData}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl"
              title="Refresh Telemetry"
            >
              <RotateCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Telemetry Stats Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-800">
          <div className="bg-slate-800/50 p-3.5 rounded-xl border border-slate-700/50">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Fleet Units Monitored
            </span>
            <span className="text-2xl font-black text-white">{fleet.length} Units</span>
          </div>
          <div className="bg-slate-800/50 p-3.5 rounded-xl border border-slate-700/50">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Active Dispatches
            </span>
            <span className="text-2xl font-black text-emerald-400">
              {orders.filter((o) => o.status === 'in_transit' || o.status === 'dispatched').length} Active
            </span>
          </div>
          <div className="bg-slate-800/50 p-3.5 rounded-xl border border-slate-700/50">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Held for Officer Approval
            </span>
            <span className="text-2xl font-black text-amber-400">
              {orders.filter((o) => o.requires_approval && !o.is_approved).length} Pending
            </span>
          </div>
          <div className="bg-slate-800/50 p-3.5 rounded-xl border border-slate-700/50">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Dynamic Reroutes
            </span>
            <span className="text-2xl font-black text-blue-400">
              {orders.filter((o) => o.rerouted_count > 0).length} Dynamic
            </span>
          </div>
        </div>
      </div>

      {/* Interactive Simulation Control Bar */}
      <div className="p-4 bg-gradient-to-r from-rose-950/60 via-slate-900 to-amber-950/60 border border-slate-800 rounded-2xl flex flex-wrap items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-white">
            {t.simulatorTitle}:
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={handleTriggerFlood}
            disabled={simulating}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold shadow-md transition-all disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5" />
            <span>{t.simulateFlood}</span>
          </button>

          <button
            onClick={handleTriggerDrought}
            disabled={simulating}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-bold shadow-md transition-all disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5" />
            <span>{t.simulateDrought}</span>
          </button>

          <button
            onClick={handleTriggerReroute}
            disabled={simulating}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-md transition-all disabled:opacity-50"
          >
            <RotateCw className="w-3.5 h-3.5" />
            <span>{t.simulateReroute}</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Command Map + Dispatch Orders Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Command Map Area (2 Cols) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-900 p-2 rounded-2xl border border-slate-800 shadow-2xl relative overflow-hidden">
            <LeafletCommandMap
              district={district}
              fleet={fleet}
              orders={orders}
              activeHazardBbox={activeHazardBbox}
            />

            {/* Map Legend */}
            <div className="absolute top-6 right-6 z-10 bg-slate-950/90 backdrop-blur-md p-3 rounded-xl border border-slate-800 text-[11px] text-slate-300 space-y-1.5 shadow-xl">
              <div className="font-bold text-white text-xs border-b border-slate-800 pb-1">
                Telemetry Legend
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-blue-500 inline-block" />
                <span>Primary Safe Road Route</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-emerald-400 inline-block" />
                <span>Dynamic Rerouted Bypass Path</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-rose-500 inline-block" />
                <span>Inundated Flood Barrier Polygon</span>
              </div>
            </div>
          </div>

          {/* Active Dispatch Orders List */}
          <div className={`p-5 rounded-2xl border ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
            <h3 className="text-base font-bold text-white flex items-center gap-2 mb-4">
              <Truck className="w-5 h-5 text-emerald-400" />
              {t.activeOrders} ({orders.length})
            </h3>
            <div className="space-y-3">
              {orders.map((ord) => {
                const statusColors = {
                  dispatched: 'border-blue-500/40 bg-blue-500/10 text-blue-300',
                  in_transit: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300',
                  pending_approval: 'border-amber-500/40 bg-amber-500/10 text-amber-300',
                  delivered: 'border-slate-500/40 bg-slate-500/10 text-slate-300',
                };
                return (
                  <div
                    key={ord.id}
                    className="p-4 rounded-xl border border-slate-800 bg-slate-850/60 flex flex-col md:flex-row md:items-center justify-between gap-4"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold text-white">{ord.tracking_number}</span>
                        <span
                          className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${
                            statusColors[ord.status as keyof typeof statusColors] || statusColors.in_transit
                          }`}
                        >
                          {ord.status.replace('_', ' ')}
                        </span>
                        {ord.rerouted_count > 0 && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            REROUTED x{ord.rerouted_count}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-300 flex items-center gap-1">
                        <MapPin className="w-3 h-3 text-rose-400" />
                        Destination: <strong>{ord.destination_village}</strong> | Vehicle:{' '}
                        <strong>{ord.vehicle_id || 'Auto-Allocated'}</strong>
                      </p>
                      <div className="text-[11px] text-slate-400">
                        Total Value: <strong>₹{Number(ord.total_value_inr).toLocaleString('en-IN')}</strong> |
                        Items: {ord.items_ordered?.map((it: any) => `${it.qty}x ${it.item}`).join(', ')}
                      </div>
                    </div>

                    {/* Human in the loop action */}
                    {ord.requires_approval && !ord.is_approved && (
                      <button
                        onClick={() => handleApproveOrder(ord.id)}
                        className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold rounded-xl shadow-md transition-all flex items-center gap-1.5 self-start md:self-auto"
                      >
                        <ShieldCheck className="w-4 h-4" />
                        <span>{t.approveBtn}</span>
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Audit Log Drawer (1 Col) */}
        <div className={`p-5 rounded-2xl border flex flex-col h-[780px] ${lowBandwidth ? 'bg-white border-black' : 'bg-slate-900 border-slate-800 shadow-xl'}`}>
          <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-800">
            <Terminal className="w-5 h-5 text-emerald-400" />
            <h3 className="text-base font-bold text-white">{t.auditLogTitle}</h3>
          </div>

          {/* Scrollable Audit Log Entries */}
          <div className="flex-1 overflow-y-auto space-y-3 pr-1">
            {auditLogs.map((log) => {
              const isExpanded = expandedLogId === log.id;
              return (
                <div
                  key={log.id}
                  className="p-3.5 rounded-xl border border-slate-800 bg-slate-950/60 text-xs space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] text-slate-400 flex items-center gap-1">
                      <Clock className="w-3 h-3 text-emerald-400" />
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-slate-800 text-emerald-400 border border-slate-700">
                      {log.trigger_event}
                    </span>
                  </div>

                  <p className="text-slate-200 text-xs leading-normal font-sans">
                    {log.reasoning_text}
                  </p>

                  <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                    <span className="text-[11px] font-semibold text-slate-400">
                      Action: {log.action_taken}
                    </span>
                    {log.tool_calls && log.tool_calls.length > 0 && (
                      <button
                        onClick={() => setExpandedLogId(isExpanded ? null : log.id)}
                        className="text-[10px] font-bold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
                      >
                        <span>{log.tool_calls.length} Tools</span>
                        {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      </button>
                    )}
                  </div>

                  {/* Expanded Tool Call Inspection */}
                  {isExpanded && log.tool_calls && (
                    <div className="mt-2 p-2 bg-slate-900 rounded-lg border border-slate-800 font-mono text-[10px] text-slate-300 space-y-1">
                      <div className="font-bold text-emerald-400 border-b border-slate-800 pb-1">
                        Tool Executions:
                      </div>
                      <pre className="overflow-x-auto whitespace-pre-wrap">
                        {JSON.stringify(log.tool_calls, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

