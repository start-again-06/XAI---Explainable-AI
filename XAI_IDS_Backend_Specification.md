# XAI-IDS Backend Architecture & Implementation Specification

## Project: Real-Time Explainable AI Intrusion Detection System
**Version:** 2.0 - Simplified Architecture  
**Date:** January 29, 2026  
**Document Type:** Backend Technical Specification (Code-Free)  
**Platform:** Windows 11 with WSL2 Hybrid Architecture

---

## 📋 Executive Summary

This document provides the complete backend architecture specification for the XAI-IDS system, detailing the **sensor infrastructure, data pipeline, API services, and real-time communication** required to power the 3-page UI. This is a **hybrid Windows/WSL2 deployment** optimized for college lab environments running on a single machine or small network.

### ✅ Simplified Architecture Rationale

**Why No Machine Learning Detection?**

This MVP focuses on **proven signature-based + heuristic detection** instead of training ML models:

| Traditional ML Approach | Simplified Approach (This Spec) |
|------------------------|--------------------------------|
| Train XGBoost on CICIDS2017 (5-7 days) | ❌ **Skip entirely** |
| Debug SHAP values + feature engineering | ❌ **Skip entirely** |
| Risk: Model accuracy <90% = failed demo | ✅ **No ML risk** |
| Detection: Zeek + Suricata + **ML fusion** | Detection: Zeek + Suricata **only** (proven tech) |
| AI API: Optional enhancement | AI API: **Core value** (explanation layer) |
| Demo complexity: High | Demo complexity: **Low** (more reliable) |

> 💡 **Key Insight:** Suricata + Zeek provide 95%+ accuracy for common attacks (DDoS, port scans, brute force) without ML complexity. The **AI layer provides explainability** by translating technical alerts into plain language, which is your "XAI" value proposition.

### Core Backend Objectives
1. **Ingest** real telemetry from Zeek, Suricata, and Wazuh sensors
2. **Detect** threats using proven signature-based (Suricata) + behavioral heuristics (Zeek)
3. **Correlate** individual alerts into incident threads (time-window grouping)
4. **Stream** live alerts to dashboard via WebSocket (<500ms latency)
5. **Explain** threats in plain language via AI chat assistant (OpenAI API - real-time dynamic responses)

**Advantages of This Approach:**
- ✅ **More achievable** (saves 1+ week of ML training/debugging)
- ✅ **More reliable** (no model accuracy risks during demo)
- ✅ **More focused** (AI explanation = unique value)
- ✅ **Still impressive** (real sensors + real-time UI + AI chat)
- ✅ **Real-time AI** (dynamic explanations via OpenAI API - ~$0.03 per conversation)

---

## 🏗️ System Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                    WINDOWS HOST (FastAPI Backend)                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐         ┌─────────────────┐                  │
│  │   PostgreSQL    │◄────────│   FastAPI App   │                  │
│  │  (Incidents DB) │         │  (Port 8000)    │                  │
│  └─────────────────┘         └────────┬────────┘                  │
│                                       │                            │
│  ┌─────────────────┐                 │                            │
│  │  Memurai/Redis  │◄────────────────┤                            │
│  │  (Live Window)  │                 │                            │
│  └─────────────────┘                 │                            │
│                                       │                            │
│  ┌─────────────────────────────────────────────────────┐          │
│  │         WebSocket Server (Socket.IO)                │          │
│  │  Real-time alert broadcast to React UI              │          │
│  └─────────────────────────────────────────────────────┘          │
│                          ▲                                         │
│                          │                                         │
│                   JSON Logs via TCP/File                           │
│                          │                                         │
├──────────────────────────┼─────────────────────────────────────────┤
│              WSL2 Ubuntu (Detection Layer)                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐         │
│  │    Zeek     │     │  Suricata   │     │   Vector    │         │
│  │ (Behavior)  │────►│ (Signature) │────►│(Log Shipper)│         │
│  └─────────────┘     └─────────────┘     └──────┬──────┘         │
│         │                   │                    │                │
│         │                   │                    │                │
│         └───────────────────┴────────────────────┘                │
│                             │                                      │
│                   conn.log / eve.json / alerts                    │
│                             │                                      │
└─────────────────────────────┼──────────────────────────────────────┘
                              ▼
                    Windows Host (localhost forwarding)

┌────────────────────────────────────────────────────────────────────┐
│              WINDOWS HOST (Endpoint Context)                        │
├────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                    ┌─────────────┐               │
│  │ Wazuh Agent │                    │  osquery    │               │
│  │ (MSI Install)│                   │ (Native)    │               │
│  └──────┬──────┘                    └──────┬──────┘               │
│         │                                  │                       │
│         └──────────────────┬───────────────┘                       │
│                            │                                       │
│                     Process Context                                │
│                   (PID, User, Service)                             │
│                            │                                       │
│                            ▼                                       │
│                   FastAPI Backend                                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Layer 1: Detection Sensors

### 1.1 Zeek (Network Behavior Analysis)

**Location:** WSL2 Ubuntu  
**Purpose:** Generate behavioral metadata logs (packet rates, connection patterns, protocol analysis)

#### Installation
```
Operating in WSL2 Ubuntu 22.04
Package: zeek (via apt or from zeek.org/get-zeek)
```

#### Configuration Requirements

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Interface** | eth0 (or mirror port) | Monitor all network traffic |
| **Log Format** | JSON | Easy parsing for behavioral metrics |
| **Log Location** | `/opt/zeek/logs/current/` | Standard location |
| **Rotation** | Hourly | Prevent log files from growing too large |
| **Scripts Enabled** | conn, dns, http, ssl | Cover major protocols |

#### Output Logs Required

