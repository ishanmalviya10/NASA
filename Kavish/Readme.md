# Air Quality Platform — Mock API + Viz (FastAPI)

## Quickstart (local)
1. Create virtualenv and install:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2. Run dev server:
uvicorn main:app --reload --port 8000


3. API docs:
- OpenAPI / Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

4. Useful endpoints:
- Stations: `GET /api/v1/stations`
- Forecasts: `GET /api/v1/forecasts?pollutant=PM2.5&horizon=24h`
- Timeseries: `GET /api/v1/timeseries?pollutant=PM2.5&window=48h`
- Risk summary: `GET /api/v1/risk/summary`
- Attribution: `GET /api/v1/attribution?pollutant=PM2.5`
- Alerts: `GET /api/v1/alerts`
- Viz (PNG): `GET /api/v1/viz/timeseries.png?region=Delhi%20NCR&pollutant=PM2.5&hours=24`
- Viz (JSON config): `GET /api/v1/viz/timeseries.json?region=Delhi%20NCR&pollutant=PM2.5&hours=24`
- Component spec: `GET /spec/components`
- Architecture doc: `GET /spec/architecture`

