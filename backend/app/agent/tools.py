from sqlalchemy.orm import Session
from app.incidents.models import Incident
import json
import os

def search_incidents(db: Session, query: str):
    incidents = db.query(Incident).filter(
        Incident.title.ilike(f"%{query}%") | 
        Incident.description.ilike(f"%{query}%") |
        Incident.symptoms.ilike(f"%{query}%")
    ).all()
    return [{"id": i.id, "title": i.title, "symptoms": i.symptoms, "root_cause": i.root_cause, "resolution": i.resolution} for i in incidents]

def get_incident(db: Session, incident_id: int):
    i = db.query(Incident).filter(Incident.id == incident_id).first()
    if not i: return None
    return {"id": i.id, "title": i.title, "symptoms": i.symptoms, "root_cause": i.root_cause, "resolution": i.resolution}

def search_logs(query: str):
    try:
        with open("../data/sample_logs.json", "r") as f:
            logs = json.load(f)
            return [l for l in logs if query.lower() in json.dumps(l).lower()]
    except Exception:
        return []

def get_runbook(service: str):
    try:
        with open("../data/sample_runbooks.json", "r") as f:
            runbooks = json.load(f)
            return runbooks.get(service, "No runbook found")
    except Exception:
        return "No runbook found"