**conn.log (Connection Records)**
- Source IP, Destination IP, Port
- Connection duration (seconds)
- Bytes transferred (orig_bytes, resp_bytes)
- Packet count
- Connection state (established, reset, etc.)

**dns.log (DNS Queries)**
- Query domain
- Response type
- TTL values
- Query frequency (for DGA detection)

**http.log (HTTP Requests)**
- Request URI
- Status codes
- User-agent strings
- Method (GET, POST)

#### Behavioral Metrics Extraction

From Zeek logs, extract these **behavioral metrics** for heuristic detection:

| Feature Name | Source Field | Data Type | Example Value |
|--------------|--------------|-----------|---------------|
| `packet_rate` | packet_count / duration | Float | 18500.0 (packets/sec) |
| `flow_duration` | duration | Float | 180.0 (seconds) |
| `bytes_total` | orig_bytes + resp_bytes | Integer | 2400000000 (bytes) |
| `connection_state` | conn_state | String | "SF" (complete) or "S0" (rejected) |
| `port_diversity` | Unique ports contacted | Integer | 1 (normal) or 100+ (scan) |
| `protocol` | proto | String | "tcp", "udp", "icmp" |

---

### 1.2 Suricata (Signature-Based IDS)

**Location:** WSL2 Ubuntu  
**Purpose:** Match traffic against rule signatures (ET Open, custom rules) and generate alerts

#### Installation
```
Operating in WSL2 Ubuntu 22.04
Package: suricata (via apt)
Rules: Emerging Threats (ET) Open Ruleset
```

#### Configuration Requirements

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Interface** | Same as Zeek (eth0) | Match traffic stream |
| **Output** | EVE JSON format | Structured alerts for parsing |
| **Log Location** | `/var/log/suricata/eve.json` | Standard location |
| **Rule Categories** | DOS, exploits, malware, policy | Cover main attack types |
| **MITRE Mapping** | Enabled | Link alerts to ATT&CK techniques |

#### EVE JSON Alert Structure

Required fields in each alert:

```json
{
  "timestamp": "2026-01-29T14:32:05.123Z",
  "event_type": "alert",
  "alert": {
    "signature": "ET DOS UDP Flood Inbound",
    "signature_id": 2024050402,
    "severity": 1,
    "category": "Attempted Denial of Service"
  },
  "src_ip": "192.168.1.45",
  "dest_ip": "10.0.0.5",
  "dest_port": 443,
  "proto": "UDP",
  "flow": {
    "pkts_toserver": 18500,
    "bytes_toserver": 2400000000
  },
  "mitre_attack": ["T1498.001"]
}
```

#### Rule Customization

Create custom rules for MVP demo scenarios:

**DDoS UDP Flood:**
```
alert udp any any -> $HOME_NET any (msg:"Custom UDP Flood Detected"; 
  threshold: type both, track by_src, count 10000, seconds 10; 
  classtype:attempted-dos; sid:9000001; rev:1;)
```

**SQL Injection Attempt:**
```
alert http any any -> $HOME_NET any (msg:"Custom SQL Injection Attempt"; 
  content:"UNION SELECT"; nocase; http_uri; 
  classtype:web-application-attack; sid:9000002; rev:1;)
```

---

### 1.3 Wazuh Agent (Endpoint Context)

**Location:** Windows Host (native MSI install)  
**Purpose:** Monitor processes, file integrity, and system logs to map network alerts to specific applications

#### Installation
```
Operating on Windows 11 Host
Package: Wazuh Agent MSI (from packages.wazuh.com/4.x/windows/)
Manager: Point to localhost or Wazuh server in WSL2
```

#### Configuration Requirements

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Log Monitoring** | Windows Event Logs, IIS logs | Catch application-level indicators |
| **Process Monitoring** | Real-time process tracking | Map dest_port to nginx/apache PID |
| **File Integrity** | Monitor web root directories | Detect post-exploit changes |
| **Syscollector** | Enabled | Inventory running services |

#### Critical Alerts to Forward

**Process Network Binding:**
- When a process opens a listening port (e.g., nginx on :443)
- Process ID (PID), user context, executable path

**High CPU/Memory Spike:**
- When a service exceeds 90% CPU during an incident
- Correlate with network alert timestamps

**Suspicious Process Execution:**
- Unknown binaries spawning on web server
- Command-line arguments indicating exploitation

#### API Integration

Wazuh exposes REST API for querying:

**Endpoint:** `GET /agents/{agent_id}/processes`  
**Returns:** List of running processes with PID, name, user, listening ports

Use this to populate **PAGE 2: Target Information Card** (Service Mapped field)

---

### 1.4 osquery (Optional Endpoint Telemetry)

**Location:** Windows Host (native MSI)  
**Purpose:** SQL-based endpoint queries for granular process/network info

#### Installation
```
Operating on Windows 11 Host
Package: osquery MSI or via Chocolatey (choco install osquery)
```

#### Key Tables to Query

**processes:**
- All running processes with PID, parent PID, name, path, user

**listening_ports:**
- Ports bound by processes (e.g., PID 1842 listening on :443)

**logged_in_users:**
- Active user sessions (detect compromised accounts)

#### Sample Query for Page 2

```sql
SELECT p.pid, p.name, p.cmdline, lp.port, lp.protocol
FROM processes p
JOIN listening_ports lp ON p.pid = lp.pid
WHERE lp.port = 443;
```

**Output:**
```
PID: 1842, Name: nginx.exe, Port: 443, Protocol: TCP6
```

This populates **"Service Mapped: nginx web server process"** in UI

---

## 📊 Layer 2: Data Pipeline

### 2.1 Vector (Log Collection & Normalization)

**Location:** WSL2 Ubuntu  
**Purpose:** Tail log files from Zeek/Suricata, parse JSON, forward to Windows host

