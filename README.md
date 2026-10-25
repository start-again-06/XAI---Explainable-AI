# XAI-IDS: Explainable AI Intrusion Detection System

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Real-time network threat detection with rule-based classification and AI-powered explanations.**

A MVP demonstrating "glass box" AI security - combining proven signature-based detection (Suricata + Zeek) with real-time AI explanations via OpenAI API.

---

## Project Overview

### Key Features
- **5-Sensor Architecture** - Zeek, Suricata, Wazuh, osquery, Vector
- **Rule-based Detection** - 25+ Suricata signatures + Zeek behavioral thresholds (95%+ accuracy)
- **Real-time Dashboard** - Live threat feed with WebSocket updates
- **AI Explanations** - Dynamic incident analysis via OpenAI API
- **3-Page UI** - Dashboard → Incident Details → AI Chat
- **End-to-End Testing** - Complete test suite for full data pipeline

### Attack Detection Coverage
- **DDoS/Flooding** - High packet rate detection
- **Port Scanning** - Horizontal and vertical scan detection
- **Brute Force** - SSH, FTP, RDP, HTTP auth attacks
- **SQL Injection** - Web attack signatures
- **Malware/C2** - Command & control detection
- **Data Exfiltration** - Large outbound transfers

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WINDOWS HOST                              │
├─────────────────────────────────────────────────────────────┤
│  Frontend: React + Vite (Port 5173)                          │
│  ├── Live Feed Dashboard                                     │
│  ├── Incident Attribution Details                            │
│  └── AI Security Assistant Chat                              │
├─────────────────────────────────────────────────────────────┤
│  Backend: FastAPI (Port 8000)                                │
│  ├── PostgreSQL - Persistent storage                         │
│  ├── Redis - Real-time event buffer                          │
│  ├── WebSocket - Socket.IO real-time alerts                  │
│  └── OpenAI API - AI explanations                            │
├─────────────────────────────────────────────────────────────┤
│  Windows Sensors:                                            │
│  ├── Wazuh Agent - Endpoint monitoring                       │
│  └── osquery - SQL-based endpoint queries                    │
└─────────────────────────────────────────────────────────────┘
                              │
                    HTTP API / WebSocket
                              │
┌─────────────────────────────────────────────────────────────┐
│                   WSL2 UBUNTU                                │
├─────────────────────────────────────────────────────────────┤
│  Network Sensors:                                            │
│  ├── Zeek - Behavioral analysis (conn.log, http.log)         │
│  ├── Suricata - Signature-based IDS (25+ custom rules)       │
│  └── Vector - Log shipper to backend                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
XAI-IDS/
├── backend/                      # FastAPI Backend
│   ├── main.py                   # Application entry point
│   ├── config.py                 # Environment settings
│   ├── requirements.txt          # Python dependencies
│   ├── routes/                   # API Endpoints
│   │   ├── ingest.py            # POST /api/ingest (sensor logs)
│   │   ├── dashboard.py         # GET /api/dashboard/alerts
│   │   ├── incidents.py         # GET /api/incidents/{id}
│   │   ├── chat.py              # POST /api/chat (AI assistant)
│   │   └── actions.py           # POST /api/actions/* (block, resolve)
│   ├── services/                # Business Logic
│   │   ├── heuristic_detection.py   # Rule-based classification
│   │   ├── feature_extraction.py    # Zeek/Suricata parsing
│   │   ├── ai_chat.py              # OpenAI integration
│   │   ├── correlation.py          # Alert correlation engine
│   │   └── geolocation.py          # IP geolocation
│   ├── database/                # Data Layer
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── postgres.py          # PostgreSQL connection
│   │   ├── redis.py             # Redis client
│   │   └── schema.sql           # Database DDL
│   ├── websocket/               # Real-time Updates
│   │   └── server.py            # Socket.IO server
│   └── scripts/                 # Utility Scripts
│       └── seed_demo_data.py    # Demo data generator
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── pages/               # Main UI Pages
│   │   │   ├── LiveFeedDashboard.jsx
│   │   │   ├── IncidentDetails.jsx
│   │   │   └── AIChat.jsx
│   │   ├── services/            # API Clients
│   │   │   ├── api.js          # REST API calls
│   │   │   └── websocket.js    # WebSocket client
│   │   ├── hooks/               # React Hooks
│   │   │   └── useWebSocket.js
│   │   └── components/          # Reusable Components
│   │       └── Layout.jsx
│   └── package.json
│
├── sensors/                      # Sensor Configurations
│   ├── zeek/                    # Zeek configs
│   │   ├── local.zeek          # Main Zeek script
│   │   ├── node.cfg            # Interface config
│   │   └── zeek_control.sh     # Control script
│   ├── suricata/                # Suricata configs
│   │   ├── suricata.yaml       # Main config
│   │   ├── custom.rules        # 25 custom rules
│   │   └── suricata_control.sh # Control script
│   ├── wazuh/                   # Wazuh configs
│   │   ├── ossec.conf          # Agent config
│   │   └── local_rules.xml     # 13 custom rules
│   ├── osquery/                 # osquery configs
│   │   ├── osquery.conf        # Main config
│   │   └── packs/              # Query packs
│   ├── vector/                  # Vector configs
│   │   ├── vector.toml         # Pipeline config
│   │   └── setup.sh            # Setup script
│   ├── manage_sensors.sh       # Unified sensor manager
│   ├── install.sh              # Installation script
│   └── test_traffic.sh         # Test traffic generator
│
└── tests/                        # Testing
    └── test_e2e.py              # End-to-end tests
