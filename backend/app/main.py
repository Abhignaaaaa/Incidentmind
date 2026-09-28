from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, incidents, agent
from app.database.connection import engine, Base
from app.logging import logger

app = FastAPI(title="Incidentmind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(health.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")
app.include_router(agent.router, prefix="/api")

@app.on_event("startup")
async def startup():
    logger.info("Starting up Incidentmind backend")
