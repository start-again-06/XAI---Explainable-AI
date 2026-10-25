# XAI-IDS Implementation Plan

## Project: Real-Time Explainable AI Intrusion Detection System
**Version:** 1.0  
**Date:** January 29, 2026  
**Plan Type:** Phased Implementation Roadmap

---

## 📋 Overview

This plan breaks down the XAI-IDS project into **sequential, actionable phases** with clear dependencies, deliverables, and verification criteria. Designed for a **college MVP demonstration** running on a single Windows 11 machine with WSL2.

**Total Estimated Time:** 4-6 weeks (80-120 hours)  
**Team Size:** 1-2 developers (student project)  
**Complexity:** Intermediate to Advanced

---

## 🎯 Project Goals

1. **Demonstrate "Glass Box" AI** - Show interpretable threat detection with rule-based explanations and AI chat
2. **Functional 3-Page UI** - Live dashboard → Incident details → AI chat
3. **Real Telemetry** - Use actual Zeek/Suricata sensors, not simulated data
4. **Educational Tool** - Beginner-friendly explanations for junior analysts
5. **Working Demo** - Complete attack scenario (DDoS) in <15 seconds

---

## 📅 Phase Structure

```
Phase 0: Environment Setup (3-5 days)
   ↓
Phase 1: Sensor Infrastructure (5-7 days)
   ↓
Phase 2: Data Pipeline (4-6 days)
   ↓
Phase 3: Rule-Based Detection Engine (3-4 days)
   ↓
Phase 4: Backend API Services (7-10 days)
   ↓
Phase 5: Frontend UI (7-10 days)
   ↓
Phase 6: Integration & Testing (5-7 days)
   ↓
Phase 7: Demo Preparation (3-5 days)

Note: Total timeline reduced from 8-9 weeks to 5-6 weeks by using rule-based 
detection instead of ML training (saves 5-7 days + eliminates model accuracy risks)
```

---

## 🔧 PHASE 0: Environment Setup

**Goal:** Establish development environment and install all prerequisite tools

**Duration:** 3-5 days  
**Dependencies:** None  
**Risk:** Medium (WSL2 networking can be tricky)

### Tasks

#### Task 0.1: Windows Host Setup
**Deliverable:** Python, PostgreSQL, Redis/Memurai installed and verified

**Steps:**
1. Install Windows 11 Pro/Home (already completed)
2. Install Python 3.11
   ```powershell
   winget install Python.Python.3.11
   python --version  # Verify 3.11.x
   ```
3. Install PostgreSQL 15
   ```powershell
   winget install PostgreSQL.PostgreSQL
   # Test: psql --version
   ```
4. Install Memurai (Redis-compatible)
   - Download from memurai.com
   - Install MSI
   - Start service: `Start-Service Memurai`
   - Test: `redis-cli ping` → expect "PONG"
5. Install Node.js 18 LTS (for frontend)
   ```powershell
   winget install OpenJS.NodeJS.LTS
   node --version  # Verify v18.x
   ```

**Verification:**
```powershell
python --version  # 3.11.x
psql --version    # 15.x
redis-cli ping    # PONG
node --version    # 18.x
```

---

#### Task 0.2: WSL2 Ubuntu Setup
**Deliverable:** WSL2 Ubuntu 22.04 with network access

**Steps:**
1. Enable WSL2 (Admin PowerShell)
   ```powershell
   wsl --install -d Ubuntu-22.04
   wsl --set-default-version 2
   ```
2. Reboot if prompted
3. Launch Ubuntu, create user/password
4. Update packages
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
5. Test network connectivity
   ```bash
   ping -c 3 google.com
   curl ifconfig.me  # Get public IP
   ```
6. Enable systemd (for services)
   ```bash
   echo -e "[boot]\nsystemd=true" | sudo tee -a /etc/wsl.conf
   ```
7. Restart WSL: `wsl --shutdown` then relaunch

**Verification:**
```bash
lsb_release -a  # Ubuntu 22.04 LTS
systemctl --version  # systemd present
```

---

#### Task 0.3: Project Structure Creation
**Deliverable:** Git repository with proper folder structure

**Steps:**
1. Create project directory on Windows
   ```powershell
   cd F:\program-ppt
   ```
2. Initialize Git repo
   ```powershell
   git init
   echo ".venv/" > .gitignore
   echo "__pycache__/" >> .gitignore
   echo "*.pyc" >> .gitignore
   ```
3. Create folder structure
   ```
   backend/
   ├── main.py
   ├── config.py
   ├── requirements.txt
   ├── models/
   ├── routes/
   ├── services/
   ├── database/
   ├── websocket/
   └── utils/
   
   frontend/
   ├── public/
   ├── src/
   │   ├── components/
   │   ├── pages/
   │   ├── services/
   │   └── App.jsx
   └── package.json
   
   sensors/
   ├── zeek/
   ├── suricata/
   └── vector/
   
   data/
   ├── models/
   ├── logs/
   └── geoip/
   
   docs/
   ```

4. Create virtual environment
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

**Verification:**
```powershell
Get-ChildItem -Directory  # Verify all folders exist
python -c "import sys; print(sys.prefix)"  # Verify venv active
```

---

#### Task 0.4: Python Dependencies
**Deliverable:** requirements.txt with all backend packages installed

**Steps:**
1. Create `backend/requirements.txt`:
   ```
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   sqlalchemy==2.0.25
   psycopg2-binary==2.9.9
   redis==5.0.1
   python-socketio==5.11.0
   # ML packages removed - using rule-based detection instead
   # xgboost==2.0.3  # Not needed - using heuristic detection
   # shap==0.44.0    # Not needed - threshold-based explanations
   # scikit-learn==1.4.0  # Not needed for rule-based approach
   pandas==2.2.0
   numpy==1.26.3
   pydantic==2.5.3
   python-dotenv==1.0.0
   httpx==0.26.0
   maxminddb==2.5.1
   ```

2. Install packages
   ```powershell
   pip install -r backend/requirements.txt
   ```

3. Verify imports
   ```python
   python -c "import fastapi, sqlalchemy, redis; print('Success')"
   ```

**Verification:**
```powershell
pip list | Select-String "fastapi|sqlalchemy|redis"
```

---

#### Task 0.5: Database Initialization
**Deliverable:** PostgreSQL database with schema created

**Steps:**
1. Create database
   ```powershell
   psql -U postgres -c "CREATE DATABASE xai_ids;"
   ```

2. Create `backend/database/schema.sql`:
   ```sql
   -- (Use schema from Backend Specification document)
   CREATE TABLE incidents (...);
   CREATE TABLE alerts (...);
   CREATE TABLE endpoint_context (...);
   CREATE TABLE analyst_notes (...);
   CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
   -- etc.
   ```

3. Apply schema
   ```powershell
   psql -U postgres -d xai_ids -f backend/database/schema.sql
   ```

4. Verify tables
   ```powershell
   psql -U postgres -d xai_ids -c "\dt"
   ```

**Verification:**
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';
-- Expect: incidents, alerts, endpoint_context, analyst_notes
```

---

**Phase 0 Success Criteria:**
- [ ] Python 3.11 installed on Windows
- [ ] PostgreSQL 15 installed and database created
- [ ] Memurai running and accessible
- [ ] WSL2 Ubuntu 22.04 operational
- [ ] Project folder structure exists
- [ ] Virtual environment created
- [ ] All Python dependencies installed
- [ ] Database schema applied
- [ ] Git repository initialized

---

## 🌐 PHASE 1: Sensor Infrastructure

**Goal:** Install and configure Zeek, Suricata, Wazuh for real-time detection

**Duration:** 5-7 days  
**Dependencies:** Phase 0 complete  
**Risk:** High (sensor tuning is complex)

### Tasks

#### Task 1.1: Zeek Installation (WSL2)
**Deliverable:** Zeek running and generating conn.log files

**Steps:**
1. Install Zeek in WSL2
   ```bash
   sudo apt install zeek
   ```

2. Identify network interface
   ```bash
   ip addr show  # Look for eth0 or similar
   ```

3. Configure Zeek
   ```bash
   sudo nano /opt/zeek/etc/node.cfg
   # Set interface=eth0
   # Set type=standalone
   ```

4. Define local networks
   ```bash
   sudo nano /opt/zeek/site/local.zeek
   # Add: redef Site::local_nets += { 10.0.0.0/8, 192.168.0.0/16 };
   ```

5. Deploy Zeek
   ```bash
   sudo zeekctl deploy
   sudo zeekctl status  # Should show "running"
   ```

6. Generate test traffic
   ```bash
   curl https://example.com
   ```

7. Check logs
   ```bash
   tail -f /opt/zeek/logs/current/conn.log
   # Expect JSON entries for curl connection
   ```

**Verification:**
```bash
ls /opt/zeek/logs/current/
# Expect: conn.log, dns.log, http.log, etc.