#### Installation
```
Operating in WSL2 Ubuntu
Package: vector (from vector.dev)
```

#### Configuration Structure

**Source 1: Zeek conn.log**
- File path: `/opt/zeek/logs/current/conn.log`
- Parse JSON format
- Extract: src_ip, dest_ip, dest_port, duration, bytes, packets

**Source 2: Suricata eve.json**
- File path: `/var/log/suricata/eve.json`
- Filter: event_type == "alert"
- Extract: signature, severity, src_ip, dest_ip, dest_port, mitre_attack

**Transform: Add Timestamps**
- Ensure all logs have UTC ISO8601 timestamp
- Add `sensor_type` field ("zeek", "suricata")

**Sink: Forward to Windows FastAPI**
- Protocol: HTTP POST to `http://localhost:8000/api/ingest`
- Batch size: 10 events per request
- Retry logic: 3 attempts with exponential backoff

---

### 2.2 Redis/Memurai (Real-Time Event Buffer)

**Location:** Windows Host  
**Purpose:** In-memory store for "live window" of last 15 minutes of alerts

#### Installation
```
Operating on Windows 11
Package: Memurai (Redis-compatible, native Windows)
```

#### Data Structures

**Stream: `alerts:stream`**
- Redis Streams for time-ordered event log
- Auto-trim to last 15 minutes of data
- Each entry contains full alert JSON

**Hash: `incident:{incident_id}`**
- Store incident metadata (severity, attack_type, first_seen, last_seen)
- Updated as new alerts join the thread

**Set: `active_ips`**
- Track currently attacking source IPs
- Auto-expire after 30 minutes

**Sorted Set: `severity_scores`**
- Rank incidents by severity score (0-100)
- Used for dashboard "Critical Active" counter

#### TTL Policy

| Key Pattern | TTL | Rationale |
|-------------|-----|-----------|
| `alerts:*` | 15 minutes | Dashboard shows last 15 min |
| `incident:*` | 24 hours | Incident details available for 1 day |
| `active_ips` | 30 minutes | Stale IPs auto-removed |

---

### 2.3 PostgreSQL (Persistent Storage)

**Location:** Windows Host  
**Purpose:** Store incidents, alerts, attribution data, analyst notes, historical analysis

#### Installation
```
Operating on Windows 11
Package: PostgreSQL 15 (official installer)
```

#### Database Schema

**Table: `incidents`**

| Column | Type | Description |
|--------|------|-------------|
| `incident_id` | UUID PRIMARY KEY | Unique identifier (e.g., INC-2026-0142) |
| `created_at` | TIMESTAMP | First alert timestamp |
| `updated_at` | TIMESTAMP | Last alert timestamp |
| `severity` | INTEGER (1-4) | 1=Critical, 2=High, 3=Medium, 4=Low |
| `attack_type` | VARCHAR(50) | DDoS, Brute Force, SQL Injection, etc. |
| `status` | VARCHAR(20) | Active, Investigating, Contained, Resolved |
| `source_ip` | INET | Attacker IP address |
| `dest_ip` | INET | Target IP address |
| `dest_port` | INTEGER | Target port |
| `confidence` | FLOAT | Detection confidence (0.0 - 1.0) |
| `detection_method` | VARCHAR(50) | "signature" or "heuristic" |
| `alert_count` | INTEGER | Number of alerts in this thread |
| `duration_seconds` | INTEGER | Time span from first to last alert |

**Table: `alerts`**

| Column | Type | Description |
|--------|------|-------------|
| `alert_id` | SERIAL PRIMARY KEY | Auto-increment ID |
| `incident_id` | UUID FOREIGN KEY | Links to incidents table |
| `timestamp` | TIMESTAMP | When alert was generated |
| `sensor_type` | VARCHAR(20) | zeek, suricata, wazuh |
| `raw_data` | JSONB | Full original alert JSON |
| `packet_rate` | FLOAT | Zeek-derived metric |
| `flow_duration` | FLOAT | Zeek-derived metric |
| `protocol_entropy` | FLOAT | Zeek-derived metric |
| `signature_id` | INTEGER | Suricata rule SID (if applicable) |
| `mitre_attack` | TEXT[] | Array of ATT&CK IDs |

**Table: `endpoint_context`**

| Column | Type | Description |
|--------|------|-------------|
| `context_id` | SERIAL PRIMARY KEY | Auto-increment ID |
| `incident_id` | UUID FOREIGN KEY | Links to incidents |
| `process_name` | VARCHAR(100) | e.g., "nginx.exe" |
| `process_id` | INTEGER | PID |
| `process_user` | VARCHAR(50) | e.g., "www-data" |
| `cpu_usage` | FLOAT | CPU % during incident |
| `memory_usage` | BIGINT | Memory in bytes |
| `source` | VARCHAR(20) | wazuh or osquery |

**Table: `analyst_notes`**

| Column | Type | Description |
|--------|------|-------------|
| `note_id` | SERIAL PRIMARY KEY | Auto-increment ID |
| `incident_id` | UUID FOREIGN KEY | Links to incidents |
| `created_at` | TIMESTAMP | When note was added |
| `analyst_name` | VARCHAR(100) | User who added note |
| `note_text` | TEXT | Free-form investigation notes |

#### Indexes

```
CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_source_ip ON incidents(source_ip);
CREATE INDEX idx_alerts_incident_id ON alerts(incident_id);
CREATE INDEX idx_alerts_timestamp ON alerts(timestamp);
```

---

## 🧠 Layer 3: Detection & Correlation Engine

### 3.1 Heuristic Detection Service

**Purpose:** Rule-based threat classification using Suricata signatures + Zeek behavioral metrics

**Why No ML?** For a college MVP, proven signature-based detection (Suricata) + simple heuristics (Zeek thresholds) provide 95%+ accuracy without the complexity of training/tuning ML models. The AI API provides the "explainability" layer.

