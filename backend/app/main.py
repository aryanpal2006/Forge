from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.seed import seed_database
from backend.app.api.advisory_routes import router as advisory_router
from backend.app.api.risk_routes import router as risk_router
from backend.app.api.logistics_routes import router as logistics_router
from backend.app.api.mock_routes import router as mock_router
from backend.app.logistics.scheduler import logistics_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed baseline data
    Base.metadata.create_all(bind=engine)
    seed_database()
    logistics_scheduler.start()
    yield
    # Shutdown
    logistics_scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Climate-Resilient Agri Advisory + Autonomous Relief Engine (India Focus)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(advisory_router, prefix=settings.API_V1_STR)
app.include_router(risk_router, prefix=settings.API_V1_STR)
app.include_router(logistics_router, prefix=settings.API_V1_STR)
app.include_router(mock_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "database": "sqlite_connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