cat /opt/zeek/logs/current/conn.log | jq . | head -n 20
# Expect valid JSON with src_ip, dest_ip, duration, etc.
```

---

#### Task 1.2: Suricata Installation (WSL2)
**Deliverable:** Suricata running with ET Open rules, generating eve.json alerts

**Steps:**
1. Install Suricata
   ```bash
   sudo apt install suricata
   ```

2. Download ET Open rules
   ```bash
   sudo suricata-update
   # This downloads and installs Emerging Threats rules
   ```

3. Configure Suricata
   ```bash
   sudo nano /etc/suricata/suricata.yaml
   # Set af-packet interface: eth0
   # Set HOME_NET: "[10.0.0.0/8,192.168.0.0/16]"
   # Enable EVE JSON: eve-log: enabled: yes
   ```

4. Test configuration
   ```bash
   sudo suricata -T -c /etc/suricata/suricata.yaml
   # Expect: "Configuration provided was successfully loaded"
   ```

5. Start Suricata
   ```bash
   sudo systemctl start suricata
   sudo systemctl status suricata  # Should be active
   ```

6. Generate test alert (DDoS simulation)
   ```bash
   # Use hping3 to trigger DOS rule
   sudo apt install hping3
   sudo hping3 -S -p 443 --flood localhost &
   # Let run for 5 seconds
   sudo killall hping3
   ```

7. Check alerts
   ```bash
   tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'
   # Expect alerts with signature containing "DOS" or "Flood"
   ```

**Verification:**
```bash
sudo suricata-update list-enabled-sources
# Expect: et/open

cat /var/log/suricata/eve.json | jq '.event_type' | sort | uniq
# Expect: "alert", "flow", "stats"
```

---

#### Task 1.3: Wazuh Agent Installation (Windows)
**Deliverable:** Wazuh agent monitoring Windows processes and logs

**Steps:**
1. Download Wazuh Agent MSI
   - URL: https://packages.wazuh.com/4.x/windows/
   - Version: 4.7.x (latest)

2. Install MSI
   - During install, set Manager IP to `127.0.0.1` (local demo mode)
   - Or install Wazuh Manager in WSL2 (advanced)

3. Start Wazuh service
   ```powershell
   Start-Service Wazuh
   Get-Service Wazuh  # Should be "Running"
   ```

4. Verify agent registration
   ```powershell
   # Check logs
   Get-Content "C:\Program Files (x86)\ossec-agent\ossec.log" -Tail 20
   # Expect: "Connected to the server"
   ```

5. Trigger test alert
   ```powershell
   # Open 50 fake processes to trigger CPU alert
   1..50 | ForEach-Object { Start-Process notepad }
   Start-Sleep 10
   Stop-Process -Name notepad -Force
   ```

6. Check Wazuh alerts
   ```bash
   # In WSL2 (if manager installed there)
   cat /var/ossec/logs/alerts/alerts.json | jq .
   ```

**Verification:**
```powershell
Get-Service Wazuh  # Status: Running
Get-Process | Where-Object {$_.Name -eq "ossec-agent"}  # Should exist
```

---

#### Task 1.4: osquery Installation (Windows)
**Deliverable:** osquery running and queryable for process/port info

**Steps:**
1. Install osquery
   ```powershell
   choco install osquery
   # Or download MSI from osquery.io
   ```

2. Start osquery service
   ```powershell
   Start-Service osqueryd
   ```

3. Test query
   ```powershell
   osqueryi
   > SELECT pid, name, path FROM processes WHERE name LIKE '%nginx%';
   > SELECT pid, port, protocol FROM listening_ports WHERE port = 443;
   ```

4. Create helper script `backend/utils/osquery_helper.py`:
   ```python
   import subprocess
   import json
   
   def query_listening_ports(port):
       cmd = f'osqueryi --json "SELECT pid, name FROM processes p JOIN listening_ports lp ON p.pid = lp.pid WHERE lp.port = {port}"'
       result = subprocess.run(cmd, shell=True, capture_output=True)
       return json.loads(result.stdout)
   ```

**Verification:**
```powershell
osqueryi --version  # Verify installed
osqueryi --json "SELECT COUNT(*) as process_count FROM processes"
# Expect JSON with process_count > 50
```

---

#### Task 1.5: Sensor Health Monitoring
**Deliverable:** Script to verify all sensors are running

**Create:** `sensors/check_health.sh` (WSL2)

```bash
#!/bin/bash

echo "=== Sensor Health Check ==="

# Check Zeek
if sudo zeekctl status | grep -q "running"; then
    echo "✅ Zeek: Running"
else
    echo "❌ Zeek: NOT running"
fi

# Check Suricata
if systemctl is-active --quiet suricata; then
    echo "✅ Suricata: Running"
else
    echo "❌ Suricata: NOT running"
fi

# Check log files exist
if [ -f /opt/zeek/logs/current/conn.log ]; then
    echo "✅ Zeek conn.log exists"
else
    echo "❌ Zeek conn.log missing"
fi

if [ -f /var/log/suricata/eve.json ]; then
    echo "✅ Suricata eve.json exists"
else
    echo "❌ Suricata eve.json missing"
fi
```

Make executable: `chmod +x sensors/check_health.sh`

**Verification:**
```bash
./sensors/check_health.sh
# Expect all ✅ checks to pass
```

---

**Phase 1 Success Criteria:**
- [ ] Zeek running in WSL2, generating conn.log
- [ ] Suricata running with ET rules, generating eve.json alerts
- [ ] Wazuh agent running on Windows host
- [ ] osquery installed and queryable
- [ ] All sensors passing health check script
- [ ] Test traffic generates logs in all sensors
- [ ] At least 1 test alert generated in Suricata

---

## 🔄 PHASE 2: Data Pipeline

**Goal:** Build log collection and forwarding from WSL2 sensors to Windows backend

**Duration:** 4-6 days  
**Dependencies:** Phase 0, Phase 1 complete  
**Risk:** Medium (WSL2 → Windows networking)

### Tasks

#### Task 2.1: Vector Installation & Configuration
**Deliverable:** Vector tailing Zeek/Suricata logs and forwarding to Windows

**Steps:**
1. Install Vector in WSL2
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.vector.dev | bash
   ```

2. Create `sensors/vector/vector.toml`:
   ```toml
   [sources.zeek_conn]
   type = "file"
   include = ["/opt/zeek/logs/current/conn.log"]
   read_from = "end"
   
   [sources.suricata_eve]
   type = "file"
   include = ["/var/log/suricata/eve.json"]
   read_from = "end"
   
   [transforms.parse_zeek]
   type = "remap"
   inputs = ["zeek_conn"]
   source = '''
   .sensor_type = "zeek"
   .timestamp = now()
   '''
   
   [transforms.parse_suricata]
   type = "remap"
   inputs = ["suricata_eve"]
   source = '''
   .sensor_type = "suricata"
   '''
   
   [sinks.to_api]
   type = "http"
   inputs = ["parse_zeek", "parse_suricata"]
   uri = "http://172.X.X.X:8000/api/ingest"  # Replace with Windows host IP
   encoding.codec = "json"
   batch.max_events = 10
   ```

3. Find Windows host IP from WSL2
   ```bash
   cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
   # This is your Windows host IP (usually 172.X.X.X)
   ```

4. Update vector.toml with correct IP

5. Test Vector
   ```bash
   vector --config sensors/vector/vector.toml
   # Should start without errors
   ```

**Verification:**
```bash
# In another terminal, generate traffic
curl https://example.com

# Check Vector logs
# Expect: "Forwarded X events to http://172.X.X.X:8000/api/ingest"
```

---

#### Task 2.2: FastAPI Ingest Endpoint (Stub)
**Deliverable:** Basic /api/ingest endpoint that receives logs

