import time
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.logistics.agent import relief_agent
from backend.app.database import SessionLocal
from backend.app.models.logistics import DispatchOrder, FleetVehicle

class LogisticsScheduler:
    """Continuous monitor scheduler and event simulator manager."""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def start(self):
        if not self.is_running:
            # Check risk triggers every 15 minutes in background
            self.scheduler.add_job(
                func=self._monitor_check,
                trigger="interval",
                minutes=15,
                id="continuous_risk_monitor",
                replace_existing=True
            )
            self.scheduler.start()
            self.is_running = True
            print("Logistics Continuous Monitor Scheduler started.")

    def shutdown(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False

    def _monitor_check(self):
        print(f"[{time.strftime('%H:%M:%S')}] Executing scheduled multi-district climate risk scan...")
        # Inspect demo districts
        for dist in ["solapur", "darbhanga", "cuddalore"]:
            try:
                relief_agent.orchestrate_emergency_response(district_id=dist, event_trigger="SCHEDULED_MONITOR")
            except Exception as e:
                print(f"Scheduled scan error for {dist}: {e}")

    def simulate_emergency_event(self, district_id: str, event_type: str, severity: float = 0.85) -> Dict[str, Any]:
        """Manual event simulator trigger (e.g. 'Trigger flash flood in Darbhanga')."""
        return relief_agent.orchestrate_emergency_response(
            district_id=district_id,
            event_trigger=f"SIMULATED_{event_type.upper()}",
            injected_severity=severity
        )

    def approve_order(self, order_id: str) -> Dict[str, Any]:
        """Human-in-the-Loop approval for high-value dispatch order."""
        db = SessionLocal()
        try:
            order = db.query(DispatchOrder).filter(DispatchOrder.id == order_id).first()
            if not order:
                return {"status": "ERROR", "message": "Order not found"}
            
            order.is_approved = True
            order.status = "dispatched"
            
            # Update vehicle status
            if order.vehicle_id:
                veh = db.query(FleetVehicle).filter(FleetVehicle.id == order.vehicle_id).first()
                if veh:
                    veh.status = "in_transit"
                    veh.active_order_id = order.id
                    
            db.commit()
            return {
                "status": "APPROVED",
                "order_id": order.id,
                "tracking_number": order.tracking_number,
                "order_status": order.status
            }
        finally:
            db.close()

logistics_scheduler = LogisticsScheduler()