```

---

## Quick Start

### Prerequisites
- **Windows 11** with WSL2 Ubuntu
- **Python 3.11+**
- **PostgreSQL 15**
- **Redis** (or Memurai for Windows)
- **Node.js 18+**
- **OpenAI API Key** - [Get from OpenAI](https://platform.openai.com/api-keys)

## Sensor Configuration

### Zeek (Network Analysis)
- **Location**: WSL2
- **Logs**: `/opt/zeek/logs/current/`
- **Features**: Connection tracking, HTTP analysis, DNS monitoring
- **Control**: `sensors/zeek/zeek_control.sh`

### Suricata (Signature IDS)
- **Location**: WSL2
- **Rules**: 25 custom rules + Emerging Threats Open
- **Alerts**: `/var/log/suricata/eve.json`
- **Control**: `sensors/suricata/suricata_control.sh`

### Wazuh (Endpoint Monitoring)
- **Location**: Windows
- **Path**: `C:\Program Files (x86)\ossec-agent\`
- **Rules**: 13 custom endpoint detection rules
- **Features**: Process monitoring, authentication tracking

### osquery (SQL Queries)
- **Location**: Windows
- **Config**: `C:\ProgramData\osquery\`
- **Queries**: 22 scheduled queries
- **Features**: Process, port, and connection monitoring

### Vector (Log Shipping)
- **Location**: WSL2
- **Sources**: Zeek, Suricata logs
- **Destination**: `http://WINDOWS_IP:8000/api/ingest`
- **Setup**: `sensors/vector/setup.sh`

---

## Testing

### End-to-End Tests

```powershell
# Run all E2E tests
python tests/test_e2e.py

# Run specific scenario
python tests/test_e2e.py --scenario ddos

# Run with verbose output
python tests/test_e2e.py --verbose
```

### Sensor Health Check

```bash
# In WSL2
./sensors/check_health.sh

# Or use the unified manager
./sensors/manage_sensors.sh health
```

### Generate Test Traffic

```bash
# In WSL2
./sensors/test_traffic.sh all

# Or interactive mode
./sensors/test_traffic.sh menu
```

### Demo Data

```powershell
# Seed database with demo incidents
python backend/scripts/seed_demo_data.py --count 15

# Clear and re-seed
python backend/scripts/seed_demo_data.py --clear --count 20
```

---

## API Reference

### Dashboard APIs
- `GET /api/dashboard/alerts` - List incidents with filters
- `GET /api/dashboard/statistics` - Dashboard statistics

### Incident APIs
- `GET /api/incidents/{id}` - Get incident details
- `PATCH /api/incidents/{id}/status` - Update incident status

### Ingest API
- `POST /api/ingest` - Receive sensor logs

### Actions APIs
- `POST /api/actions/block_ip` - Block attacker IP
- `POST /api/actions/resolve_incident` - Mark as resolved
- `POST /api/actions/add_note` - Add analyst note

### Chat API
- `POST /api/chat` - AI assistant chat
- `GET /api/chat/initial/{id}` - Get initial explanation

### WebSocket
- `ws://localhost:8000/socket.io/` - Real-time alerts

---

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Check Redis is running: `redis-cli ping`
- Verify `.env` file exists with `OPENAI_API_KEY`

### Sensors not sending data
- Run health check: `./sensors/check_health.sh`
- Test Vector config: `vector validate /opt/xai-ids/vector/vector.toml`
- Check Windows firewall allows port 8000

### Frontend not loading
- Ensure backend is running on port 8000
- Check `VITE_API_URL` in frontend `.env`
- Clear browser cache

### No alerts appearing
- Generate test traffic: `./sensors/test_traffic.sh all`
- Check backend logs for errors
- Verify database connection

---

## Documentation

- **Implementation Plan**: `XAI_IDS_Implementation_Plan.md`
- **Backend Spec**: `XAI_IDS_Backend_Specification.md`
- **UI Spec**: `XAI_IDS_UI_Specification.md`
- **Sensor Setup**: `sensors/SENSORS_SETUP.md`

---

## Contributing

This is a MVP project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- Suricata - [https://suricata.io](https://suricata.io)
- Zeek - [https://zeek.org](https://zeek.org)
- Wazuh - [https://wazuh.com](https://wazuh.com)
- osquery - [https://osquery.io](https://osquery.io)
- Vector - [https://vector.dev](https://vector.dev)

---

**Last Updated: October 2026**