**Create:** `backend/routes/ingest.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class LogEvent(BaseModel):
    sensor_type: str
    timestamp: str
    data: Dict[str, Any]

@router.post("/ingest")
async def ingest_logs(event: LogEvent):
    """Receive logs from Vector"""
    logger.info(f"Received {event.sensor_type} log: {event.data}")
    
    # TODO: Phase 3 will add ML detection here
    # For now, just acknowledge receipt
    
    return {"status": "received", "sensor": event.sensor_type}
```

**Create:** `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ingest
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="XAI-IDS Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api", tags=["ingest"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

**Start server:**
```powershell
cd F:\program-ppt
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Verification:**
```powershell
# Test health endpoint
curl http://localhost:8000/api/health
# Expect: {"status":"healthy","version":"1.0.0"}

# Test ingest endpoint
curl -X POST http://localhost:8000/api/ingest -H "Content-Type: application/json" -d '{"sensor_type":"test","timestamp":"2026-01-29T12:00:00Z","data":{"src_ip":"1.2.3.4"}}'
# Expect: {"status":"received","sensor":"test"}
```

---

#### Task 2.3: Redis Connection Setup
**Deliverable:** Redis client wrapper for storing live alerts

**Create:** `backend/database/redis_client.py`

```python
import redis
from typing import Dict, List
import json
from datetime import timedelta

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def add_alert_to_stream(self, alert: Dict) -> str:
        """Add alert to Redis stream"""
        alert_id = self.client.xadd('alerts:stream', alert, maxlen=1000)
        return alert_id
    
    def get_recent_alerts(self, count=50) -> List[Dict]:
        """Get last N alerts from stream"""
        alerts = self.client.xrevrange('alerts:stream', count=count)
        return [data for _, data in alerts]
    
    def store_incident(self, incident_id: str, data: Dict, ttl_hours=24):
        """Store incident in hash with TTL"""
        key = f"incident:{incident_id}"
        self.client.hset(key, mapping=data)
        self.client.expire(key, timedelta(hours=ttl_hours))
    
    def get_incident(self, incident_id: str) -> Dict:
        """Retrieve incident data"""
        key = f"incident:{incident_id}"
        return self.client.hgetall(key)
```

**Test:**
```python
# In Python console
from backend.database.redis_client import RedisClient
rc = RedisClient()
rc.add_alert_to_stream({"test": "data", "timestamp": "2026-01-29T12:00:00Z"})
alerts = rc.get_recent_alerts(1)
print(alerts)  # Expect: [{'test': 'data', 'timestamp': '2026-01-29T12:00:00Z'}]
```

**Verification:**
```powershell
redis-cli
> XLEN alerts:stream
# Expect: (integer) 1
```

---

#### Task 2.4: PostgreSQL Connection Pool
**Deliverable:** SQLAlchemy models and connection setup

**Create:** `backend/database/models.py`

```python
from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, ARRAY, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Incident(Base):
    __tablename__ = 'incidents'
    
    incident_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    severity = Column(Integer)
    attack_type = Column(String(50))
    status = Column(String(20), default='active')
    source_ip = Column(INET)
    dest_ip = Column(INET)
    dest_port = Column(Integer)
    confidence = Column(Float)
    detection_method = Column(String(50))  # "signature" or "heuristic"
    alert_count = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)

class Alert(Base):
    __tablename__ = 'alerts'
    
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(UUID(as_uuid=True), ForeignKey('incidents.incident_id'))
    timestamp = Column(TIMESTAMP, server_default=func.now())
    sensor_type = Column(String(20))
    raw_data = Column(JSON)
    packet_rate = Column(Float)
    flow_duration = Column(Float)
    protocol_entropy = Column(Float)
    signature_id = Column(Integer)
    mitre_attack = Column(ARRAY(Text))
```

**Create:** `backend/database/postgres.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/xai_ids")

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
```

**Verification:**
```python
from backend.database.postgres import init_db, get_db
from backend.database.models import Incident

init_db()  # Create tables
db = next(get_db())
count = db.query(Incident).count()
print(f"Incidents in DB: {count}")  # Expect: 0 initially
```

---

**Phase 2 Success Criteria:**
- [ ] Vector installed and running in WSL2
- [ ] Vector forwarding logs to Windows FastAPI
- [ ] FastAPI ingest endpoint receiving logs
- [ ] Redis client storing alerts in stream
- [ ] PostgreSQL connection pool established
- [ ] SQLAlchemy models defined
- [ ] Test log reaches backend and is acknowledged
- [ ] No network errors between WSL2 and Windows

---

## 🤖 PHASE 3: Rule-Based Detection Engine

**Goal:** Implement heuristic detection using Suricata signatures + Zeek behavioral thresholds

**Duration:** 3-4 days  
**Dependencies:** Phase 0, 1, 2 complete  
**Risk:** Low (proven signature-based detection)

### Rationale for Rule-Based Approach

Instead of training ML models, we use:
- **Suricata signatures** for known attack patterns (95%+ accuracy)
- **Zeek behavioral metrics** with simple thresholds for anomaly detection
- **AI explanation layer** for the "XAI" value proposition

**Advantages:**
- No ML training/debugging (saves 5-7 days)
- No model accuracy risks during demo
- More reliable for college MVP
- Still delivers "glass box" explainability through rule-based logic

### Tasks

#### Task 3.1: Create Heuristic Detection Service
**Deliverable:** Rule-based threat classification service

**Create:** `backend/services/heuristic_detection.py`

```python
from typing import Dict, Tuple

def detect_attack(alert_data: dict) -> dict:
    """
    Rule-based detection using Suricata signatures + Zeek heuristics
    NO ML MODEL REQUIRED
    
    Args:
        alert_data: Combined data from Suricata alert + Zeek conn.log
    
    Returns:
        {attack_type, severity, confidence, reason}
    """
    attack_type = "Unknown"
    severity = 3  # Medium default
    confidence = 0.95  # High confidence (rule-based)
    reason = "Signature match"
    
    # Extract metrics
    signature = alert_data.get("signature", "")
    packet_rate = alert_data.get("packet_rate", 0)
    port_diversity = alert_data.get("port_diversity", 0)
    flow_duration = alert_data.get("flow_duration", 0)
    bytes_total = alert_data.get("bytes_total", 0)
    
    # Rule 1: Suricata signature-based detection
    if "DOS" in signature or "Flood" in signature:
        attack_type = "DDoS"
        severity = 1  # Critical
        reason = f"Suricata rule: {signature}"
    
    elif "SQL" in signature or "Injection" in signature:
        attack_type = "SQL Injection"
        severity = 1
        reason = f"Suricata rule: {signature}"
    
    elif "Brute" in signature or "Authentication" in signature:
        attack_type = "Brute Force"
        severity = 2  # High
        reason = f"Suricata rule: {signature}"
    
    elif "Scan" in signature or "Reconnaissance" in signature:
        attack_type = "Port Scan"
        severity = 2
        reason = f"Suricata rule: {signature}"
    
    # Rule 2: Zeek behavioral heuristics (fallback if no Suricata match)
    elif packet_rate > 10000:  # >10k packets/sec
        attack_type = "DDoS (High Packet Rate)"
        severity = 1
        confidence = 0.90
        reason = f"Abnormal packet rate: {packet_rate}/sec (threshold: 10000)"
    
    elif port_diversity > 50:  # Contacted 50+ unique ports
        attack_type = "Port Scan"
        severity = 2
        confidence = 0.85
        reason = f"High port diversity: {port_diversity} ports (threshold: 50)"
    
    elif flow_duration > 300 and bytes_total > 1000000000:  # 5+ min, 1GB+
        attack_type = "Data Exfiltration"
        severity = 1
        confidence = 0.80
        reason = f"Suspicious long flow: {flow_duration}s, {bytes_total} bytes"
    
    return {
        "attack_type": attack_type,
        "severity": severity,
        "confidence": confidence,
        "reason": reason
    }
```

**Detection Thresholds:**

| Heuristic | Threshold | Attack Type | Severity |
|-----------|-----------|-------------|----------|
| Packet Rate | > 10,000/sec | DDoS | Critical (1) |
| Port Diversity | > 50 unique ports | Port Scan | High (2) |
| Flow Duration + Bytes | > 300s AND > 1GB | Data Exfiltration | Critical (1) |
| Failed Logins (from Wazuh) | > 20 in 5 min | Brute Force | High (2) |

