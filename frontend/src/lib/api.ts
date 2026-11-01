const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchAdvisory(params: {
  district: string;
  crop_type: string;
  village?: string;
  language?: string;
  soil_type?: string;
  irrigation_type?: string;
  query_text?: string;
}) {
  const res = await fetch(`${API_BASE}/advisory/advise`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error("Failed to generate advisory");
  return res.json();
}

export async function fetchRiskGrid(district: string, crop: string = "soybean") {
  const res = await fetch(`${API_BASE}/risk/grid?district=${encodeURIComponent(district)}&crop=${encodeURIComponent(crop)}`);
  if (!res.ok) throw new Error("Failed to load risk grid");
  return res.json();
}

export async function fetchRiskSummary(district: string) {
  const res = await fetch(`${API_BASE}/risk/summary?district=${encodeURIComponent(district)}`);
  if (!res.ok) throw new Error("Failed to load risk summary");
  return res.json();
}

export async function fetchMitigationPlan(district: string, crop: string = "soybean") {
  const res = await fetch(`${API_BASE}/risk/mitigation?district=${encodeURIComponent(district)}&crop=${encodeURIComponent(crop)}`);
  if (!res.ok) throw new Error("Failed to load mitigation plan");
  return res.json();
}

export async function fetchSuppliers(district?: string) {
  const url = district ? `${API_BASE}/logistics/suppliers?district=${district}` : `${API_BASE}/logistics/suppliers`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch suppliers");
  return res.json();
}

export async function fetchFleet() {
  const res = await fetch(`${API_BASE}/logistics/fleet`);
  if (!res.ok) throw new Error("Failed to fetch fleet");
  return res.json();
}

export async function fetchOrders(district?: string) {
  const url = district ? `${API_BASE}/logistics/orders?district=${district}` : `${API_BASE}/logistics/orders`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch orders");
  return res.json();
}

export async function simulateEmergency(district_id: string, event_type: string, severity: number = 0.85) {
  const res = await fetch(`${API_BASE}/logistics/simulate-event`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ district_id, event_type, severity }),
  });
  if (!res.ok) throw new Error("Simulation trigger failed");
  return res.json();
}

export async function triggerReroute(order_id?: string, district: string = "darbhanga") {
  const url = order_id
    ? `${API_BASE}/logistics/reroute?order_id=${encodeURIComponent(order_id)}&district=${district}`
    : `${API_BASE}/logistics/reroute?district=${district}`;
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) throw new Error("Reroute trigger failed");
  return res.json();
}

export async function approveOrder(order_id: string) {
  const res = await fetch(`${API_BASE}/logistics/orders/${encodeURIComponent(order_id)}/approve`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Order approval failed");
  return res.json();
}

export async function fetchAuditLogs(district?: string) {
  const url = district ? `${API_BASE}/logistics/audit?district=${district}` : `${API_BASE}/logistics/audit`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch audit logs");
  return res.json();
}

