# XAI-IDS Critical Tasks - Execution Plan
**Created:** January 30, 2026  
**Source:** TODO_PRIORITY_LIST.md + COMPLETION_ANALYSIS.md  
**Goal:** Fix all CRITICAL blockers for MVP

---

## 🚨 CRITICAL BLOCKERS (Must Fix)

### Task 1: Actions Router Import Error ✅
**Priority:** 🔴 HIGHEST  
**File:** `backend/routes/actions.py`  
**Status:** COMPLETED  
**Time:** 5 minutes  
**Fix:** Add `from typing import Optional`

---

### Task 2: WebSocket Event Name Mismatch ✅
**Priority:** 🔴 CRITICAL  
**Files:** 
- `backend/websocket/server.py` (emits: new_alert, incident_update)
- `frontend/src/services/websocket.js` (listens for new_alert, incident_update)
- `frontend/src/hooks/useWebSocket.js` (updated event names)
**Status:** COMPLETED  
**Time:** 30 minutes  
**Fix:** Aligned all event names between backend and frontend

---

### Task 3: Dashboard API Contract Mismatch ✅
**Priority:** 🟠 HIGH  
**Files:** 
- `backend/routes/dashboard.py`
- `frontend/src/pages/LiveFeedDashboard.jsx`  
**Status:** COMPLETED  
**Time:** 1 hour  
**Fix:** 
- Changed severity to numeric (1-4) 
- Renamed source_country to country_code
- Added severity_label for display

---

### Task 4: Incident Details API Contract Mismatch ✅
**Priority:** 🟠 HIGH  
**Files:** 
- `backend/routes/incidents.py`
- `frontend/src/pages/IncidentDetails.jsx`  
**Status:** COMPLETED  
**Time:** 2 hours  
**Fix:** 
- Flattened nested objects (attacker → source_ip/country, target → dest_ip/port/process)
- Fixed timeline structure (time/type/event)
- Added missing fields (confidence, detection_node)

---

### Task 5: Resolve-Incident Request Shape Mismatch ⏳
**Priority:** 🟠 HIGH  
**Files:** 
- `backend/routes/actions.py`
- `frontend/src/services/api.js`  
**Status:** PENDING  
**Time:** 30-60 minutes  
**Issue:** Frontend sends JSON, backend expects query params

---

### Task 6: Suricata Signature Extraction Bug ⏳
**Priority:** 🟠 HIGH  
**Files:** 
- `backend/routes/ingest.py`
- `backend/services/feature_extraction.py`  
**Status:** PENDING  
**Time:** 1 hour  
**Issue:** Evidence lacks signature name/SID

---

### Task 7: Wazuh Ingest + Endpoint Context Missing ⏳
**Priority:** 🟠 HIGH  
**Files:** 
- `backend/routes/ingest.py`
- `backend/database/models.py`
- `backend/routes/incidents.py`  
**Status:** PENDING  
**Time:** 2-3 hours  
**Issue:** Target process context empty

---

## 🟢 OPTIONAL TASKS (Post-MVP)

### Task 8: Dashboard Stats Endpoint
**Priority:** 🟢 LOW  
**Status:** PENDING

### Task 9: Demo Data Seeding Script
**Priority:** 🟢 MEDIUM  
**Status:** PENDING

### Task 10: End-to-End Testing
**Priority:** 🟢 MEDIUM  
**Status:** PENDING

### Task 11: Documentation Completion
**Priority:** 🟢 MEDIUM  
**Status:** PENDING

## 🟡 ANALYSIS TASKS (New Request)

### Task 12: Explainability artifacts & chat context
**Priority:** 🟡 MEDIUM  
**Status:** PENDING  
**Goal:** Design backend changes that capture feature-contribution artifacts per alert/incident, persist chat context for AI responses, and lower ingestion/WebSocket latency.  
**Notes:** Align schema and APIs to hydrate frontend with structured contributions, plus propose tests validating storage and retrieval of artifacts/conversations.

---

## 📊 Progress Tracker

| Task | Status | Time Spent | Priority |
|------|--------|------------|----------|
| 1. Actions Import Error | ✅ DONE | 5 min | 🔴 Highest |
| 2. WebSocket Events | ✅ DONE | 30 min | 🔴 Critical |
| 3. Dashboard API | ✅ DONE | 1 hr | 🟠 High |
| 4. Incident Details API | ✅ DONE | 2 hrs | 🟠 High |
| 5. Resolve Incident | ⏳ PENDING | - | 🟠 High |
| 6. Suricata Signature | ⏳ PENDING | - | 🟠 High |
| 7. Wazuh Ingest | ⏳ PENDING | - | 🟠 High |
| 8. Stats Endpoint | ⏳ PENDING | - | 🟢 Low |
| 9. Demo Data | ⏳ PENDING | - | 🟢 Medium |
| 10. E2E Testing | ⏳ PENDING | - | 🟢 Medium |
| 11. Documentation | ⏳ PENDING | - | 🟢 Medium |

**Progress: 4/11 tasks complete (36%)**
**Critical tasks remaining: 3/7 (Tasks 5-7)**

---

## 📝 Summary of Changes Made

### Backend Changes:
1. **actions.py**: Added `from typing import Optional` import
2. **dashboard.py**: 
   - Changed AlertSummary severity to numeric (int)
   - Added country_code field
   - Added severity_label field
3. **incidents.py**:
   - Flattened all nested objects (attacker, target, process)
   - Fixed timeline structure with time/type/event fields
   - Added confidence and detection_node fields

### Frontend Changes:
1. **websocket.js**: Updated event names to match backend (new_alert, incident_update)
2. **useWebSocket.js**: Updated event listeners to use correct event names

---

## 🎯 Next Priority: Task 5

The next critical task is **Task 5: Resolve-Incident Request Shape Mismatch**

This fixes the issue where resolving an incident returns 422 error because the frontend sends JSON body but backend expects query parameters.
