# Hindsight Integration

We use Hindsight for storing past incident resolutions and recalling them. The integration connects to the official Hindsight Cloud API.

- **Base URL**: `https://api.hindsight.vectorize.io`
- **Authentication**: `Authorization: Bearer <HINDSIGHT_API_KEY>`
- **Retain**: `POST /v1/default/banks/{bank_id}/memories`
- **Recall**: `POST /v1/default/banks/{bank_id}/memories/recall`

### Required Environment Variables
- `HINDSIGHT_URL`
- `HINDSIGHT_API_KEY`
- `HINDSIGHT_BANK_ID`

### Fallback Behavior
- **Configured**: If an API key is provided, the backend attempts to call the real Hindsight API.
- **Failures**: If the real API request fails, it logs the error clearly and falls back to the local in-memory array.
- **Unconfigured**: If no API key is provided (e.g. local development), it immediately uses the in-memory fallback.
