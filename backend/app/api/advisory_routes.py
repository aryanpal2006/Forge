from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.farmer import FarmerProfile
from backend.app.schemas.farmer import FarmerProfileCreate, FarmerProfileOut
from backend.app.schemas.advisory import AdvisoryRequest, AdvisoryResponse
from backend.app.advisory.advisory_service import advisory_service

router = APIRouter(prefix="/advisory", tags=["Advisory"])

@router.post("/onboard", response_model=FarmerProfileOut)
def onboard_farmer(profile: FarmerProfileCreate, db: Session = Depends(get_db)):
    db_profile = FarmerProfile(
        name=profile.name,
        phone=profile.phone,
        language=profile.language,
        district=profile.district,
        village=profile.village,
        latitude=profile.latitude,
        longitude=profile.longitude,
        crop_type=profile.crop_type,
        land_size_acres=profile.land_size_acres,
        soil_type=profile.soil_type,
        irrigation_type=profile.irrigation_type
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.post("/advise", response_model=AdvisoryResponse)
def get_farmer_advisory(req: AdvisoryRequest, db: Session = Depends(get_db)):
    # If farmer_id is provided, pull saved profile
    if req.farmer_id:
        p = db.query(FarmerProfile).filter(FarmerProfile.id == req.farmer_id).first()
        if p:
            req.district = p.district
            req.village = p.village
            req.crop_type = p.crop_type
            req.language = p.language
            req.soil_type = p.soil_type
            req.irrigation_type = p.irrigation_type

    res = advisory_service.generate_advisory(
        district=req.district,
        crop=req.crop_type,
        village=req.village or "Central Village",
        language=req.language or "en",
        soil_type=req.soil_type or "Black",
        irrigation_type=req.irrigation_type or "Rainfed",
        query_text=req.query_text or ""
    )
    return res

