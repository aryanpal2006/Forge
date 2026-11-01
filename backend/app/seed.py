import json
from pathlib import Path
from backend.app.database import engine, SessionLocal, Base
from backend.app.models.risk import District, RiskGridCell
from backend.app.models.logistics import Supplier, FleetVehicle, DispatchOrder, AuditLog
from backend.app.models.farmer import FarmerProfile
from backend.app.config import settings

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(District).count() > 0:
            print("Database already seeded with districts.")
            return

        # 1. Seed Districts
        districts_file = settings.SEED_DATA_DIR / "districts.json"
        if districts_file.exists():
            with open(districts_file, "r", encoding="utf-8") as f:
                d_list = json.load(f)
                for d in d_list:
                    dist = District(
                        id=d["id"],
                        name=d["name"],
                        state=d["state"],
                        center_lat=d["center_lat"],
                        center_lon=d["center_lon"],
                        agro_zone=d["agro_zone"],
                        primary_hazard=d["primary_hazard"],
                        description=d.get("description", "")
                    )
                    db.add(dist)
            db.commit()
            print("Seeded districts successfully.")

        # 2. Seed Suppliers
        supp_file = settings.SEED_DATA_DIR / "suppliers.json"
        if supp_file.exists():
            with open(supp_file, "r", encoding="utf-8") as f:
                s_list = json.load(f)
                for s in s_list:
                    supp = Supplier(
                        id=s["id"],
                        name=s["name"],
                        district_id=s["district_id"],
                        category=s["category"],
                        latitude=s["latitude"],
                        longitude=s["longitude"],
                        contact_phone=s.get("contact_phone"),
                        inventory_data=s["inventory_data"],
                        is_active=s.get("is_active", True)
                    )
                    db.add(supp)
            db.commit()
            print("Seeded 10 suppliers successfully.")

        # 3. Seed Fleet Vehicles
        fleet_file = settings.SEED_DATA_DIR / "fleet.json"
        if fleet_file.exists():
            with open(fleet_file, "r", encoding="utf-8") as f:
                v_list = json.load(f)
                for v in v_list:
                    veh = FleetVehicle(
                        id=v["id"],
                        vehicle_code=v["vehicle_code"],
                        vehicle_type=v["vehicle_type"],
                        capacity_kg=v["capacity_kg"],
                        fuel_level_pct=v.get("fuel_level_pct", 100.0),
                        current_lat=v["current_lat"],
                        current_lon=v["current_lon"],
                        status=v.get("status", "idle")
                    )
                    db.add(veh)
            db.commit()
            print("Seeded 8 fleet vehicles successfully.")

        # 4. Seed Demo Farmer Profile
        sample_farmer = FarmerProfile(
            name="Ramesh Patil",
            phone="+91 98220 54321",
            language="mr",
            district="Solapur",
            village="Mohol",
            latitude=17.7000,
            longitude=75.8000,
            crop_type="soybean",
            land_size_acres=3.5,
            soil_type="Black",
            irrigation_type="Rainfed"
        )
        db.add(sample_farmer)
        db.commit()
        print("Seeded demo farmer profile.")

        # 5. Initial Audit Log
        init_audit = AuditLog(
            trigger_event="SYSTEM_BOOTSTRAP",
            district_id="solapur",
            reasoning_text="KisanShield Core Data Engine initialized with 3 districts, 10 suppliers, and 8 fleet vehicles.",
            action_taken="System initialization and baseline risk calibration.",
            status="INITIALIZED"
        )
        db.add(init_audit)
        db.commit()
        print("Database bootstrap complete.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

