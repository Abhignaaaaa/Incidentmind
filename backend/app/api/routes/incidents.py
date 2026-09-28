from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.incidents.schemas import IncidentCreate, IncidentResponse
from app.incidents.service import create_incident, get_incidents, get_incident

router = APIRouter()

@router.post("/incidents", response_model=IncidentResponse)
def create_new_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    return create_incident(db=db, incident=incident)

@router.get("/incidents", response_model=List[IncidentResponse])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_incidents(db, skip=skip, limit=limit)

@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = get_incident(db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident
