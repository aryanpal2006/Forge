import time
import json
import uuid
from typing import Dict, Any, List, Optional
from backend.app.database import SessionLocal
from backend.app.models.logistics import DispatchOrder, AuditLog, FleetVehicle
from backend.app.risk_engine.risk_service import risk_service
from backend.app.logistics.mock_services import mock_services
from backend.app.logistics.router import road_router

class AutonomousReliefAgent:
    """Autonomous Emergency Response & Logistics Orchestrator with tool-calling and dynamic rerouting."""

    def __init__(self, hitl_threshold_inr: float = 50000.0):
        self.hitl_threshold_inr = hitl_threshold_inr

    # --- Tool 1: get_risk_zones ---
    def get_risk_zones(self, district_id: str) -> List[Dict[str, Any]]:
        grid = risk_service.get_district_risk_grid(district_id)
        # Filter high risk cells (> 0.60)
        high_risk = []
        for feat in grid.get("features", []):
            props = feat.get("properties", {})
            f_score = props.get("flood_risk", 0.0)
            d_score = props.get("drought_risk", 0.0)
            if f_score >= 0.60 or d_score >= 0.70:
                high_risk.append({
                    "cell_code": props.get("cell_code"),
                    "flood_risk": f_score,
                    "drought_risk": d_score,
                    "center_lat": props.get("center_lat"),
                    "center_lon": props.get("center_lon"),
                    "bbox": [props.get("min_lon"), props.get("min_lat"), props.get("max_lon"), props.get("max_lat")]
                })
        return high_risk

    # --- Tool 2: get_fleet_status ---
    def get_fleet_status(self, district_id: str) -> List[Dict[str, Any]]:
        return mock_services.list_fleet(district_id=district_id)

    # --- Tool 3: get_supplier_inventory ---
    def get_supplier_inventory(self, item_keyword: str, district_id: str) -> Optional[Dict[str, Any]]:
        return mock_services.find_supplier_for_item(item_keyword, district_id)

    # --- Tool 4: compute_safe_route ---
    def compute_safe_route(
        self,
        district_id: str,
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        hazard_polygons: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        origin_node = road_router.find_nearest_node(district_id, origin_lat, origin_lon)
        dest_node = road_router.find_nearest_node(district_id, dest_lat, dest_lon)
        return road_router.compute_safe_route(district_id, origin_node, dest_node, hazard_polygons)

    # --- Tool 5: create_dispatch_order ---
    def create_dispatch_order(
        self,
        district_id: str,
        supplier_id: str,
        destination_village: str,
        dest_lat: float,
        dest_lon: float,
        items: List[Dict[str, Any]],
        vehicle_id: str,
        route_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            total_val = sum(it.get("value_inr", 0.0) for it in items)
            req_approval = total_val >= self.hitl_threshold_inr
            is_approved = not req_approval # Auto-approved if under threshold
            
            order_id = f"ORD-{int(time.time()*1000)}-{str(uuid.uuid4())[:4].upper()}"
            tracking_num = f"KS-{district_id[:3].upper()}-{int(time.time() * 1000) % 1000000}-{str(uuid.uuid4())[:3].upper()}"

            order = DispatchOrder(
                id=order_id,
                tracking_number=tracking_num,
                district_id=district_id,
                supplier_id=supplier_id,
                vehicle_id=vehicle_id,
                destination_village=destination_village,
                destination_lat=dest_lat,
                destination_lon=dest_lon,
                items_ordered=items,
                total_value_inr=total_val,
                status="dispatched" if is_approved else "pending_approval",
                requires_approval=req_approval,
                is_approved=is_approved,
                route_geojson=route_info.get("route_geojson"),
                rerouted_count=1 if route_info.get("is_rerouted") else 0
            )
            db.add(order)
            
            # Update vehicle status if auto-dispatched
            if is_approved:
                v = db.query(FleetVehicle).filter(FleetVehicle.id == vehicle_id).first()
                if v:
                    v.status = "in_transit"
                    v.active_order_id = order_id
                mock_services.update_vehicle_status(vehicle_id, "in_transit", order_id=order_id)
                
            db.commit()
            return {
                "order_id": order_id,
                "tracking_number": tracking_num,
                "status": order.status,
                "total_value_inr": total_val,
                "requires_approval": req_approval,
                "vehicle_id": vehicle_id,
                "route_info": route_info
            }
        finally:
            db.close()

    # --- Tool 6: notify ---
    def notify(self, target: str, message: str, language: str = "en") -> Dict[str, Any]:
        return {
            "target": target,
            "message": message,
            "language": language,
            "channel": "SMS_AND_DASHBOARD",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    # --- Core Autonomous Planning Loop ---
    def orchestrate_emergency_response(
        self,
        district_id: str,
        event_trigger: str = "SCHEDULED_MONITOR",
        injected_severity: float = 0.85
    ) -> Dict[str, Any]:
        """Tool-calling orchestration loop responding to emergency risk triggers."""
        db = SessionLocal()
        tool_audit_trail = []
        
        try:
            # Step 1: Tool call -> get_risk_zones
            risk_zones = self.get_risk_zones(district_id)
            tool_audit_trail.append({
                "tool": "get_risk_zones",
                "inputs": {"district_id": district_id},
                "output_count": len(risk_zones),
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Determine needed item
            if district_id == "darbhanga":
                needed_item = "equipment"
                dest_village = "Kalyanpur Floodplain"
                dest_lat, dest_lon = 26.2200, 85.9400
                items_payload = [
                    {"item": "Diesel De-Watering Pump (10 HP)", "qty": 2, "value_inr": 30000.0},
                    {"item": "Reinforced Water Discharge Hose (200m)", "qty": 4, "value_inr": 12000.0},
                    {"item": "Submergence-Tolerant Swarna Sub-1 Seed Bags", "qty": 10, "value_inr": 18000.0}
                ]
            elif district_id == "solapur":
                needed_item = "water"
                dest_village = "Mohol Gram Panchayat"
                dest_lat, dest_lon = 17.8100, 75.6500
                items_payload = [
                    {"item": "Emergency Potable Water Tanker (12,000L)", "qty": 1, "value_inr": 28000.0},
                    {"item": "Dry Cattle Fodder Silage Bundles", "qty": 100, "value_inr": 25000.0}
                ]
            else:
                needed_item = "equipment"
                dest_village = "Chidambaram Coastal Ward"
                dest_lat, dest_lon = 11.3900, 79.6900
                items_payload = [
                    {"item": "Emergency Green Shade Nets (100m)", "qty": 5, "value_inr": 16000.0},
                    {"item": "Saline-Tolerant Paddy Seed (TRY-1)", "qty": 15, "value_inr": 22500.0}
                ]

            # Step 2: Tool call -> get_supplier_inventory
            supplier = self.get_supplier_inventory(needed_item, district_id)
            tool_audit_trail.append({
                "tool": "get_supplier_inventory",
                "inputs": {"item_keyword": needed_item, "district_id": district_id},
                "matched_supplier": supplier["name"] if supplier else None,
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Step 3: Tool call -> get_fleet_status
            fleet = self.get_fleet_status(district_id)
            idle_vehicles = [v for v in fleet if v.get("status") in ["idle", "available"]]
            assigned_vehicle = idle_vehicles[0] if idle_vehicles else (fleet[0] if fleet else None)
            
            tool_audit_trail.append({
                "tool": "get_fleet_status",
                "inputs": {"district_id": district_id},
                "assigned_vehicle": assigned_vehicle["vehicle_code"] if assigned_vehicle else "NONE",
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Step 4: Tool call -> compute_safe_route with active hazard polygons
            supp_lat = supplier.get("latitude", 26.15) if supplier else 26.15
            supp_lon = supplier.get("longitude", 85.89) if supplier else 85.89
            
            route_res = self.compute_safe_route(
                district_id=district_id,
                origin_lat=supp_lat,
                origin_lon=supp_lon,
                dest_lat=dest_lat,
                dest_lon=dest_lon,
                hazard_polygons=risk_zones
            )
            
            tool_audit_trail.append({
                "tool": "compute_safe_route",
                "inputs": {"origin": (supp_lat, supp_lon), "destination": (dest_lat, dest_lon)},
                "distance_km": route_res.get("distance_km"),
                "is_rerouted": route_res.get("is_rerouted"),
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Step 5: Tool call -> create_dispatch_order
            order_res = self.create_dispatch_order(
                district_id=district_id,
                supplier_id=supplier["id"] if supplier else "SUPP-01",
                destination_village=dest_village,
                dest_lat=dest_lat,
                dest_lon=dest_lon,
                items=items_payload,
                vehicle_id=assigned_vehicle["id"] if assigned_vehicle else "VEH-01",
                route_info=route_res
            )
            
            tool_audit_trail.append({
                "tool": "create_dispatch_order",
                "order_id": order_res["order_id"],
                "total_value_inr": order_res["total_value_inr"],
                "requires_approval": order_res["requires_approval"],
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Step 6: Tool call -> notify
            notify_res = self.notify(
                target="District Collectorate & Gram Panchayat",
                message=f"KisanShield Emergency Dispatch {order_res['tracking_number']}: Assigned {assigned_vehicle['vehicle_code']} to {dest_village}.",
                language="hi" if district_id == "darbhanga" else ("mr" if district_id == "solapur" else "ta")
            )
            tool_audit_trail.append({
                "tool": "notify",
                "inputs": {"target": notify_res["target"], "lang": notify_res["language"]},
                "status": "SENT",
                "timestamp": time.strftime("%H:%M:%S")
            })

            # Step 7: Persist Audit Log
            reasoning = (
                f"Emergency trigger {event_trigger} activated for {district_id.capitalize()} with severity {injected_severity:.2f}. "
                f"Identified {len(risk_zones)} vulnerable risk cells. Selected supplier '{supplier['name'] if supplier else 'Hub'}' "
                f"and assigned vehicle '{assigned_vehicle['vehicle_code'] if assigned_vehicle else 'Unit'}'. "
                f"Safe route computed over {route_res['distance_km']} km (Rerouted around hazard: {route_res['is_rerouted']}). "
                f"Order total value ₹{order_res['total_value_inr']:,} ({'Held for HITL Officer Approval' if order_res['requires_approval'] else 'Auto-executed'})."
            )

            audit = AuditLog(
                trigger_event=event_trigger,
                district_id=district_id,
                reasoning_text=reasoning,
                tool_calls=tool_audit_trail,
                action_taken=f"Created relief dispatch order {order_res['tracking_number']}",
                status="COMPLETED"
            )
            db.add(audit)
            db.commit()

            return {
                "status": "SUCCESS",
                "trigger": event_trigger,
                "district": district_id,
                "dispatch_order": order_res,
                "audit_summary": reasoning,
                "tool_calls": tool_audit_trail
            }
        finally:
            db.close()

    # --- Dynamic Mid-Transit Rerouting ---
    def trigger_mid_transit_rerouting(self, order_id: str, new_hazard_bbox: List[float]) -> Dict[str, Any]:
        """Demonstrates autonomous mid-transit dynamic rerouting when a new hazard emerges along active route."""
        db = SessionLocal()
        try:
            order = db.query(DispatchOrder).filter(DispatchOrder.id == order_id).first()
            if not order:
                # Fallback to most recent order
                order = db.query(DispatchOrder).order_by(DispatchOrder.created_at.desc()).first()
            if not order:
                return {"status": "ERROR", "message": "No active dispatch orders to reroute."}

            supplier = mock_services.get_supplier(order.supplier_id)
            supp_lat = supplier.get("latitude", 26.15) if supplier else 26.15
            supp_lon = supplier.get("longitude", 85.89) if supplier else 85.89

            # Re-compute route avoiding the new hazard polygon
            new_hazard_polygon = [{"bbox": new_hazard_bbox, "severity": 0.95}]
            new_route_res = self.compute_safe_route(
                district_id=order.district_id,
                origin_lat=supp_lat,
                origin_lon=supp_lon,
                dest_lat=order.destination_lat,
                dest_lon=order.destination_lon,
                hazard_polygons=new_hazard_polygon
            )

            order.route_geojson = new_route_res.get("route_geojson")
            order.rerouted_count += 1
            order.status = "in_transit"
            db.commit()

            # Record in Audit Log
            audit = AuditLog(
                trigger_event="MID_TRANSIT_HAZARD_EMERGENCE",
                district_id=order.district_id,
                reasoning_text=(
                    f"New flash-flood breach detected along active transit corridor for {order.tracking_number}. "
                    f"NetworkX recalculated safe bypass route ({new_route_res['distance_km']} km) avoiding inundated road segments."
                ),
                tool_calls=[{
                    "tool": "compute_safe_route_dynamic_reroute",
                    "new_hazard_bbox": new_hazard_bbox,
                    "rerouted_path": new_route_res.get("path_nodes"),
                    "avoided_segments": new_route_res.get("blocked_segments")
                }],
                action_taken=f"Dynamically rerouted dispatch {order.tracking_number} around flood barrier.",
                status="REROUTED"
            )
            db.add(audit)
            db.commit()

            return {
                "status": "REROUTED",
                "order_id": order.id,
                "tracking_number": order.tracking_number,
                "rerouted_count": order.rerouted_count,
                "new_distance_km": new_route_res.get("distance_km"),
                "new_route_geojson": order.route_geojson
            }
        finally:
            db.close()

relief_agent = AutonomousReliefAgent()
