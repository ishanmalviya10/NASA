# main.py
import io
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = FastAPI(
    title="Air Quality Platform — Mock API + Viz",
    version="1.0",
    description="Mock backend providing forecasts, timeseries, risk, attribution, alerts, and visualization endpoints (PNG + Plotly-like JSON)."
)

# -------------------------
# Pydantic Schemas
# -------------------------
class Station(BaseModel):
    station_id: str
    name: str
    lat: float
    lon: float
    region: str
    tags: List[str]
    sensors: Optional[List[Dict]] = None

class ForecastPoint(BaseModel):
    ts: datetime
    value: float
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    model_version: Optional[str] = None

class ForecastResponse(BaseModel):
    station_id: str
    pollutant: str
    units: str
    horizon: str
    forecasts: List[ForecastPoint]

class TimeSeriesPoint(BaseModel):
    ts: datetime
    value: float
    qa_flag: Optional[str] = "good"

class TimeSeriesResponse(BaseModel):
    station_id: str
    pollutant: str
    units: str
    series: List[TimeSeriesPoint]

class RiskScore(BaseModel):
    pollutant: str
    score_0_100: float
    category: str
    threshold_used: float

class RiskSummaryResponse(BaseModel):
    region: str
    timestamp: datetime
    risk_scores: List[RiskScore]

class AttributionBreakdown(BaseModel):
    source: str
    contribution_percent: float
    value: float

class AttributionResponse(BaseModel):
    pollutant: str
    total: float
    breakdown: List[AttributionBreakdown]

class AlertRecord(BaseModel):
    alert_id: str
    station_id: str
    pollutant: str
    threshold: float
    observed_value: float
    ts: datetime
    status: str

class WebhookSimulateRequest(BaseModel):
    type: str
    payload: Dict

# -------------------------
# Mock data (in-memory)
# -------------------------
_STATIONS = [
    Station(
        station_id="ST-DEL-001",
        name="Delhi - ITO",
        lat=28.6353,
        lon=77.22496,
        region="Delhi NCR",
        tags=["urban"],
        sensors=[{"pollutant":"PM2.5","unit":"ug/m3","sensor_id":"S1"},{"pollutant":"NO2","unit":"ppb","sensor_id":"S2"}]
    ),
    Station(
        station_id="ST-DEL-002",
        name="Gurgaon - Sector 14",
        lat=28.4674,
        lon=77.0266,
        region="Delhi NCR",
        tags=["suburban"],
        sensors=[{"pollutant":"PM2.5","unit":"ug/m3","sensor_id":"S3"}]
    )
]

_ALERTS = [
    AlertRecord(
        alert_id="A-001",
        station_id="ST-DEL-001",
        pollutant="PM2.5",
        threshold=60.0,
        observed_value=82.0,
        ts=datetime.utcnow(),
        status="active"
    )
]

# -------------------------
# Utilities: generators
# -------------------------
def _iso_now_plus(hours: int) -> datetime:
    return datetime.utcnow() + timedelta(hours=hours)

def generate_forecasts(station_id: str, pollutant: str, hours: int = 24) -> List[Dict]:
    out = []
    base = 80 if pollutant.upper().startswith("PM") else 30
    for h in range(hours):
        ts = _iso_now_plus(h)
        noise = (math.sin(h/6.0) + random.random()*0.6) * 10
        val = max(0, round(base + noise, 2))
        out.append({
            "ts": ts,
            "value": val,
            "ci_lower": max(0, round(val - 8.0,2)),
            "ci_upper": round(val + 8.0,2),
            "model_version": "mock-v0.3"
        })
    return out

def generate_timeseries(station_id: str, pollutant: str, hours: int = 48) -> List[Dict]:
    out = []
    for h in range(hours, -1, -1):
        ts = datetime.utcnow() - timedelta(hours=h)
        val = round(40 + random.random()*80, 2)
        out.append({"ts": ts, "value": val, "qa_flag": "good"})
    return out

def generate_risk_scores(region: str) -> List[Dict]:
    scores = []
    for pollutant in ["PM2.5","PM10","NO2","O3"]:
        score = round(random.uniform(10,90),2)
        cat = "Low" if score < 33 else "Moderate" if score < 66 else "High"
        threshold = 50 if pollutant.startswith("PM") else 40
        scores.append({"pollutant": pollutant, "score_0_100": score, "category": cat, "threshold_used": threshold})
    return scores