**Verification:**
```python
from backend.services.heuristic_detection import detect_attack

# Test DDoS detection
test_alert = {
    "signature": "ET DOS UDP Flood Inbound",
    "packet_rate": 18500,
    "port_diversity": 1,
    "flow_duration": 180,
    "bytes_total": 2400000000
}

result = detect_attack(test_alert)
print(result)
# Expect: {"attack_type": "DDoS", "severity": 1, "confidence": 0.95, "reason": "Suricata rule: ET DOS UDP Flood Inbound"}
```

---

#### Task 3.2: Feature Extraction for Rule-Based Detection
**Deliverable:** Script to extract behavioral metrics from Zeek logs

**Create:** `backend/services/feature_extraction.py`

```python
from typing import Dict

def extract_features_from_zeek(conn_log: Dict) -> Dict:
    """Extract behavioral metrics from Zeek conn.log entry"""
    
    duration = conn_log.get('duration', 0.0)
    orig_bytes = conn_log.get('orig_bytes', 0)
    resp_bytes = conn_log.get('resp_bytes', 0)
    orig_pkts = conn_log.get('orig_pkts', 0)
    
    # Calculate metrics for rule-based detection
    packet_rate = orig_pkts / duration if duration > 0 else 0
    bytes_total = orig_bytes + resp_bytes
    
    return {
        'packet_rate': packet_rate,
        'flow_duration': duration,
        'bytes_total': bytes_total,
        'port_diversity': conn_log.get('port_diversity', 1),
        'protocol': conn_log.get('proto', 'tcp'),
        'conn_state': conn_log.get('conn_state', 'S0')
    }
```

**Verification:**
```python
test_log = {
    'duration': 180,
    'orig_bytes': 1000000,
    'resp_bytes': 1400000,
    'orig_pkts': 18500,
    'conn_state': 'SF',
    'proto': 'udp'
}
features = extract_features_from_zeek(test_log)
print(features)
# Expect: {'packet_rate': 102.78, 'flow_duration': 180, ...}
```

---

#### Task 3.3: Evidence Formatting Service
**Deliverable:** Format detection results for UI display (threshold-based explanations)

**Create:** `backend/services/evidence_formatter.py`

```python
from typing import Dict

def format_evidence(alert_data: dict, detection_result: dict) -> dict:
    """
    Structure evidence for UI consumption (threshold-based, no SHAP)
    """
    return {
        "zeek_analysis": {
            "packet_rate": {
                "value": alert_data.get("packet_rate", 0),
                "unit": "packets/sec",
                "threshold": 10000,
                "impact": "High" if alert_data.get("packet_rate", 0) > 10000 else "Normal",
                "exceeded_by": f"{alert_data.get('packet_rate', 0) - 10000}/sec"
            },
            "flow_duration": {
                "value": alert_data.get("flow_duration", 0),
                "unit": "seconds",
                "threshold": 300,
                "impact": "High" if alert_data.get("flow_duration", 0) > 300 else "Normal"
            },
            "bytes_transferred": {
                "value": alert_data.get("bytes_total", 0),
                "unit": "bytes",
                "threshold": 1000000000,
                "impact": "High" if alert_data.get("bytes_total", 0) > 1000000000 else "Normal",
                "exceeded_by": f"{(alert_data.get('bytes_total', 0) - 1000000000) / 1000000:.1f} MB"
            }
        },
        "suricata_alert": {
            "signature_id": alert_data.get("signature_id"),
            "rule_name": alert_data.get("signature"),
            "classification": detection_result["attack_type"],
            "mitre_attack": alert_data.get("mitre_attack", [])
        },
        "detection_reason": detection_result["reason"]
    }

def calculate_severity(detection_result: dict, alert_count: int) -> int:
    """
    Simple severity scoring based on attack type + alert frequency
    
    Returns: 1 (Critical), 2 (High), 3 (Medium), 4 (Low)
    """
    base_severity = detection_result["severity"]
    
    # Escalate if multiple alerts in short time
    if alert_count > 10:
        base_severity = max(1, base_severity - 1)  # Bump up one level
    
    return base_severity
```

**Test:**
```python
from backend.services.evidence_formatter import format_evidence, calculate_severity

test_alert = {
    "packet_rate": 18500,
    "flow_duration": 180,
    "bytes_total": 2400000000,
    "signature_id": 2024050402,
    "signature": "ET DOS UDP Flood Inbound",
    "mitre_attack": ["T1498.001"]
}

test_detection = {
    "attack_type": "DDoS",
    "severity": 1,
    "confidence": 0.95,
    "reason": "Suricata rule: ET DOS UDP Flood Inbound"
}

evidence = format_evidence(test_alert, test_detection)
print(evidence)
# Expect: Structured evidence with threshold comparisons

severity = calculate_severity(test_detection, 5)
print(f"Severity: {severity}")  # Expect: 1
```

**Verification:**
```python
assert evidence["zeek_analysis"]["packet_rate"]["impact"] == "High"
assert evidence["zeek_analysis"]["packet_rate"]["threshold"] == 10000
assert "suricata_alert" in evidence
assert severity in [1, 2, 3, 4]
```

---

#### Task 3.4: AI API Integration Service
**Deliverable:** Real-time AI explanation service using OpenAI/Anthropic API

**Create:** `backend/services/ai_chat.py`

```python
import os
import httpx
from typing import Dict, List
from datetime import datetime

class AIChatService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4")
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    async def get_explanation(self, incident_data: dict, user_question: str = None) -> Dict:
        """
        Get AI explanation for incident using real API
        """
        # Build defensive prompt with incident context
        system_prompt = self._build_system_prompt(incident_data)
        
        # Default question if none provided
        if not user_question:
            user_question = "Explain this incident in simple terms"
        
        # Call AI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=10.0
            )
        
        if response.status_code != 200:
            raise Exception(f"AI API error: {response.text}")
        
        result = response.json()
        ai_content = result['choices'][0]['message']['content']
        
        return {
            "role": "assistant",
            "content": ai_content,
            "timestamp": datetime.utcnow().isoformat(),
            "model": self.model,
            "tokens_used": result.get('usage', {}).get('total_tokens', 0)
        }
    
    def _build_system_prompt(self, incident_data: dict) -> str:
        """Build defensive security prompt with incident context"""
        return f"""You are a cybersecurity AI assistant helping a junior analyst investigate an incident.

INCIDENT CONTEXT:
- Incident ID: {incident_data.get('incident_id')}
- Attack Type: {incident_data.get('attack_type')}
- Severity: {incident_data.get('severity')}
- Source IP: {incident_data.get('source_ip')} ({incident_data.get('country', 'Unknown')})
- Target: {incident_data.get('target_service')} on port {incident_data.get('dest_port')}
- Confidence: {incident_data.get('confidence', 95)}%

DETECTION EVIDENCE:
- Detection Method: {incident_data.get('detection_reason', 'Rule-based')}
- Packet Rate: {incident_data.get('packet_rate', 'Unknown')}/sec (threshold: 10,000/sec)
- Duration: {incident_data.get('duration_seconds', 'Unknown')}s
- Bytes Transferred: {incident_data.get('bytes_total', 'Unknown')}
- Suricata Match: {incident_data.get('signature_name', 'Unknown')}

INSTRUCTIONS:
1. Explain in plain language (beginner-friendly)
2. Focus ONLY on defensive actions
3. Cite specific evidence from the context (e.g., "Packet rate of 18,500/sec exceeded normal threshold")
4. Structure response: Summary, Reasons, Evidence, Actions
5. Refuse any requests for offensive techniques
6. If uncertain, admit limitations
7. Always provide actionable defensive recommendations

RESPONSE FORMAT:
📋 SUMMARY
[1-2 sentence plain language explanation]

🔍 WHY / REASON
[Bullet points explaining the logic]

📊 EVIDENCE
[Specific data points from logs/sensors]

✅ RECOMMENDED ACTIONS / NEXT STEPS
[Numbered list of defensive actions]

🛡️ CONFIDENCE LEVEL
[High/Medium/Low with brief justification]"""

# Offensive content filter
OFFENSIVE_KEYWORDS = [
    "exploit", "hack into", "penetrate", "attack", 
    "crack", "break into", "payload", "reverse shell"
]

def check_offensive_content(message: str) -> bool:
    """Check if message contains offensive intent"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in OFFENSIVE_KEYWORDS)
```

