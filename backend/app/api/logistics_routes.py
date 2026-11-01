from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from backend.app.database import get_db
from backend.app.models.logistics import Supplier, FleetVehicle, DispatchOrder, AuditLog
from backend.app.schemas.logistics import SimulateEventRequest
from backend.app.logistics.scheduler import logistics_scheduler
from backend.app.logistics.agent import relief_agent
from backend.app.logistics.mock_services import mock_services

router = APIRouter(prefix="/logistics", tags=["Autonomous Logistics"])

@router.get("/suppliers")
def get_suppliers(
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Supplier)
    if district:
        query = query.filter(Supplier.district_id == district.lower())
    if category:
        query = query.filter(Supplier.category == category.lower())
    suppliers = query.all()
    return suppliers

@router.get("/fleet")
def get_fleet(
    district: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(FleetVehicle)
    if district:
        query = query.filter(FleetVehicle.id.like(f"%{district[:2].upper()}%"))
    vehicles = query.all()
    return vehicles

@router.get("/orders")
def get_orders(
    district: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(DispatchOrder).order_by(DispatchOrder.created_at.desc())
    if district:
        query = query.filter(DispatchOrder.district_id == district.lower())
    if status:
        query = query.filter(DispatchOrder.status == status.lower())
    return query.limit(20).all()

@router.post("/simulate-event")
def simulate_event(req: SimulateEventRequest):
    """Triggers an emergency response simulation e.g., 'Trigger flash flood in Darbhanga'."""
    result = logistics_scheduler.simulate_emergency_event(
        district_id=req.district_id,
        event_type=req.event_type,
        severity=req.severity
    )
    return result

@router.post("/reroute")
def trigger_dynamic_reroute(
    order_id: Optional[str] = Query(None),
    district: str = Query("darbhanga")
):
    """Simulates mid-transit hazard emergence and computes dynamic bypass route."""
    # Define an active hazard polygon covering a road segment
    new_hazard_bbox = [85.90, 26.13, 85.93, 26.16] # Inundated corridor
    res = relief_agent.trigger_mid_transit_rerouting(order_id or "", new_hazard_bbox)
    return res

@router.post("/orders/{order_id}/approve")
def approve_dispatch_order(order_id: str):
    """Human-in-the-Loop officer approval gate for held orders."""
    res = logistics_scheduler.approve_order(order_id)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail="Order not found")
    return res

@router.get("/audit")
def get_audit_trail(
    district: Optional[str] = Query(None),
    limit: int = Query(25),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog).order_by(AuditLog.timestamp.desc())
    if district:
        query = query.filter(AuditLog.district_id == district.lower())
    return query.limit(limit).all()