def generate_attribution(pollutant: str) -> Dict:
    sources = ["Traffic","Industry","Construction","Residential","Natural"]
    vals = [random.uniform(10,40) for _ in sources]
    total = sum(vals)
    breakdown = []
    for s,v in zip(sources, vals):
        p = round((v/total)*100,2)
        breakdown.append({"source": s, "contribution_percent": p, "value": round((v/total)*100,2)})
    return {"pollutant": pollutant, "total": round(total,2), "breakdown": breakdown}

# -------------------------
# API: core endpoints
# -------------------------
@app.get("/api/v1/stations", response_model=List[Station])
def list_stations(region: Optional[str] = Query(None), limit: int = 50, offset: int = 0):
    results = _STATIONS
    if region:
        results = [s for s in results if s.region == region]
    return results[offset: offset + limit]

@app.get("/api/v1/stations/{station_id}", response_model=Station)
def get_station(station_id: str):
    for s in _STATIONS:
        if s.station_id == station_id:
            return s
    raise HTTPException(status_code=404, detail="station not found")

@app.get("/api/v1/forecasts", response_model=ForecastResponse)
def get_forecasts(station_id: Optional[str] = None, pollutant: str = "PM2.5", horizon: str = "24h"):
    st = station_id or _STATIONS[0].station_id
    hours = 168 if horizon == "7d" else 72 if horizon == "72h" else 24
    forecasts = generate_forecasts(st, pollutant, hours)
    return {"station_id": st, "pollutant": pollutant, "units": "ug/m3" if pollutant.startswith("PM") else "ppb", "horizon": horizon, "forecasts": forecasts}

@app.get("/api/v1/timeseries", response_model=TimeSeriesResponse)
def get_timeseries(station_id: Optional[str] = None, pollutant: str = "PM2.5", window: str = "48h"):
    st = station_id or _STATIONS[0].station_id
    hours = int(window.replace("h","")) if "h" in window else 48
    series = generate_timeseries(st, pollutant, hours)
    return {"station_id": st, "pollutant": pollutant, "units": "ug/m3" if pollutant.startswith("PM") else "ppb", "series": series}

@app.get("/api/v1/risk/summary", response_model=RiskSummaryResponse)
def get_risk_summary(region: Optional[str] = None):
    r = region or "Delhi NCR"
    ts = datetime.utcnow()
    risk_scores = generate_risk_scores(r)
    return {"region": r, "timestamp": ts, "risk_scores": risk_scores}

@app.get("/api/v1/attribution", response_model=AttributionResponse)
def get_attribution(station_id: Optional[str] = None, pollutant: str = "PM2.5", window: str = "past_24h"):
    return generate_attribution(pollutant)

@app.get("/api/v1/alerts", response_model=List[AlertRecord])
def list_alerts(region: Optional[str] = None, since: Optional[datetime] = None):
    out = _ALERTS
    if region:
        out = [a for a in out if any(s.region == region and s.station_id == a.station_id for s in _STATIONS)]
    if since:
        out = [a for a in out if a.ts >= since]
    return out

@app.post("/api/v1/webhook/simulate")
def webhook_simulate(payload: WebhookSimulateRequest):
    # Simple echo + event id
    event_id = f"evt-{random.randint(1000,9999)}"
    return {"event_id": event_id, "type": payload.type, "payload": payload.payload, "received_at": datetime.utcnow()}

# -------------------------
# Visualization: PNG endpoints (matplotlib) + Plotly-like JSON
# -------------------------
def _line_plot_png(x, y, title, y_label="value", width=900, height=360):
    plt.figure(figsize=(width/100, height/100))
    plt.plot(x, y, marker="o", linewidth=2)
    plt.title(title)
    plt.xlabel("time")
    plt.ylabel(y_label)
    plt.grid(alpha=0.25)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=100)
    plt.close()
    buf.seek(0)
    return buf

@app.get("/api/v1/viz/timeseries.png")
def viz_timeseries_png(region: str = Query("Delhi NCR"), pollutant: str = Query("PM2.5"), hours: int = Query(24)):
    series = generate_timeseries(station_id=None, pollutant=pollutant, hours=hours)["series"] if False else generate_timeseries(None, pollutant, hours)
    x = [p["ts"] for p in series]
    y = [p["value"] for p in series]
    buf = _line_plot_png(x, y, f"{pollutant} timeseries — {region}", y_label="µg/m³")
    return StreamingResponse(buf, media_type="image/png")