**Create:** `backend/routes/chat.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from backend.services.ai_chat import AIChatService, check_offensive_content

router = APIRouter()
ai_service = AIChatService()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    incident_id: str
    message: str
    conversation_history: List[ChatMessage] = []

@router.post("/chat")
async def ai_chat(request: ChatRequest):
    """
    AI assistant for incident explanation (defensive only, real API)
    """
    # Check for offensive content
    if check_offensive_content(request.message):
        return {
            "role": "assistant",
            "content": "🚫 I can't help with that request.\n\n" +
                      "My purpose is to help you DEFEND your systems, not attack others.\n\n" +
                      "Is there anything else about defending against this incident I can help with?",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Fetch incident from database
    # (simplified - full implementation queries incident details)
    incident_data = {
        "incident_id": request.incident_id,
        "attack_type": "DDoS",
        "severity": "Critical",
        "source_ip": "192.168.1.45",
        "country": "Russia",
        "target_service": "Web Server",
        "dest_port": 443,
        "confidence": 95,
        "detection_reason": "Suricata rule: ET DOS UDP Flood Inbound",
        "packet_rate": 18500,
        "duration_seconds": 180,
        "bytes_total": 2400000000,
        "signature_name": "ET DOS UDP Flood Inbound"
    }
    
    # Get AI response from real API
    try:
        ai_response = await ai_service.get_explanation(incident_data, request.message)
        return ai_response
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
```

**Configuration:**

In `backend/config.yaml`:
```yaml
ai:
  openai_api_key: "${OPENAI_API_KEY}"  # Required - get from OpenAI dashboard
  model: "gpt-4"  # Options: gpt-4, gpt-3.5-turbo
  max_tokens: 500
  temperature: 0.7
  timeout_seconds: 10
```

**Environment Variables:**
```bash
# Required for AI chat functionality
export OPENAI_API_KEY="sk-your-key-here"

# Optional - defaults shown
export AI_MODEL="gpt-4"
```

**API Costs (Estimated):**
- GPT-4: ~$0.03 per conversation (input + output tokens)
- GPT-3.5-turbo: ~$0.002 per conversation
- For demo with 50 conversations: $1.50 (GPT-4) or $0.10 (GPT-3.5)

**Requirements Update:**
Add to `backend/requirements.txt`:
```
httpx==0.26.0  # For async HTTP requests to AI API
```

**Features:**
- ✅ Real-time dynamic responses to any question
- ✅ Consistent formatting with defensive focus
- ✅ Offensive content filtering
- ✅ Token usage tracking
- ✅ Error handling for API failures
- ✅ Configurable model and parameters

---

#### Task 3.5: Integrate Rule-Based Detection into Ingest
**Deliverable:** Ingest endpoint runs heuristic detection on incoming logs

**Update:** `backend/routes/ingest.py`

```python
from backend.services.heuristic_detection import detect_attack
from backend.services.feature_extraction import extract_features_from_zeek
from backend.database.redis_client import RedisClient
from backend.database.postgres import get_db
from backend.database.models import Incident, Alert
from fastapi import Depends
from sqlalchemy.orm import Session

redis_client = RedisClient()

@router.post("/ingest")
async def ingest_logs(event: LogEvent, db: Session = Depends(get_db)):
    """Receive logs from Vector and run rule-based detection"""
    
    # Process Zeek conn logs
    if event.sensor_type == "zeek":
        # Extract behavioral metrics
        features_dict = extract_features_from_zeek(event.data)
        
        # Run rule-based detection
        detection_result = detect_attack(features_dict)
        
        if detection_result["severity"] <= 2:  # Critical or High
            # Store alert in Redis
            alert_data = {
                'sensor_type': 'zeek',
                'timestamp': event.timestamp,
                'source_ip': event.data.get('src_ip'),
                'dest_ip': event.data.get('dest_ip'),
                'dest_port': event.data.get('dest_port'),
                'attack_type': detection_result['attack_type'],
                'confidence': detection_result['confidence'],
                'detection_reason': detection_result['reason'],
                'packet_rate': features_dict.get('packet_rate'),
                'flow_duration': features_dict.get('flow_duration'),
                'bytes_total': features_dict.get('bytes_total'),
                'threat_detected': True
            }
            redis_client.add_alert_to_stream(alert_data)
            
            # TODO: Phase 4 will add incident creation logic
            
            return {"status": "threat_detected", "attack_type": detection_result['attack_type'], "confidence": detection_result['confidence']}
    
    return {"status": "benign"}
```

**Verification:**
Send test Zeek log via Vector → Check Redis for alert

```powershell
redis-cli XLEN alerts:stream
# Expect: > 0 if threats detected
```

---

**Phase 3 Success Criteria:**
- [ ] Heuristic detection function implemented
- [ ] Feature extraction working for behavioral metrics
- [ ] Detection thresholds configured (packet_rate: 10000, port_diversity: 50)
- [ ] Rule-based classification working (Suricata signatures + Zeek heuristics)
- [ ] Evidence formatting service implemented
- [ ] AI API integration service implemented (OpenAI/Anthropic)
- [ ] AI chat endpoint functional with real API responses
- [ ] Ingest endpoint running rule-based detection
- [ ] Test alert stored in Redis with detection reason
- [ ] Critical/High severity threats trigger alerts
- [ ] API key configured and tested

---

## 🔗 PHASE 4: Backend API Services

**Goal:** Build all REST API endpoints for UI pages

**Duration:** 7-10 days  
**Dependencies:** Phase 0-3 complete  
**Risk:** Medium (complex correlation logic)

### Tasks

#### Task 4.1: Incident Correlation Service
**Deliverable:** Logic to group alerts into incidents

**Create:** `backend/services/correlation.py`

```python
from datetime import datetime, timedelta
from typing import Optional
from backend.database.redis_client import RedisClient
from backend.database.postgres import SessionLocal
from backend.database.models import Incident, Alert
import uuid

class CorrelationEngine:
    def __init__(self):
        self.redis = RedisClient()
    
    def find_existing_incident(
        self, 
        source_ip: str, 
        dest_ip: str, 
        dest_port: int,
        attack_type: str,
        time_window_minutes=5
    ) -> Optional[str]:
        """
        Check if an incident exists matching these keys within time window
        """
        db = SessionLocal()
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        
        incident = db.query(Incident).filter(
            Incident.source_ip == source_ip,
            Incident.dest_ip == dest_ip,
            Incident.dest_port == dest_port,
            Incident.attack_type == attack_type,
            Incident.updated_at >= cutoff_time,
            Incident.status == 'active'
        ).first()
        
        db.close()
        
        return str(incident.incident_id) if incident else None
    
    def create_incident(
        self,
        source_ip: str,
        dest_ip: str,
        dest_port: int,
        attack_type: str,
        confidence: float,
        severity: int
    ) -> str:
        """Create new incident in database"""
        db = SessionLocal()
        
        incident = Incident(
            incident_id=uuid.uuid4(),
            source_ip=source_ip,
            dest_ip=dest_ip,
            dest_port=dest_port,
            attack_type=attack_type,
            confidence=confidence,
            severity=severity,
            alert_count=1
        )
        
        db.add(incident)
        db.commit()
        db.refresh(incident)
        
        incident_id = str(incident.incident_id)
        db.close()
        
        # Store in Redis for fast access
        self.redis.store_incident(incident_id, {
            'source_ip': source_ip,
            'dest_ip': dest_ip,
            'severity': severity,
            'attack_type': attack_type
        })
        
        return incident_id
    
    def add_alert_to_incident(
        self,
        incident_id: str,
        alert_data: dict
    ):
        """Add alert to existing incident"""
        db = SessionLocal()
        
        alert = Alert(
            incident_id=uuid.UUID(incident_id),
            sensor_type=alert_data['sensor_type'],
            raw_data=alert_data,
            packet_rate=alert_data.get('packet_rate'),
            flow_duration=alert_data.get('flow_duration')
        )
        
        db.add(alert)
        
        # Update incident
        incident = db.query(Incident).filter(
            Incident.incident_id == uuid.UUID(incident_id)
        ).first()
        
        if incident:
            incident.alert_count += 1
            incident.updated_at = datetime.utcnow()
        
        db.commit()
        db.close()
```

**Integrate into ingest endpoint** (update from Task 3.5)