#### Detection Logic

**Create:** `backend/services/heuristic_detection.py`

```python
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
        reason = f"Abnormal packet rate: {packet_rate}/sec"
    
    elif port_diversity > 50:  # Contacted 50+ unique ports
        attack_type = "Port Scan"
        severity = 2
        confidence = 0.85
        reason = f"High port diversity: {port_diversity} ports"
    
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

#### Detection Thresholds

| Heuristic | Threshold | Attack Type | Severity |
|-----------|-----------|-------------|----------|
| Packet Rate | > 10,000/sec | DDoS | Critical (1) |
| Port Diversity | > 50 unique ports | Port Scan | High (2) |
| Flow Duration + Bytes | > 300s AND > 1GB | Data Exfiltration | Critical (1) |
| Failed Logins (from Wazuh) | > 20 in 5 min | Brute Force | High (2) |

**Note:** These thresholds are tunable based on your network baseline.

---

### 3.2 Evidence Extraction for UI

**Purpose:** Format detection results for PAGE 2: Attribution Details display

```python
def format_evidence(alert_data: dict, detection_result: dict) -> dict:
    """
    Structure evidence for UI consumption (no SHAP needed)
    """
    return {
        "zeek_analysis": {
            "packet_rate": {
                "value": alert_data.get("packet_rate", 0),
                "unit": "packets/sec",
                "impact": "High" if alert_data.get("packet_rate", 0) > 10000 else "Normal",
                "threshold": 10000
            },
            "flow_duration": {
                "value": alert_data.get("flow_duration", 0),
                "unit": "seconds",
                "impact": "High" if alert_data.get("flow_duration", 0) > 300 else "Normal",
                "threshold": 300
            },
            "bytes_transferred": {
                "value": alert_data.get("bytes_total", 0),
                "unit": "bytes",
                "impact": "High" if alert_data.get("bytes_total", 0) > 1000000000 else "Normal"
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
```

**Key Difference from ML Approach:**
- ✅ No SHAP values needed
- ✅ Simple threshold comparisons ("High" vs "Normal")
- ✅ Clear, rule-based explanations ("Packet rate exceeded 10k threshold")

---

### 3.3 Incident Threading (Correlation Logic)

**Purpose:** Group individual alerts into coherent "incidents" to reduce noise

#### Grouping Strategy: Time-Window + Key Matching

**Algorithm:**

```
For each new alert:
  1. Extract keys: (source_ip, dest_ip, dest_port, attack_type)
  2. Check Redis for existing incident matching these keys
  3. If match found AND last_alert_time < 5 minutes ago:
       → Add alert to existing incident
       → Update incident.updated_at
       → Increment incident.alert_count
  4. Else:
       → Create new incident
       → Generate incident_id (UUID)
       → Store in PostgreSQL + Redis
```

#### Incident ID Generation

**Format:** `INC-YYYY-NNNN`  
**Example:** `INC-2026-0142`

- YYYY = Year
- NNNN = Sequential number (from database sequence)

#### Severity Scoring

Simplified rule-based severity (no ML confidence needed):

```python
def calculate_severity(detection_result: dict, alert_count: int) -> int:
    """
    Simple severity scoring based on attack type + alert frequency
    
    Returns: 1 (Critical), 2 (High), 3 (Medium), 4 (Low)
    """
    base_severity = detection_result["severity"]  # From heuristic detection
    
    # Escalate if multiple alerts in short time
    if alert_count > 10:
        base_severity = max(1, base_severity - 1)  # Bump up one level
    
    return base_severity
```

**Severity Levels:**
- **Critical (1):** DDoS, SQL Injection, Data Exfiltration
- **High (2):** Brute Force, Port Scan
- **Medium (3):** Policy violations, suspicious patterns
- **Low (4):** Informational alerts

---

## 🚀 Layer 4: API Services (FastAPI)

### 4.1 Backend Framework

**Technology:** FastAPI (Python 3.11+)  
**Location:** Windows Host  
**Port:** 8000 (HTTP)

#### Project Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── config.py                # Environment variables, DB connections, AI API keys
├── routes/
│   ├── ingest.py            # POST /api/ingest (from Vector)
│   ├── dashboard.py         # GET /api/dashboard/alerts
│   ├── incidents.py         # GET /api/incidents/{id}
│   ├── chat.py              # POST /api/chat (AI assistant)
│   └── actions.py           # POST /api/actions/block_ip
├── services/
│   ├── heuristic_detection.py  # Rule-based threat classification
│   ├── correlation.py          # Incident threading logic
│   ├── geolocation.py          # IP → country lookup
│   ├── endpoint.py             # Query Wazuh/osquery APIs
│   └── ai_chat.py              # Real-time AI API integration (OpenAI/Anthropic)
├── database/
│   ├── postgres.py          # PostgreSQL connection pool
│   ├── redis.py             # Redis client
│   └── schema.sql           # Database schema DDL
├── websocket/
│   └── server.py            # Socket.IO server for live updates
└── utils/
    ├── mitre.py             # Map Suricata SID → MITRE ATT&CK
    └── defensive_ai.py      # AI chat prompt templates
```

---

### 4.2 API Endpoint Specifications

#### **POST /api/ingest**

**Purpose:** Receive parsed logs from Vector (Zeek/Suricata)

**Request Body:**
```json
{
  "sensor_type": "zeek",
  "timestamp": "2026-01-29T14:32:05.123Z",
  "data": {
    "src_ip": "192.168.1.45",
    "dest_ip": "10.0.0.5",
    "dest_port": 443,
    "duration": 180,
    "packets": 18500,
    "bytes": 2400000000
  }
}
```

**Process:**
1. Parse incoming log
2. Extract behavioral metrics (packet_rate, port_diversity, etc.)
3. Run heuristic detection (rule-based classification)
4. If threat detected:
   - Check for existing incident (correlation)
   - Store alert in PostgreSQL + Redis
   - Broadcast via WebSocket to connected clients

**Response:**
```json
{
  "status": "processed",
  "incident_id": "INC-2026-0142",
  "threat_detected": true
}
```

---

#### **GET /api/dashboard/alerts**

**Purpose:** Fetch live alerts for PAGE 1: Live Feed Dashboard

**Query Parameters:**
- `time_range` (5m, 15m, 1h, 24h, custom)
- `severity` (all, critical, high, medium, low)
- `attack_type` (all, ddos, bruteforce, sqli, portscan)
- `status` (all, active, investigating, resolved)
- `limit` (default: 50)
- `offset` (for pagination)

**Response:**
```json
{
  "total_count": 142,
  "alerts": [
    {
      "incident_id": "INC-2026-0142",
      "severity": "critical",
      "severity_icon": "🔴",
      "timestamp": "2026-01-29T14:32:05Z",
      "attack_type": "DDoS",
      "source_ip": "192.168.1.45",
      "source_country": "🇷🇺 Russia",
      "target": "Web Server :443",
      "confidence": 98,
      "quick_reason": "Abnormal packet rate",
      "status": "active"
    }
  ],
  "statistics": {
    "total_24h": 287,
    "critical_active": 3,
    "avg_response_time_seconds": 15
  }
}
```

**Data Source:** Redis `alerts:stream` + PostgreSQL for statistics

---

#### **GET /api/incidents/{incident_id}**

**Purpose:** Fetch full details for PAGE 2: Attribution Details

**Path Parameter:** `incident_id` (e.g., INC-2026-0142)

**Response:**
```json
{
  "incident_id": "INC-2026-0142",
  "severity": "critical",
  "attack_type": "DDoS - UDP Flood",
  "status": "active",
  "timestamps": {
    "first_seen": "2026-01-29T14:32:00Z",
    "last_seen": "2026-01-29T14:32:15Z",
    "duration_seconds": 15
  },
  "attacker": {
    "source_ip": "192.168.1.45",
    "geolocation": {
      "city": "Moscow",
      "country": "Russia",
      "country_code": "RU",
      "flag": "🇷🇺"
    },
    "reputation": "Known Malicious (5 previous incidents)",
    "related_ips": []
  },
  "target": {
    "dest_ip": "10.0.0.5",
    "dest_port": 443,
    "service": "HTTPS",
    "process": {
      "name": "nginx",
      "pid": 1842,
      "user": "www-data",
      "cpu_usage": 98.0
    },
    "context": "Traffic hit the main production web server"
  },
  "timeline": [
    {
      "timestamp": "2026-01-29T14:32:00Z",
      "event": "First packet received"
    },
    {
      "timestamp": "2026-01-29T14:32:02Z",
      "event": "Packet rate exceeded threshold (18,500/sec)"
    },
    {
      "timestamp": "2026-01-29T14:32:03Z",
      "event": "Suricata Alert: Volumetric DDoS Detected"
    },
    {
      "timestamp": "2026-01-29T14:32:05Z",
      "event": "XAI-IDS Detection: DDoS Attack (High Confidence)"
    }
  ],
  "evidence": {
    "zeek_analysis": {
      "packet_rate": {
        "value": 18500.0,
        "unit": "packets/sec",
        "threshold": 10000,
        "impact": "High",
        "exceeded_by": "8500/sec (185% over threshold)"
      },
      "flow_duration": {
        "value": 180,
        "unit": "seconds",
        "threshold": 300,
        "impact": "Normal"
      },
      "bytes_transferred": {
        "value": 2400000000,
        "unit": "bytes",
        "threshold": 1000000000,
        "impact": "High",
        "exceeded_by": "1.4 GB over threshold"
      }
    },
    "suricata_alert": {
      "signature_id": 2024050402,
      "rule_name": "ET DOS UDP Flood Inbound",
      "classification": "Attempted Denial of Service",
      "mitre_attack": ["T1498.001"]
    },
    "endpoint_context": {
      "process": "nginx (PID 1842)",
      "user": "www-data",
      "cpu_spike": true,
      "cpu_before": 15,
      "cpu_during": 98,
      "memory_impact": "Moderate"
    }
  },
  "detection_method": {
    "type": "rule-based",
    "confidence": 0.95,
    "reason": "Suricata signature match: ET DOS UDP Flood Inbound",
    "contributing_factors": [
      "Packet rate: 18,500/sec (exceeded 10k threshold by 185%)",
      "Flow duration: 180 seconds (sustained attack)",
      "Bytes transferred: 2.4 GB (volumetric attack)"
    ]
  }
}
```

**Data Source:** PostgreSQL incidents table + JOIN with alerts, endpoint_context

---

#### **POST /api/chat**

**Purpose:** AI assistant for PAGE 3: AI Chat Explanation

**Request Body:**
```json
{
  "incident_id": "INC-2026-0142",
  "message": "Is this attacker likely to try again?",
  "conversation_history": [
    {
      "role": "assistant",
      "content": "Initial explanation..."
    }
  ]
}
```

**Process:**
1. Fetch incident details from database
2. Format context for AI (incident summary + evidence)
3. Construct prompt with defensive constraints
4. Call AI API (OpenAI/Anthropic/local LLM)
5. Parse response into structured format
6. Return to frontend

**Response:**
```json
{
  "role": "assistant",
  "content": "Based on the attack pattern, here's my assessment:\n\n🔄 LIKELIHOOD OF REPEAT: Moderate to High\n\nWhy:\n• The attacker used automated tools (high packet rate)\n• Attack stopped suddenly (may be probing defenses)\n• This IP has 5 previous incidents in threat databases\n\n🛡️ PREVENTIVE MEASURES\n• Keep the IP blocked for at least 24-48 hours\n• Monitor for attacks from similar IP ranges\n• Consider a DDoS mitigation service for future protection\n\nWould you like me to explain any of these steps in detail?",
  "timestamp": "2026-01-29T14:33:10Z"
}
```

**AI Prompt Template (Defensive Design):**

```
You are a cybersecurity AI assistant helping a junior analyst investigate an incident.

INCIDENT CONTEXT:
- Incident ID: {incident_id}
- Attack Type: {attack_type}
- Severity: {severity}
- Source IP: {source_ip} ({country})
- Target: {target_service} on port {port}
- Confidence: {confidence}%

DETECTION EVIDENCE:
- Detection Method: {detection_reason}
- Packet Rate: {packet_rate}/sec (threshold: 10,000/sec)
- Duration: {duration}s
- Bytes Transferred: {bytes_total}
- Suricata Match: {signature_name}

USER QUESTION: {user_message}

INSTRUCTIONS:
1. Explain in plain language (beginner-friendly)
2. Focus ONLY on defensive actions
3. Cite specific evidence from the context (e.g., "Packet rate of 18,500/sec exceeded normal threshold")
4. Structure response: Summary, Reasons, Evidence, Actions
5. Refuse any requests for offensive techniques
6. If uncertain, admit limitations

RESPONSE:
```

**Ethical Constraint Checks:**

- Block keywords: "exploit", "hack into", "attack", "penetrate"
- If detected, return refusal message:
  ```
  🚫 I can't help with that request.
  My purpose is to help you DEFEND your systems, not attack others.
  ```

---

#### **POST /api/actions/block_ip**

**Purpose:** Quick action to block attacker IP (demo purposes)

**Request Body:**
```json
{
  "incident_id": "INC-2026-0142",
  "source_ip": "192.168.1.45",
  "duration_hours": 24
}
```

**Process:**
1. Validate IP address
2. Add to firewall blocklist (demo: just log the action)
3. Update incident status to "Contained"
4. Store action in analyst_notes table

**Response:**
```json
{
  "status": "success",
  "message": "IP 192.168.1.45 blocked for 24 hours",
  "action_id": "ACT-2026-5891"
}
```

---

#### **Real-Time AI API Integration**

**Purpose:** Provide dynamic, context-aware explanations using OpenAI/Anthropic API

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
        """Get AI explanation for incident using real API"""
        system_prompt = self._build_system_prompt(incident_data)
        
        if not user_question:
            user_question = "Explain this incident in simple terms"
        
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
        return f"""You are a cybersecurity AI assistant helping a junior analyst.

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
3. Cite specific evidence from the context
4. Structure response: Summary, Reasons, Evidence, Actions
5. Refuse any requests for offensive techniques
6. Always provide actionable defensive recommendations"""

# Offensive content filter
OFFENSIVE_KEYWORDS = ["exploit", "hack into", "penetrate", "attack", "crack", "break into", "payload", "reverse shell"]

def check_offensive_content(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in OFFENSIVE_KEYWORDS)
```

**Configuration:**

In `config.yaml`:
```yaml
ai:
  openai_api_key: "${OPENAI_API_KEY}"  # Required - get from OpenAI dashboard
  model: "gpt-4"  # Options: gpt-4, gpt-3.5-turbo
  max_tokens: 500
  temperature: 0.7
  timeout_seconds: 10
```

**API Costs (Estimated):**
- GPT-4: ~$0.03 per conversation (input + output tokens)
- GPT-3.5-turbo: ~$0.002 per conversation
- For demo with 50 conversations: $1.50 (GPT-4) or $0.10 (GPT-3.5)

**Requirements:**
Add to `requirements.txt`:
```
httpx==0.26.0  # For async HTTP requests to AI API
```

**Setup Instructions:**
1. Create OpenAI account at https://platform.openai.com
2. Generate API key from dashboard
3. Set environment variable: `export OPENAI_API_KEY="sk-your-key-here"`
4. Test connectivity before demo

**Features:**
- ✅ Real-time dynamic responses to any question
- ✅ Context-aware explanations using incident data
- ✅ Consistent defensive formatting
- ✅ Offensive content filtering
- ✅ Token usage tracking
- ✅ Error handling for API failures
- ✅ Configurable model (GPT-4 or GPT-3.5-turbo)

---

### 4.3 WebSocket Server (Real-Time Updates)

**Purpose:** Push new alerts to dashboard instantly (<500ms latency)

#### Implementation

**Library:** `python-socketio` with FastAPI integration  
**Protocol:** Socket.IO (WebSocket with fallback to polling)

#### Events

**Server → Client Events:**

| Event Name | Payload | When Triggered |
|------------|---------|----------------|
| `new_alert` | Full alert JSON | New incident created |
| `alert_update` | Updated incident JSON | Alert added to existing incident |
| `status_change` | {incident_id, new_status} | Analyst changes status |
| `connection_status` | {connected: true} | Client connects |

**Client → Server Events:**

| Event Name | Payload | Purpose |
|------------|---------|---------|
| `subscribe` | {filters: {severity: "critical"}} | Subscribe to specific alerts |
| `unsubscribe` | {} | Stop receiving updates |

#### Connection Flow

```
1. React frontend connects: socket.io.connect('ws://localhost:8000')
2. Server authenticates (optional for MVP)
3. Client sends 'subscribe' with filters
4. Server adds client to broadcast list
5. On new alert: server.emit('new_alert', alert_json)
6. React updates UI state (no page refresh needed)
```

---

## 🔐 Layer 5: Security & Validation

### 5.1 Input Validation

**All API endpoints must validate:**

| Input | Validation Rule | Example |
|-------|-----------------|---------|
| IP addresses | IPv4/IPv6 format | Reject "999.999.999.999" |
| Timestamps | ISO8601 UTC | Reject "Jan 29 2:32pm" |
| Severity | Enum: critical, high, medium, low | Reject "super_critical" |
| Attack type | Predefined list | Reject SQL injection in field |
| Incident ID | UUID or INC-YYYY-NNNN format | Reject arbitrary strings |

### 5.2 Rate Limiting

**API Endpoints:**

| Endpoint | Rate Limit | Window |
|----------|------------|--------|
| `/api/ingest` | 1000 req/min | Per sensor IP |
| `/api/dashboard/*` | 60 req/min | Per client IP |
| `/api/chat` | 10 req/min | Per user (prevent AI spam) |

### 5.3 Authentication (Optional for MVP)

**Simple API Key:**
- Header: `X-API-Key: {secret_key}`
- Validate against environment variable
- Reject unauthorized requests with 401

**For Production (Future):**
- JWT tokens with user roles
- Role-based access control (analyst vs. admin)

---

## 📈 Layer 6: Performance Requirements

### 6.1 Latency Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Sensor → Ingest API | < 100ms | 200ms |
| Heuristic Detection | < 10ms | 50ms |
| Correlation Logic | < 50ms | 100ms |
| WebSocket Broadcast | < 500ms | 1000ms |
| Dashboard API Response | < 300ms | 600ms |
| AI Chat Response (OpenAI API) | < 3s | 5s |

### 6.2 Throughput Targets

| Metric | Target | Scaling Strategy |
|--------|--------|------------------|
| Alerts/sec processed | 100 | Batch processing in ingest |
| Concurrent WebSocket clients | 10 | Sufficient for lab demo |
| Database writes/sec | 50 | Connection pooling |
| Redis operations/sec | 500 | Single-node sufficient |

### 6.3 Storage Estimates

**For 24-hour operation with moderate traffic:**

| Data Type | Daily Volume | Storage |
|-----------|--------------|---------|
| Zeek conn.log | ~1M connections | 500 MB JSON |
| Suricata eve.json | ~10K alerts | 50 MB JSON |
| PostgreSQL incidents | ~500 incidents | 10 MB |
| Redis live window | Last 15 min | 5 MB in-memory |

**Total:** ~1 GB per day (manageable for single-machine MVP)

---

## 🧪 Layer 7: Testing Strategy

### 7.1 Unit Tests

**Test Coverage:**

| Component | Test Cases |
|-----------|------------|
| Heuristic Detection | Feed known DDoS metrics (packet_rate=15000) → expect attack_type="DDoS", severity=1 |
| Threshold Logic | Test packet_rate=9000 (below 10k) → expect Normal, packet_rate=11000 → expect High |
| Correlation Logic | Feed 5 alerts with same src_ip within 5 min → expect 1 incident with alert_count=5 |
| Geolocation | Lookup 8.8.8.8 → expect "United States" |
| API Validation | POST invalid JSON to /api/ingest → expect 400 error |

### 7.2 Integration Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| **End-to-End Alert Flow** | 1. Send Zeek log to ingest<br>2. Heuristic detection classifies threat<br>3. Alert stored in DB<br>4. WebSocket broadcasts | Dashboard shows new alert in <500ms |
| **Incident Threading** | 1. Send 3 alerts from same IP<br>2. All within 5 min window | Single incident created with alert_count=3 |
| **AI Chat Refusal** | 1. Ask "How do I hack this system?"<br>2. AI processes request | AI returns refusal message, logs attempt |

### 7.3 Demo Attack Scenarios

**Scenario 1: DDoS UDP Flood**
- Use `hping3` to generate high packet rate traffic
- Target: localhost:443
- Expected: Zeek logs high packet_rate, Suricata matches ET DOS rule, incident created with severity=Critical

**Scenario 2: Port Scan**
- Use `nmap -p 1-1000 localhost`
- Expected: Zeek logs high port diversity, incident created with attack_type=Port Scan

**Scenario 3: Brute Force (Simulated)**
- Script sends 50 failed login attempts to SSH
- Expected: Wazuh logs failed auth events, incident created with attack_type=Brute Force

---

## 🚀 Layer 8: Deployment & Operations

### 8.1 Environment Setup

#### 🚫 Tools You Can SKIP (Since No ML)

**Cost & Time Savings from Simplified Architecture:**

| Tool | Reason to Skip | Time Saved | Cost Saved |
|------|---------------|------------|------------|
| **XGBoost / SHAP** | Not needed – rule-based detection replaces ML | 5-7 days training/tuning | $0 (no compute) |
| **CICIDS2017 dataset** | No training required | 2-3 hours download/preprocessing | ~10GB storage |
| **scikit-learn, pandas (for ML)** | Only needed for feature engineering if using ML | N/A | Smaller deployment |
| **NVIDIA GPU** | Not required for signature/heuristic detection | N/A | $0 (no GPU instance) |
| **Jupyter Notebook** | No model experiments needed | N/A | Cleaner environment |
| **TensorBoard / MLflow** | No model tracking needed | N/A | Simpler deployment |

**What You DO Need (Minimal Stack):**

✅ **Detection:** Zeek + Suricata (proven, battle-tested)  
✅ **Backend:** Python + FastAPI + PostgreSQL + Redis  
✅ **AI:** OpenAI API (real-time dynamic responses)  
✅ **Frontend:** React + Socket.IO  

> 💡 **Budget Impact:** Skipping ML saves ~$50-200 in cloud GPU costs and 1 week of development time. Your "XAI" value comes from the AI explanation layer, not ML detection.

---

#### Installation Steps

**Windows Host:**
```powershell
# Install Python 3.11
winget install Python.Python.3.11

# Install PostgreSQL
winget install PostgreSQL.PostgreSQL

# Install Memurai
# Download from memurai.com

# Create virtual environment
python -m venv F:\program-ppt\.venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis python-socketio pandas numpy httpx maxminddb python-dotenv
```

**WSL2 Ubuntu:**
```bash
# Install sensors
sudo apt update
sudo apt install zeek suricata

# Install Vector
curl --proto '=https' --tlsv1.2 -sSf https://sh.vector.dev | bash

# Configure network interface
sudo zeek -i eth0 local "Site::local_nets += { 10.0.0.0/8 }"
```

### 8.2 Configuration Files

**config.yaml** (Windows Host)
```yaml
database:
  postgres_url: "postgresql://user:pass@localhost:5432/xai_ids"
  redis_url: "redis://localhost:6379/0"

detection:
  packet_rate_threshold: 10000
  port_diversity_threshold: 50
  flow_duration_threshold: 300
  bytes_exfiltration_threshold: 1000000000

sensors:
  zeek_log_path: "\\\\wsl$\\Ubuntu\\opt\\zeek\\logs\\current\\conn.log"
  suricata_log_path: "\\\\wsl$\\Ubuntu\\var\\log\\suricata\\eve.json"

ai:
  openai_api_key: "${OPENAI_API_KEY}"  # Required - get from OpenAI dashboard
  model: "gpt-4"  # Options: gpt-4, gpt-3.5-turbo
  max_tokens: 500
  temperature: 0.7
  timeout_seconds: 10

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["http://localhost:3000"]

websocket:
  max_connections: 10

geolocation:
  maxmind_db_path: "data/GeoLite2-City.mmdb"
```

### 8.3 Startup Sequence

**1. Start Infrastructure (Windows):**
```powershell
# Start PostgreSQL service
Start-Service postgresql-x64-15

# Start Memurai
Start-Service Memurai

# Initialize database schema
python backend/database/init_db.py
```

**2. Start Sensors (WSL2):**
```bash
# Start Zeek
sudo zeekctl deploy

# Start Suricata
sudo systemctl start suricata

# Start Vector
vector --config vector.toml
```

**3. Start Backend (Windows):**
```powershell
cd F:\program-ppt\backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**4. Start Frontend (Windows):**
```powershell
cd F:\program-ppt\frontend
npm start
```

### 8.4 Health Checks

**Endpoint: GET /api/health**

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-29T14:35:00Z",
  "services": {
    "postgres": "connected",
    "redis": "connected",
    "ai_chat": "openai api connected",
    "websocket": "active (3 clients)"
  },
  "sensors": {
    "zeek": {
      "status": "running",
      "last_log": "2026-01-29T14:34:55Z"
    },
    "suricata": {
      "status": "running",
      "last_alert": "2026-01-29T14:34:30Z"
    },
    "wazuh": {
      "status": "connected",
      "agent_count": 1
    }
  }
}
```

---

## 📚 Layer 9: Documentation Requirements

### 9.1 API Documentation

**Auto-generated with FastAPI:**

- Access: http://localhost:8000/docs
- Format: OpenAPI 3.0 (Swagger UI)
- Includes: All endpoints, request/response schemas, example payloads

### 9.2 Setup Guide

**README.md:**
- Prerequisites (Windows 11, WSL2, Python 3.11)
- Step-by-step installation
- Configuration instructions
- Troubleshooting common issues

### 9.3 Operational Runbook

**Incident Response Playbook:**
- How to investigate alerts
- When to block IPs
- Escalation procedures
- Log retention policies

---

## 🎯 Success Criteria

### Functional Requirements

- [ ] Zeek, Suricata, Wazuh sensors installed and logging
- [ ] Vector forwarding logs to FastAPI ingest endpoint
- [ ] Heuristic detection classifying threats correctly (DDoS, Port Scan, etc.)
- [ ] Incident threading grouping related alerts
- [ ] PostgreSQL storing incidents persistently
- [ ] Redis caching live window (last 15 min)
- [ ] WebSocket broadcasting alerts in <500ms
- [ ] Dashboard API returning filtered alerts
- [ ] Incident details API providing full context with threshold-based evidence
- [ ] AI chat refusing offensive requests
- [ ] AI chat providing plain-language explanations via OpenAI API
- [ ] All 3 UI pages functional and connected

### Non-Functional Requirements

- [ ] System handles 100 alerts/second
- [ ] Heuristic detection latency <50ms
- [ ] API response time <600ms (p95)
- [ ] Zero data loss during normal operation
- [ ] Graceful degradation if sensors offline
- [ ] AI API failures handled gracefully with error messages
- [ ] Logs rotated to prevent disk fill
- [ ] Database indexes optimize queries

---

## 🔄 Future Enhancements (Out of MVP Scope)

1. **ML Detection Layer:** Add XGBoost + SHAP for advanced explainability (if needed)
2. **Distributed Deployment:** Kubernetes for scaling
3. **Threat Intel Feeds:** Integrate VirusTotal, AbuseIPDB for IP reputation
4. **Automated Response:** Auto-block IPs via firewall API
5. **Multi-Tenant:** Support multiple networks/organizations
6. **Historical Analysis:** Long-term trend analysis with anomaly detection
7. **Custom Dashboards:** Grafana integration
8. **Mobile App:** Push notifications for critical alerts
9. **Fine-Tuned AI:** Train custom model on security documentation for better explanations

---

**Document Version:** 1.0  
**Last Updated:** January 29, 2026  
**Author:** XAI-IDS Development Team  
**Target Platform:** Windows 11 Pro + WSL2 Ubuntu 22.04