@app.get("/api/v1/viz/timeseries.json")
def viz_timeseries_json(region: str = Query("Delhi NCR"), pollutant: str = Query("PM2.5"), hours: int = Query(24)):
    series = generate_timeseries(None, pollutant, hours)
    x = [p["ts"].isoformat() for p in series]
    y = [p["value"] for p in series]
    fig = {
        "data": [{"x": x, "y": y, "type": "scatter", "mode": "lines+markers", "name": pollutant}],
        "layout": {"title": f"{pollutant} Time Series ({region})", "xaxis": {"title": "Time"}, "yaxis": {"title": "µg/m³"}}
    }
    return JSONResponse(content=fig)

# Risk dial PNG
def _risk_dial_png(value_pct: float, title: str = "Risk Dial") -> io.BytesIO:
    # Draw semicircular gauge from 0..100 with colored zones
    fig, ax = plt.subplots(figsize=(6,3))
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(0, 1.2)
    ax.axis('off')
    # colored arcs
    norm = lambda v: math.radians(180 * (v/100))
    # sectors: green (0-33), yellow(33-66), red(66-100)
    sectors = [(0,33,'#2ca02c'), (33,66,'#ffcc00'), (66,100,'#d62728')]
    for a,b,color in sectors:
        theta1 = math.degrees(math.pi - norm(b))
        theta2 = math.degrees(math.pi - norm(a))
        wedge = matplotlib.patches.Wedge((0,0), 1, theta1, theta2, width=0.35, facecolor=color, alpha=0.9)
        ax.add_patch(wedge)
    # needle
    theta = math.pi - norm(value_pct)
    x = 0.65 * math.cos(theta)
    y = 0.65 * math.sin(theta)
    ax.plot([0, x], [0, y], linewidth=3, color='black')
    # center circle
    ax.add_patch(matplotlib.patches.Circle((0,0), 0.06, color='black'))
    ax.text(0, -0.1, f"{value_pct:.0f}", ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_title(title)
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf

@app.get("/api/v1/viz/risk_dial.png")
def viz_risk_dial_png(region: str = Query("Delhi NCR")):
    scores = generate_risk_scores(region)
    # pick max pollutant score as dial
    max_score = max(s["score_0_100"] for s in scores)
    buf = _risk_dial_png(max_score, title=f"Risk (top) — {region}")
    return StreamingResponse(buf, media_type="image/png")

@app.get("/api/v1/viz/risk_dial.json")
def viz_risk_dial_json(region: str = Query("Delhi NCR")):
    scores = generate_risk_scores(region)
    # structure for frontend dial: value, thresholds
    top = max(scores, key=lambda s: s["score_0_100"])
    cfg = {"value": top["score_0_100"], "label": top["pollutant"], "thresholds": {"low":33,"med":66,"high":100}, "units":"score"}
    return JSONResponse(content=cfg)

# Attribution PNG (stacked horizontal bar)
def _attribution_png(breakdown, title="Attribution"):
    sources = [b["source"] for b in breakdown]
    vals = [b["contribution_percent"] for b in breakdown]
    fig, ax = plt.subplots(figsize=(8,2))
    colors = plt.cm.tab10.colors
    left = 0
    for i,(s,v) in enumerate(zip(sources,vals)):
        ax.barh(0, v, left=left, color=colors[i % len(colors)], label=f"{s} ({v}%)")
        left += v
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.legend(ncol=len(sources), bbox_to_anchor=(0.5, -0.4), loc='upper center')
    ax.set_title(title)
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf

@app.get("/api/v1/viz/attribution.png")
def viz_attribution_png(pollutant: str = Query("PM2.5")):
    attr = generate_attribution(pollutant)
    buf = _attribution_png(attr["breakdown"], title=f"Source Attribution — {pollutant}")
    return StreamingResponse(buf, media_type="image/png")

@app.get("/api/v1/viz/attribution.json")
def viz_attribution_json(pollutant: str = Query("PM2.5")):
    attr = generate_attribution(pollutant)
    # return a simple stacked config
    cfg = {"data": [{"type":"bar","orientation":"h","x":[b["contribution_percent"] for b in attr["breakdown"]],"y":[pollutant],"name":[b["source"] for b in attr["breakdown"]]}], "layout": {"title": f"Attribution — {pollutant}"}}
    return JSONResponse(content=cfg)

# -------------------------
# Docs & component / architecture specs served as endpoints
# -------------------------
_COMPONENTS_MD = """
# Visualization Component Library Spec (summary)

Design tokens:
- Color scale: sequential 6-step (blue -> red) for time series intensity.
- Attribution categorical palette: 6 fixed hex colors mapped to sources.
- Threshold categories: `safe`, `moderate`, `unhealthy`, `very_unhealthy`.

Components:
1. TimeSeriesChart
   - Props: data: [{ts, value, ci_lower?, ci_upper?}], seriesMeta: {pollutant, units, colorKey}, xZoom, yDomain
   - Exports PNG endpoint: /api/v1/viz/timeseries.png
   - Exports Plotly JSON: /api/v1/viz/timeseries.json

2. RiskDial
   - Props: value (0-100), thresholds {low, med, high}, label, onClick
   - Exports PNG endpoint: /api/v1/viz/risk_dial.png
   - Exports JSON: /api/v1/viz/risk_dial.json

3. AttributionBars (stacked)
   - Props: breakdown: [{source, contribution_percent}], showPercent boolean
   - PNG endpoint: /api/v1/viz/attribution.png
   - JSON endpoint: /api/v1/viz/attribution.json

Legend: provide a separate legend component that accepts items: [{key, label, color}].

Accessibility:
- All charts should have aria-label equivalents on the frontend.
- Provide numeric table data endpoints (timeseries) for screen readers.
"""

_ARCHITECTURE_MD = """
# Backend Architecture & Deployment Plan (summary)

Principles:
- Schema-first; raw immutable store; reproducible transforms; versioned model outputs.
- Low-latency serving (API + cache), batch for heavy ETL.

Components:
1. Ingestion:
   - Sources: sensor HTTP/MQTT, model output (S3), 3rd-party feeds.
   - Tools: lightweight collectors -> Kafka / Managed stream.

2. Raw store:
   - S3 (parquet/json) partitioned by date/region.

3. ETL / Stream processing:
   - Spark Structured Streaming / Flink or managed Glue.
   - Tasks: QA, unit conversion, resampling, aggregation, enrichment.

4. Feature/model store:
   - TimescaleDB (Postgres + Timescale) or InfluxDB for timeseries.
   - Model outputs stored in S3 & indexed in DB.

5. Serving:
   - FastAPI (or Go) microservice; caching in Redis; API Gateway (NGINX/ALB).
   - CDN for static assets.

6. Alerts engine:
   - Stream-based window detections or scheduled queries, push to Alert DB & notify via webhooks/Slack/SMS.

Deployment:
- Dev: single node
- Staging: small cluster
- Prod: k8s (EKS/GKE) with autoscaling, ArgoCD for GitOps.

Observability:
- Metrics: Prometheus + Grafana
- Logs: ELK/Opensearch
- Traces: Jaeger
"""

_TEAM_SYNC_MD = """
# Teamwide Sync Agenda (30–45 mins)

1. Recap & Goals (5 min)
2. Confirm pilot region & pollutants (5 min)
3. Member 1: ingestion details & sample payloads (7 min)
4. Member 3: model outputs & uncertainties (7 min)
5. Lock data schemas & API endpoints (5 min)
6. Assign owners & next steps (5-10 min)

Deliverables to lock in Sprint 2:
- Endpoints: /stations, /forecasts, /timeseries, /risk/summary, /attribution, /alerts
- First views: station page (time series + risk dial + attribution)
- Alert logic: threshold + rolling-average
"""

_PROGRESS_REPORT_TEMPLATE = """
Week X — Progress Report
- Done:
  - Implemented mock API endpoints and visualization endpoints (PNG + JSON).
  - Prototype visualization component spec provided.
- In progress:
  - Integrate model outputs (waiting for Member 3).
  - Hook ingestion (waiting for Member 1 sample payloads).
- Blockers:
  - Sample payload mismatch, units & timestamp differences.
- Next week:
  - Provide Postman collection, OpenAPI YAML, and simple React demo to consume JSON endpoints.
- Metrics:
  - Sample stations: {n_stations}
"""

@app.get("/spec/components", response_class=PlainTextResponse)
def spec_components():
    return _COMPONENTS_MD

@app.get("/spec/architecture", response_class=PlainTextResponse)
def spec_architecture():
    return _ARCHITECTURE_MD

@app.get("/spec/team_sync", response_class=PlainTextResponse)
def spec_team_sync():
    return _TEAM_SYNC_MD

@app.get("/spec/progress_report_template", response_class=PlainTextResponse)
def spec_progress_report():
    return _PROGRESS_REPORT_TEMPLATE.format(n_stations=len(_STATIONS))

# -------------------------
# Run note (if executed directly)
# -------------------------
if __name__ == "__main__":
    import uvicorn
    print("Run with: uvicorn main:app --reload --port 8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