**Verification:**
Send 3 alerts with same src_ip → Check DB for 1 incident with alert_count=3

---

#### Task 4.2: Dashboard API Endpoint
**Deliverable:** GET /api/dashboard/alerts with filtering

**Create:** `backend/routes/dashboard.py`

```python
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from backend.database.postgres import get_db
from backend.database.models import Incident
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/alerts")
async def get_dashboard_alerts(
    time_range: str = Query("15m", regex="^(5m|15m|1h|24h)$"),
    severity: Optional[str] = Query(None),
    attack_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Get filtered list of incidents for dashboard
    """
    # Calculate time range
    time_map = {"5m": 5, "15m": 15, "1h": 60, "24h": 1440}
    minutes = time_map.get(time_range, 15)
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    
    # Build query
    query = db.query(Incident).filter(Incident.created_at >= cutoff)
    
    if severity:
        severity_map = {"critical": 1, "high": 2, "medium": 3, "low": 4}
        query = query.filter(Incident.severity == severity_map[severity])
    
    if attack_type:
        query = query.filter(Incident.attack_type == attack_type)
    
    if status:
        query = query.filter(Incident.status == status)
    
    # Get total count
    total_count = query.count()
    
    # Paginate
    incidents = query.order_by(Incident.created_at.desc()).offset(offset).limit(limit).all()
    
    # Format response
    alerts = [
        {
            "incident_id": f"INC-{incident.created_at.year}-{str(incident.incident_id)[:4].upper()}",
            "severity": ["critical", "high", "medium", "low"][incident.severity - 1],
            "timestamp": incident.created_at.isoformat(),
            "attack_type": incident.attack_type,
            "source_ip": str(incident.source_ip),
            "target": f"Port {incident.dest_port}",
            "confidence": int(incident.confidence * 100),
            "status": incident.status
        }
        for incident in incidents
    ]
    
    return {
        "total_count": total_count,
        "alerts": alerts,
        "statistics": {
            "total_24h": db.query(Incident).filter(
                Incident.created_at >= datetime.utcnow() - timedelta(hours=24)
            ).count(),
            "critical_active": db.query(Incident).filter(
                Incident.severity == 1,
                Incident.status == 'active'
            ).count()
        }
    }
```

**Verification:**
```powershell
curl "http://localhost:8000/api/dashboard/alerts?time_range=15m"
# Expect JSON with "total_count" and "alerts" array
```

---

#### Task 4.3: Incident Details API
**Deliverable:** GET /api/incidents/{id} with full context

(See Backend Spec document for full implementation - 200+ lines)

**Key features:**
- Join incidents + alerts + endpoint_context tables
- Include geolocation lookup
- Format timeline events
- Format threshold-based evidence for UI (no SHAP needed)
- Include Suricata signature details

**Verification:**
```powershell
curl "http://localhost:8000/api/incidents/INC-2026-0142"
# Expect full JSON matching spec in Backend document
```

---

#### Task 4.4: AI Chat Endpoint
**Deliverable:** POST /api/chat with defensive prompt

**Create:** `backend/routes/chat.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import httpx

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    incident_id: str
    message: str
    conversation_history: List[ChatMessage] = []

OFFENSIVE_KEYWORDS = [
    "exploit", "hack into", "penetrate", "attack", 
    "crack", "break into", "payload", "reverse shell"
]

def check_offensive_content(message: str) -> bool:
    """Check if message contains offensive intent"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in OFFENSIVE_KEYWORDS)

@router.post("/chat")
async def ai_chat(request: ChatRequest):
    """
    AI assistant for incident explanation (defensive only)
    """
    # Check for offensive content
    if check_offensive_content(request.message):
        return {
            "role": "assistant",
            "content": "🚫 I can't help with that request.\n\n" +
                      "My purpose is to help you DEFEND your systems, not attack others.\n\n" +
                      "Is there anything else about defending against this incident I can help with?",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Fetch incident context from database
    # (simplified - full implementation queries incident details)
    incident_context = f"Incident {request.incident_id}: DDoS attack from 192.168.1.45"
    
    # Construct defensive prompt
    system_prompt = f"""You are a cybersecurity AI assistant helping a junior analyst.

INCIDENT CONTEXT:
{incident_context}

INSTRUCTIONS:
1. Explain in plain language (beginner-friendly)
2. Focus ONLY on defensive actions
3. Structure response with: Summary, Reasons, Evidence, Actions
4. Refuse any offensive technique requests

USER QUESTION: {request.message}

RESPONSE:"""
    
    # Call OpenAI API (or local LLM)
    api_key = os.getenv("OPENAI_API_KEY")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "max_tokens": 500
            }
        )
    
    ai_response = response.json()['choices'][0]['message']['content']
    
    return {
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.utcnow().isoformat()
    }
```

**Verification:**
Test offensive refusal:
```powershell
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"incident_id":"INC-2026-0142","message":"How do I hack this system?"}'
# Expect refusal message
```

---

#### Task 4.5: WebSocket Server
**Deliverable:** Real-time alert broadcasting to connected clients

**Create:** `backend/websocket/server.py`

```python
import socketio
from typing import Set

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)

# Track connected clients
connected_clients: Set[str] = set()

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    connected_clients.add(sid)
    await sio.emit('connection_status', {'connected': True}, room=sid)
    print(f"Client {sid} connected. Total: {len(connected_clients)}")

@sio.event
async def disconnect(sid):
    """Handle client disconnect"""
    connected_clients.discard(sid)
    print(f"Client {sid} disconnected. Total: {len(connected_clients)}")

@sio.event
async def subscribe(sid, data):
    """Client subscribes to specific alerts"""
    filters = data.get('filters', {})
    # Store filters for this client (simplified - use Redis in production)
    print(f"Client {sid} subscribed with filters: {filters}")
    await sio.emit('subscribed', {'status': 'success'}, room=sid)

async def broadcast_new_alert(alert_data: dict):
    """
    Broadcast new alert to all connected clients
    Called from ingest endpoint when threat detected
    """
    await sio.emit('new_alert', alert_data)

# Integrate with FastAPI
from fastapi import FastAPI
app_sio = socketio.ASGIApp(sio)
```

**Update `main.py` to mount WebSocket:**
```python
from backend.websocket.server import app_sio

app.mount("/ws", app_sio)
```

**Verification:**
Use Socket.IO client library in browser console:
```javascript
const socket = io('http://localhost:8000/ws');
socket.on('new_alert', (data) => console.log('Alert:', data));
```

---

**Phase 4 Success Criteria:**
- [ ] Incident correlation grouping alerts correctly
- [ ] Dashboard API returning filtered incidents
- [ ] Incident details API providing full context
- [ ] AI chat endpoint functional with defensive checks
- [ ] WebSocket server broadcasting alerts
- [ ] All endpoints passing basic tests
- [ ] API documented in /docs (Swagger)

---

## 🎨 PHASE 5: Frontend UI

**Goal:** Build React UI with 3 pages matching specification

**Duration:** 7-10 days  
**Dependencies:** Phase 4 complete  
**Risk:** Low-Medium (UI complexity)

### Tasks

#### Task 5.1: React Project Setup
**Deliverable:** React app with routing and folder structure

**Steps:**
1. Create React app
   ```powershell
   cd F:\program-ppt
   npx create-react-app frontend
   cd frontend
   ```

2. Install dependencies
   ```powershell
   npm install react-router-dom axios socket.io-client @mui/material @emotion/react @emotion/styled recharts
   ```

3. Create folder structure
   ```
   frontend/src/
   ├── components/
   │   ├── Dashboard/
   │   ├── IncidentDetails/
   │   ├── AIChat/
   │   └── common/
   ├── pages/
   │   ├── LiveFeedPage.jsx
   │   ├── AttributionPage.jsx
   │   └── AIChatPage.jsx
   ├── services/
   │   ├── api.js
   │   └── websocket.js
   └── App.jsx
   ```

4. Setup routing in `App.jsx`
   ```jsx
   import { BrowserRouter, Routes, Route } from 'react-router-dom';
   import LiveFeedPage from './pages/LiveFeedPage';
   import AttributionPage from './pages/AttributionPage';
   import AIChatPage from './pages/AIChatPage';
   
   function App() {
     return (
       <BrowserRouter>
         <Routes>
           <Route path="/" element={<LiveFeedPage />} />
           <Route path="/incident/:id" element={<AttributionPage />} />
           <Route path="/incident/:id/chat" element={<AIChatPage />} />
         </Routes>
       </BrowserRouter>
     );
   }
   ```

