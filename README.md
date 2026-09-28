# Incidentmind - Phase 1

Incidentmind is an AI incident response foundation that learns from previous incidents using Hindsight memory.

## Architecture
- React Frontend (Vite)
- FastAPI Backend
- PostgreSQL Database
- Hindsight Memory Integration

## Setup
1. Copy `.env.example` to `.env`
2. Run `docker-compose up --build`
3. Access UI at http://localhost:5173 and API at http://localhost:8001

## Running Demo
`python scripts/memory_demo.py`

## Running Tests
`pytest backend/tests`