**Verification:**
```powershell
npm start
# Expect: App launches on http://localhost:3000
```

---

#### Task 5.2: API Service Layer
**Deliverable:** Axios client for backend API calls

**Create:** `frontend/src/services/api.js`

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const dashboardAPI = {
  getAlerts: (params) => apiClient.get('/dashboard/alerts', { params }),
};

export const incidentAPI = {
  getDetails: (incidentId) => apiClient.get(`/incidents/${incidentId}`),
};

export const chatAPI = {
  sendMessage: (data) => apiClient.post('/chat', data),
};

export default apiClient;
```

---

#### Task 5.3: PAGE 1 - Live Feed Dashboard
**Deliverable:** Functional dashboard showing live alerts

**Create:** `frontend/src/pages/LiveFeedPage.jsx`

(See UI Specification document for complete component structure)

**Key features:**
- Alert table with sortable columns
- Filter bar (time range, severity, attack type)
- Real-time WebSocket updates
- Click row → navigate to Attribution page
- Statistics bar at bottom

**Verification:**
1. Load page → see test alerts from database
2. Generate new alert → appears without refresh
3. Click alert row → navigate to incident details

---

#### Task 5.4: PAGE 2 - Attribution Details
**Deliverable:** Incident investigation page with AI button

**Create:** `frontend/src/pages/AttributionPage.jsx`

**Key features:**
- Incident header with severity badge
- Attacker info card (IP, geolocation, reputation)
- Target info card (port, service, process)
- Interactive timeline
- Evidence cards (Zeek, Suricata, Wazuh)
- Threshold-based evidence visualization (metrics vs. thresholds)
- **"Get AI Explanation" button** (prominent CTA)

**Button click behavior:**
```jsx
const handleAIExplanation = () => {
  navigate(`/incident/${incidentId}/chat`);
};
```

**Verification:**
1. Click alert from dashboard → incident details loads
2. All sections populate with data from API
3. Click "Get AI Explanation" → navigate to chat page

---

#### Task 5.5: PAGE 3 - AI Chat
**Deliverable:** Interactive chat interface with AI assistant

**Create:** `frontend/src/pages/AIChatPage.jsx`

**Key features:**
- Incident context summary (collapsible)
- Chat message area (scrollable)
- Auto-generated initial AI message on load
- Text input with send button
- Suggested question buttons
- Message bubbles (user vs. AI styling)

**Initial message generation:**
```jsx
useEffect(() => {
  // Auto-send initial explanation request on page load
  sendMessage("Explain this incident in simple terms");
}, []);
```

**Verification:**
1. Load page → initial AI explanation appears
2. Type question → response appears in <3 seconds
3. Click suggested question → sends message
4. Test offensive keyword → get refusal message

---

#### Task 5.6: WebSocket Integration
**Deliverable:** Real-time alert updates on dashboard

**Create:** `frontend/src/services/websocket.js`

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:8000/ws', {
  autoConnect: false
});

export const connectWebSocket = (onNewAlert) => {
  socket.connect();
  
  socket.on('connect', () => {
    console.log('WebSocket connected');
    socket.emit('subscribe', { filters: {} });
  });
  
  socket.on('new_alert', (data) => {
    console.log('New alert received:', data);
    onNewAlert(data);
  });
  
  socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
  });
  
  return socket;
};

export const disconnectWebSocket = () => {
  socket.disconnect();
};
```

**Use in LiveFeedPage:**
```jsx
useEffect(() => {
  const socket = connectWebSocket((newAlert) => {
    setAlerts(prev => [newAlert, ...prev]);
  });
  
  return () => disconnectWebSocket();
}, []);
```

---

#### Task 5.7: Styling & Responsiveness
**Deliverable:** Dark mode UI matching specification

**Create:** `frontend/src/styles/theme.js`

```javascript
export const theme = {
  colors: {
    critical: '#DC2626',
    high: '#F97316',
    medium: '#EAB308',
    low: '#22C55E',
    primary: '#6366F1',
    background: '#0F172A',
    cardBg: '#1E293B',
    textPrimary: '#F8FAFC',
    textSecondary: '#94A3B8'
  },
  spacing: {
    page: '24px',
    card: '16px',
    section: '24px'
  }
};
```

Apply theme using CSS-in-JS or styled-components

**Verification:**
- Test on desktop (1920x1080) → full layout
- Test on tablet (768px) → 2-column layout
- Test on mobile (375px) → single column

---

**Phase 5 Success Criteria:**
- [ ] React app running on localhost:3000
- [ ] Page 1 (Dashboard) displaying alerts from API
- [ ] WebSocket updating dashboard in real-time
- [ ] Page 2 (Attribution) showing full incident details
- [ ] "Get AI Explanation" button navigating to chat
- [ ] Page 3 (AI Chat) functional with auto-initial message
- [ ] All pages responsive (desktop/tablet/mobile)
- [ ] Dark mode theme applied matching spec
- [ ] Navigation between all 3 pages working

---

## 🧪 PHASE 6: Integration & Testing

**Goal:** End-to-end testing and bug fixes

**Duration:** 5-7 days  
**Dependencies:** All previous phases complete  
**Risk:** Medium (integration issues common)

### Tasks

#### Task 6.1: End-to-End Test Scenarios
**Deliverable:** Documented test cases with results

**Test Scenario 1: DDoS Attack Detection**

**Steps:**
1. Start all services (sensors, backend, frontend)
2. Generate DDoS traffic:
   ```bash
   # In WSL2
   sudo hping3 -S -p 443 --flood localhost
   ```
3. Wait 10 seconds
4. Stop hping3: `sudo killall hping3`

**Expected Results:**
- [ ] Zeek logs high packet rate in conn.log
- [ ] Suricata generates "DOS" alert in eve.json
- [ ] Vector forwards logs to FastAPI
- [ ] Rule-based detection classifies as DDoS (confidence 95%)
- [ ] Incident created in PostgreSQL
- [ ] Alert appears on dashboard within 500ms
- [ ] Click alert → incident details page loads
- [ ] Evidence shows packet_rate exceeded threshold (18,500 > 10,000)
- [ ] Click "Get AI Explanation" → chat opens
- [ ] AI provides defensive recommendations

**Record:** Screenshot each step, note any failures

---

#### Task 6.2: Performance Testing
**Deliverable:** Latency measurements vs. targets

**Metrics to measure:**

| Operation | Target | Actual | Pass/Fail |
|-----------|--------|--------|-----------|
| Sensor → Ingest API | <200ms | ___ | ___ |
| Heuristic Detection | <50ms | ___ | ___ |
| Evidence Formatting | <100ms | ___ | ___ |
| WebSocket Broadcast | <500ms | ___ | ___ |
| Dashboard API | <600ms | ___ | ___ |
| AI Chat Response | <5s | ___ | ___ |

**How to measure:**
- Add timing logs to backend:
  ```python
  import time
  start = time.time()
  # ... operation ...
  elapsed = time.time() - start
  logger.info(f"Operation took {elapsed:.3f}s")
  ```

- Use browser DevTools Network tab for API calls

---

#### Task 6.3: Error Handling & Edge Cases
**Deliverable:** System gracefully handles failures

**Test cases:**

1. **Sensor offline:** Stop Zeek → Backend should log warning, dashboard shows "No data"
2. **Database connection lost:** Stop PostgreSQL → API returns 503 error, UI shows error message
3. **Invalid input:** Send malformed JSON to /api/ingest → Returns 400 error
4. **AI API failure:** Set invalid OpenAI key → Chat returns "AI unavailable" message
5. **High load:** Send 200 alerts/second → System processes without crashing

**Fix any failures found**

---

#### Task 6.4: Security Validation
**Deliverable:** Verify defensive constraints work

**Test cases:**

1. **AI offensive refusal:**
   - Send "How do I exploit this vulnerability?" to chat
   - Expect: Refusal message displayed

2. **SQL injection prevention:**
   - Try SQL injection in dashboard filters
   - Expect: Query parameterization prevents attack

3. **XSS prevention:**
   - Try entering `<script>alert('xss')</script>` in chat
   - Expect: Sanitized before display

---

#### Task 6.5: User Acceptance Testing
**Deliverable:** Demo to test users (classmates, professor)

**Feedback form:**

1. Is the dashboard easy to understand? (1-5)
2. Are the incident details helpful? (1-5)
3. Is the AI explanation clear? (1-5)
4. Did you encounter any bugs? (describe)
5. What would you improve?

**Incorporate feedback into fixes**

---

**Phase 6 Success Criteria:**
- [ ] All end-to-end test scenarios pass
- [ ] Performance metrics meet targets
- [ ] Error handling prevents crashes
- [ ] Security validations pass
- [ ] User feedback >4/5 average rating
- [ ] No critical bugs remaining
- [ ] All features working as specified

---

## 🎬 PHASE 7: Demo Preparation

**Goal:** Polish for presentation and create demo assets

**Duration:** 3-5 days  
**Dependencies:** Phase 6 complete  
**Risk:** Low

### Tasks

#### Task 7.1: Demo Script Creation
**Deliverable:** Minute-by-minute presentation outline

**Demo Script (10-minute presentation):**

**0:00 - Introduction (1 min)**
- "Today I'll demo a Real-Time Explainable AI IDS..."
- Show problem: Black Box AI vs. Glass Box transparency

**1:00 - Live Dashboard (2 min)**
- Show dashboard with pre-loaded alerts
- Explain color coding (critical/high/medium/low)
- Filter by severity → show real-time filtering
- Click on DDoS alert

**3:00 - Incident Investigation (3 min)**
- Walk through incident details page
- "WHO attacked: Moscow, Russia IP"
- "WHAT was targeted: Web server on port 443"
- "WHEN: Timeline from first packet to detection"
- "HOW detected: Show threshold-based evidence"
- Explain: "Packet rate of 18,500/sec exceeded threshold of 10,000/sec"

**6:00 - AI Explanation (2 min)**
- Click "Get AI Explanation" button
- Show initial AI response (pre-generated)
- Ask question: "What should I do next?"
- Show defensive recommendations
- Test refusal: "How do I hack back?" → Show refusal message

**8:00 - Live Attack Demo (2 min)**
- Run hping3 DDoS script
- Watch alert appear on dashboard in real-time
- "From attack to alert in under 15 seconds"

**10:00 - Conclusion (1 min)**
- Recap: "Glass Box AI for educational cybersecurity"
- Thank audience, open for questions

---

#### Task 7.2: Pre-Seed Demo Data
**Deliverable:** Database populated with realistic incidents

**Script to create demo data:**

```python
# backend/scripts/seed_demo_data.py

from backend.database.postgres import SessionLocal
from backend.database.models import Incident, Alert
from datetime import datetime, timedelta
import uuid

db = SessionLocal()

demo_incidents = [
    {
        'attack_type': 'DDoS',
        'source_ip': '192.168.1.45',
        'dest_ip': '10.0.0.5',
        'dest_port': 443,
        'severity': 1,
        'confidence': 0.98
    },
    {
        'attack_type': 'Brute Force',
        'source_ip': '203.0.113.42',
        'dest_ip': '10.0.0.10',
        'dest_port': 22,
        'severity': 2,
        'confidence': 0.87
    },
    # Add 5-10 more varied incidents
]

for inc_data in demo_incidents:
    incident = Incident(
        incident_id=uuid.uuid4(),
        created_at=datetime.utcnow() - timedelta(minutes=30),
        **inc_data
    )
    db.add(incident)

db.commit()
print(f"Seeded {len(demo_incidents)} demo incidents")
```

Run before demo: `python backend/scripts/seed_demo_data.py`

---

#### Task 7.3: Backup Demo Script
**Deliverable:** Pre-recorded video in case live demo fails

**Steps:**
1. Record screen using OBS Studio or Windows Game Bar
2. Perform full demo scenario
3. Save as MP4 (max 50MB for presentation)
4. Have ready on desktop as backup

---

#### Task 7.4: Presentation Slides
**Deliverable:** PowerPoint/PDF with visuals

**Slide outline:**

1. Title: "XAI-IDS: Glass Box Threat Detection"
2. Problem Statement: Black Box AI trust gap
3. Architecture Diagram (from Backend Spec doc)
4. Sensor Stack: Zeek + Suricata + Wazuh
5. Detection Pipeline: Rule-Based + AI Explanations (Zeek + Suricata + Heuristics)
6. UI Flow: Dashboard → Details → Chat
7. Live Demo (switch to actual app)
8. Results: Detection accuracy, response time
9. Lessons Learned
10. Future Work
11. Thank You + Questions

**Export as PDF for backup**

---

#### Task 7.5: Documentation Package
**Deliverable:** Complete project documentation

**Files to include:**

1. **README.md** - Setup instructions
2. **ARCHITECTURE.md** - System design overview
3. **API_DOCS.md** - Endpoint reference (from /docs)
4. **USER_GUIDE.md** - How to use the UI
5. **DEMO_SCRIPT.md** - Presentation outline
6. **project-details.md** - (Already created)
7. **XAI_IDS_UI_Specification.md** - (Already created)
8. **XAI_IDS_Backend_Specification.md** - (Already created)

Zip all docs: `XAI_IDS_Documentation.zip`

---

#### Task 7.6: Rehearsal
**Deliverable:** Smooth presentation with no technical issues

**Rehearsal checklist:**

- [ ] All services start without errors
- [ ] Dashboard loads in <3 seconds
- [ ] Demo data visible
- [ ] Live attack script works
- [ ] AI chat responds correctly
- [ ] Presentation fits in 10 minutes
- [ ] Backup video accessible
- [ ] Laptop fully charged
- [ ] External monitor tested (if presenting on projector)

**Do 3 full rehearsals before actual presentation**

---

**Phase 7 Success Criteria:**
- [ ] Demo script written and memorized
- [ ] Demo data pre-seeded in database
- [ ] Backup video recorded
- [ ] Presentation slides created
- [ ] All documentation complete
- [ ] Rehearsals completed successfully
- [ ] Confidence level: 9/10 or higher

---

## 📊 Project Timeline Summary

| Phase | Duration | Cumulative Time |
|-------|----------|----------------|
| Phase 0: Environment Setup | 3-5 days | 5 days |
| Phase 1: Sensor Infrastructure | 5-7 days | 12 days |
| Phase 2: Data Pipeline | 4-6 days | 18 days |
| Phase 3: Rule-Based Detection | 3-4 days | 22 days |
| Phase 4: Backend API Services | 7-10 days | 32 days |
| Phase 5: Frontend UI | 7-10 days | 42 days |
| Phase 6: Integration & Testing | 5-7 days | 49 days |
| Phase 7: Demo Preparation | 3-5 days | **54 days** |

**Total:** 5-6 weeks (assuming 6-7 work hours per day)

**Time Savings:** Using rule-based detection instead of ML saves 5-7 days and eliminates model accuracy risks.

---

## 🚨 Risk Mitigation

### High-Risk Areas

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| WSL2 networking issues | High | Medium | Use localhost forwarding, test early |
| Sensor not generating logs | Medium | High | Verify with test traffic after each install |
| Detection threshold tuning | Low | Medium | Test with sample traffic, adjust thresholds as needed |
| WebSocket connection failures | Medium | Medium | Implement reconnection logic, fallback to polling |
| AI API availability | High | High | Required OpenAI API key, test connectivity early, have backup explanation ready |
| Demo equipment failure | Low | High | Backup video, rehearse on actual presentation setup |

---

## ✅ Final Deliverables Checklist

**Code:**
- [ ] Backend repository with all services
- [ ] Frontend repository with UI
- [ ] Sensor configuration files
- [ ] Database schema and migrations

**Documentation:**
- [ ] README with setup instructions
- [ ] Architecture diagrams
- [ ] API documentation
- [ ] User guide

**Presentation:**
- [ ] Demo script
- [ ] Slide deck
- [ ] Backup video
- [ ] Live working demo

**Reports:**
- [ ] project-details.md (completed)
- [ ] XAI_IDS_UI_Specification.md (completed)
- [ ] XAI_IDS_Backend_Specification.md (completed)
- [ ] Technical report (8 pages)
- [ ] Narrative report (5 pages)

---

**Plan Version:** 1.0  
**Last Updated:** January 29, 2026  
**Estimated Completion:** March 27, 2026 (if started Feb 1, 2026)

