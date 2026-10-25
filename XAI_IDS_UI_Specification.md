# XAI-IDS User Interface Specification Document

## Project: Real-Time Explainable AI Intrusion Detection System
**Version:** 1.0  
**Date:** January 29, 2026  
**Document Type:** UI/UX Requirements & Flow Specification

---

## 📋 Executive Summary

This document defines the complete user interface structure for the XAI-IDS web application. The system follows a **3-Page Architecture** designed to guide users from situational awareness to deep investigation to AI-powered understanding.

### Design Philosophy
- **"Glass Box" Transparency:** Every screen reveals information, never hides it
- **Progressive Disclosure:** Information unfolds naturally as the user digs deeper
- **Beginner-Friendly:** Designed for students and junior analysts
- **Cognitive Load Reduction:** Prevent alert fatigue through smart grouping

---

## 🏗️ Page Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    XAI-IDS WEB APPLICATION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│   │              │      │              │      │              │  │
│   │   PAGE 1     │ ───► │   PAGE 2     │ ───► │   PAGE 3     │  │
│   │              │      │              │      │              │  │
│   │  LIVE FEED   │      │ ATTRIBUTION  │      │   AI CHAT    │  │
│   │  DASHBOARD   │      │    DETAILS   │      │  EXPLANATION │  │
│   │              │      │              │      │              │  │
│   └──────────────┘      └──────────────┘      └──────────────┘  │
│                                                                  │
│   Click Attack Row      Click AI Button       Interactive Q&A   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📄 PAGE 1: Live Feed Dashboard

### Purpose
The **"Analyst's Cockpit"** - Primary situational awareness screen showing all incoming threats in real-time.

### Page Title
**"Security Operations Dashboard"** or **"Live Threat Feed"**

---

### Header Section

| Element | Description |
|---------|-------------|
| **Logo/Brand** | XAI-IDS logo on the left |
| **Page Title** | "Live Threat Feed" prominently displayed |
| **Connection Status** | Green dot with "Connected" or Red dot with "Disconnected" |
| **Last Updated** | Timestamp showing real-time sync (e.g., "Updated: 14:32:05 UTC") |
| **Refresh Indicator** | Subtle animation showing WebSocket is active |

---

### Filter Bar

| Filter | Options | Default |
|--------|---------|---------|
| **Time Range** | Last 5 min / 15 min / 1 hour / 24 hours / Custom | Last 15 min |
| **Severity** | All / Critical / High / Medium / Low | All |
| **Attack Type** | All / DDoS / Brute Force / SQL Injection / Port Scan / Other | All |
| **Status** | All / Active / Investigating / Resolved | All |

---

### Main Content: Live Attack Table

#### Table Columns

| Column | Description | Width | Sortable |
|--------|-------------|-------|----------|
| **Severity Icon** | Color-coded badge (🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low) | 60px | Yes |
| **Timestamp** | When the attack was detected (e.g., "14:32:05") | 100px | Yes |
| **Attack Type** | Category label (DDoS, Brute Force, etc.) | 120px | Yes |
| **Source IP** | Attacker's IP address with country flag | 150px | Yes |
| **Target** | What was attacked (e.g., "Web Server :443") | 150px | Yes |
| **Confidence** | Detection confidence (rule-based: 95%) | 80px | Yes |
| **Quick Reason** | Short "why" hint (e.g., "Abnormal packet rate") | Flex | No |
| **Action** | "View Details →" button | 120px | No |

#### Row Behavior

- **Hover State:** Row highlights with subtle background color change
- **Click Action:** Entire row is clickable → Opens **PAGE 2: Attribution Details**
- **New Alert Animation:** New rows slide in from top with brief glow effect
- **Critical Alert Pulse:** Critical severity rows have subtle pulsing border

---

### Real-Time Statistics Bar (Bottom or Sidebar)

| Metric | Display |
|--------|---------|
| **Total Alerts (24h)** | Number with trend arrow (↑ or ↓) |
| **Critical Active** | Red badge with count |
| **Avg Response Time** | Time in seconds |
| **System Health** | Green/Yellow/Red indicator |

---

### Empty State
When no attacks detected:
- Large shield icon with checkmark
- Message: "All Clear - No threats detected in the selected time range"
- Subtext: "The system is actively monitoring your network"

---

## 📄 PAGE 2: Attribution Details (Incident Investigation)

### Purpose
Deep dive into a specific incident showing **WHO attacked, WHAT was targeted, WHEN it happened, and HOW it was detected**.

### Navigation
- **Back Button:** "← Back to Live Feed" (returns to Page 1)
- **Breadcrumb:** Live Feed > Incident #INC-2026-0142

---

### Incident Header Card

| Element | Description |
|---------|-------------|
| **Incident ID** | Unique identifier (e.g., "INC-2026-0142") |
| **Severity Badge** | Large colored badge with text (e.g., "🔴 CRITICAL") |
| **Attack Type** | Large label (e.g., "DDoS - UDP Flood") |
| **Status Dropdown** | Active / Investigating / Contained / Resolved |
| **Timestamp Range** | "Started: 14:32:00 UTC — Last Activity: 14:32:15 UTC" |
| **Duration** | "Duration: 15 seconds" |

---

### Section 1: Attack Attribution (WHO)

#### Attacker Information Card

| Field | Value Example |
|-------|---------------|
| **Source IP** | 192.168.1.45 |
| **Geolocation** | Moscow, Russia 🇷🇺 (with small map thumbnail) |
| **ISP/Organization** | "Unknown / Residential" |
| **Reputation Score** | "Known Malicious (5 previous incidents)" or "First Seen" |
| **Related IPs** | List of other IPs in same campaign (if any) |

---

### Section 2: Target Information (WHAT)

#### Target Details Card

| Field | Value Example |
|-------|---------------|
| **Destination IP** | 10.0.0.5 (Your Web Server) |
| **Targeted Port** | 443 (HTTPS) |
| **Service Mapped** | "nginx web server process" |
| **Process ID** | PID: 1842 |
| **Application Context** | "Traffic hit the main production web server" |

---

### Section 3: Timeline (WHEN)

#### Visual Timeline Component

```
14:32:00 ──●── First packet received
           │
14:32:02 ──●── Packet rate exceeded threshold (18,500/sec)
           │
14:32:03 ──●── Suricata Alert: "Volumetric DDoS Detected"
           │
14:32:05 ──●── XAI-IDS Detection: HIGH RISK (95% confidence - rule-based)
           │
14:32:10 ──●── Incident Thread Created
           │
14:32:15 ──●── [Current] Awaiting analyst action
```

- Timeline is interactive - clicking each node shows expanded details
- Color-coded by event type (detection, alert, action)

---

### Section 4: Detection Evidence (HOW)

#### Evidence Cards Grid

**Card 1: Behavioral Analysis (Zeek)**
| Metric | Value | Threshold | Impact |
|--------|-------|-----------|--------|
| Packet Rate | 18,500/sec | 10,000/sec | 🔴 High (85% over) |
| Connection Duration | 180 seconds | 300 seconds | 🟢 Normal |
| Bytes Transferred | 2.4 GB | 1 GB | 🔴 High (140% over) |
| Port Diversity | 1 port | 50 ports | 🟢 Normal |

**Card 2: Signature Match (Suricata)**
| Field | Value |
|-------|-------|
| Alert ID | SID: 2024-50402 |
| Rule Name | "ET DOS UDP Flood Inbound" |
| Classification | "Attempted Denial of Service" |
| Reference | MITRE ATT&CK: T1498.001 |

**Card 3: Endpoint Context (Wazuh/osquery)**
| Field | Value |
|-------|-------|
| Process | nginx (PID 1842) |
| User | www-data |
| CPU Spike | Yes (85% → 98%) |
| Memory Impact | Moderate |

---

### Section 5: Detection Evidence Visualization

#### Threshold-Based Evidence Chart

Visual comparison showing metrics vs. thresholds:

**Packet Rate:**
```
Threshold: 10,000/sec
Actual:    ████████████████████████████████████████ 18,500/sec
Status:    🔴 HIGH (185% over threshold)
```

**Flow Duration:**
```
Threshold: 300 seconds
Actual:    ████████████████ 180 seconds
Status:    🟡 NORMAL (within threshold)
```

**Bytes Transferred:**
```
Threshold: 1 GB
Actual:    ████████████████████████████████████████ 2.4 GB
Status:    🔴 HIGH (1.4 GB over threshold)
```

Caption: "These metrics exceeded detection thresholds, triggering the alert"

#### Alternative: Simple Impact Table

| Metric | Value | Threshold | Impact |
|--------|-------|-----------|--------|
| **Packet Rate** | 18,500/sec | 10,000/sec | 🔴 High (185% over) |
| **Flow Duration** | 180 sec | 300 sec | 🟢 Normal |
| **Bytes Transferred** | 2.4 GB | 1 GB | 🔴 High (140% over) |
| **Port Diversity** | 1 port | 50 ports | 🟢 Normal |

---

### 🔘 AI Explanation Button (PRIMARY CTA)

**Location:** Fixed at bottom of page OR prominent position in header

**Button Design:**
- Large, visually distinct button
- Icon: 🤖 or 💬 or ✨
- Text: **"Get AI Explanation"** or **"Ask AI Assistant"**
- Subtext: "Get plain-language analysis and recommended actions"

**Button States:**
- Default: Blue/Purple gradient with white text
- Hover: Slightly enlarged with glow effect
- Loading: Spinner with "Connecting to AI..."
- Disabled: Greyed out if incident data incomplete

**Click Action:** Opens **PAGE 3: AI Chat Explanation**

---

### Quick Actions Sidebar

| Action | Description |
|--------|-------------|
| **Block IP** | Quick action to add IP to firewall blocklist |
| **Export Report** | Download incident as PDF |
| **Mark Resolved** | Change status and close incident |
| **Add Note** | Analyst can add investigation notes |

---

## 📄 PAGE 3: AI Chat Explanation

### Purpose
Interactive AI assistant that translates technical incident data into **plain language explanations** and provides **defensive guidance**.

### Navigation
- **Back Button:** "← Back to Incident Details" (returns to Page 2)
- **Breadcrumb:** Live Feed > Incident #INC-2026-0142 > AI Explanation

---

### Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Incident Details          Incident: INC-2026-0142   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │              INCIDENT CONTEXT SUMMARY                    │    │
│  │                    (Collapsed Card)                      │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │                                                          │    │
│  │                    CHAT MESSAGE AREA                     │    │
│  │                                                          │    │
│  │                  (Scrollable History)                    │    │
│  │                                                          │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Type your question...                        [Send →]  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Suggested Questions:                                    │    │
│  │  [Explain this attack] [What should I do?] [Is it over?]│    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### Incident Context Summary (Collapsible)

Always visible at top - provides AI with context:

| Field | Value |
|-------|-------|
| **Incident** | INC-2026-0142 |
| **Type** | DDoS - UDP Flood |
| **Severity** | Critical |
| **Source** | 192.168.1.45 (Moscow, RU) |
| **Target** | Web Server :443 |
| **Confidence** | 98% |

Toggle: "Show/Hide Full Context"

---

### Chat Message Area

#### Initial AI Message (Auto-generated on page load)

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AI Security Assistant                          14:32:20  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Hello! I've analyzed Incident INC-2026-0142. Here's what    │
│ happened in plain terms:                                     │
│                                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                              │
│ 📋 SUMMARY                                                   │
│ Your web server received a flood of malicious traffic from  │
│ an IP address in Moscow, Russia. This is called a "DDoS     │
│ attack" - the attacker tried to overwhelm your server with  │
│ so many requests that legitimate users couldn't connect.     │
│                                                              │
│ 🔍 WHY IT WAS FLAGGED                                        │
│ • Packet rate was 18,500/second (normal is ~500/second)     │
│ • Attack lasted 180 seconds (3 minutes)                      │
│ • Pattern matches known "UDP Flood" signature                │
│                                                              │
│ 📊 EVIDENCE                                                  │
│ • Zeek detected abnormal connection patterns                 │
│ • Suricata matched rule: "ET DOS UDP Flood Inbound"         │
│ • Your nginx web server CPU spiked to 98%                   │
│                                                              │
│ ✅ RECOMMENDED ACTIONS                                       │
│ 1. Block the source IP (192.168.1.45) in your firewall      │
│ 2. Check if your web server is responding normally          │
│ 3. Review firewall logs for any dropped packets             │
│ 4. Consider enabling rate limiting for future protection    │
│                                                              │
│ 🛡️ CONFIDENCE: High (95%)                                   │
│ This classification is supported by Suricata signature       │
│ matching AND Zeek behavioral threshold analysis.             │
│                                                              │
│ Do you have any questions about this incident?               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

#### User Message Bubble

```
┌─────────────────────────────────────────────────────────────┐
│                                         You       14:32:45  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Is this attacker likely to try again?                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

#### AI Response Bubble

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AI Security Assistant                          14:32:47  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Based on the attack pattern, here's my assessment:          │
│                                                              │
│ 🔄 LIKELIHOOD OF REPEAT: Moderate to High                   │
│                                                              │
│ Why:                                                         │
│ • The attacker used automated tools (high packet rate)      │
│ • Attack stopped suddenly (may be probing defenses)         │
│ • This IP has 5 previous incidents in threat databases      │
│                                                              │
│ 🛡️ PREVENTIVE MEASURES                                      │
│ • Keep the IP blocked for at least 24-48 hours              │
│ • Monitor for attacks from similar IP ranges                │
│ • Consider a DDoS mitigation service for future protection  │
│                                                              │
│ Would you like me to explain any of these steps in detail?  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Chat Input Area

| Element | Description |
|---------|-------------|
| **Text Input** | Large text field with placeholder "Ask about this incident..." |
| **Send Button** | Arrow icon or "Send" text |
| **Voice Input** | (Optional) Microphone icon for voice questions |
| **Character Limit** | Display remaining characters (e.g., "450/500") |

**Input Behavior:**
- Enter key sends message
- Shift+Enter for new line
- Auto-resize as user types

---

### Suggested Questions (Quick Actions)

Pre-built question buttons below the input:

| Button | Query Sent |
|--------|------------|
| **"Explain this attack"** | "Explain this attack in simple terms" |
| **"What should I do?"** | "What are the recommended defensive actions?" |
| **"Is it still happening?"** | "Is this attack still active or has it stopped?" |
| **"How was it detected?"** | "Explain how the system detected this attack" |
| **"Is my data safe?"** | "Was any data compromised during this attack?" |
| **"Teach me"** | "Explain what a DDoS attack is for a beginner" |

---

### AI Response Template Structure

Every AI response follows this pattern:

```
📋 SUMMARY
[1-2 sentence plain language explanation]

🔍 WHY / REASON
[Bullet points explaining the logic]

📊 EVIDENCE
[Specific data points from logs/sensors]

✅ RECOMMENDED ACTIONS / NEXT STEPS
[Numbered list of defensive actions]

🛡️ CONFIDENCE LEVEL
[High/Medium/Low with brief justification]
```

---

### Ethical Constraints (Built into AI)

The AI assistant MUST:
- ✅ Explain attacks in defensive terms only
- ✅ Recommend protective actions
- ✅ Cite evidence from the system
- ✅ Admit uncertainty when confidence is low

The AI assistant MUST NOT:
- ❌ Provide instructions to perform attacks
- ❌ Explain exploitation techniques
- ❌ Share offensive tools or methods
- ❌ Help the user attack other systems

**Refusal Response Example:**
```
🚫 I can't help with that request. 

My purpose is to help you DEFEND your systems, not attack others.
If you're interested in learning about offensive security ethically,
I recommend looking into certified penetration testing courses.

Is there anything else about defending against this incident I can help with?
```

---

### Chat History Features

| Feature | Description |
|---------|-------------|
| **Scroll to Top** | Button to jump to initial explanation |
| **Copy Response** | Copy any AI response to clipboard |
| **Export Chat** | Download entire conversation as PDF/TXT |
| **Clear Chat** | Reset conversation (keeps context) |
| **Regenerate** | Re-generate last AI response |

---

## 🎨 Visual Design Guidelines

### Color Scheme

| Element | Color | Usage |
|---------|-------|-------|
| **Critical** | #DC2626 (Red) | Critical severity badges, urgent alerts |
| **High** | #F97316 (Orange) | High severity, warnings |
| **Medium** | #EAB308 (Yellow) | Medium severity, caution |
| **Low** | #22C55E (Green) | Low severity, informational |
| **Primary Action** | #6366F1 (Indigo) | Buttons, links, AI elements |
| **Background** | #0F172A (Dark Navy) | Main background (dark mode) |
| **Card Background** | #1E293B (Slate) | Cards, panels |
| **Text Primary** | #F8FAFC (White) | Main text |
| **Text Secondary** | #94A3B8 (Gray) | Subtext, hints |

### Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| **Page Title** | Inter / System | 28px | Bold |
| **Section Header** | Inter / System | 20px | Semibold |
| **Card Title** | Inter / System | 16px | Semibold |
| **Body Text** | Inter / System | 14px | Regular |
| **Small Text** | Inter / System | 12px | Regular |
| **Monospace (IPs, codes)** | JetBrains Mono | 13px | Regular |

### Spacing

| Element | Spacing |
|---------|---------|
| **Page Padding** | 24px |
| **Card Padding** | 16px |
| **Section Gap** | 24px |
| **Element Gap** | 12px |
| **Button Padding** | 12px 24px |

---

## 📱 Responsive Behavior

### Desktop (1200px+)
- Full 3-column layout where applicable
- Side-by-side cards
- Full navigation visible

### Tablet (768px - 1199px)
- 2-column layout
- Stacked cards where needed
- Collapsible sidebar

### Mobile (< 768px)
- Single column layout
- Full-width cards
- Bottom navigation
- Chat takes full screen

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Esc` | Go back to previous page |
| `R` | Refresh live feed |
| `/` | Focus search/filter |
| `Enter` | Open selected incident |
| `A` | Open AI Chat (from Page 2) |
| `?` | Show keyboard shortcuts |

---

## 🔔 Notification System

### Toast Notifications

| Type | Trigger | Duration |
|------|---------|----------|
| **New Alert** | New critical/high attack | 5 seconds + sound |
| **Status Change** | Incident status updated | 3 seconds |
| **AI Ready** | AI response generated | 2 seconds |
| **Error** | Connection lost, API fail | Until dismissed |

### Sound Alerts (Optional)

- Critical Alert: Distinct alarm tone
- New Incident: Soft notification sound
- AI Response: Subtle chime

---

## 📊 Performance Requirements

| Metric | Target |
|--------|--------|
| **Page Load Time** | < 2 seconds |
| **Live Feed Update** | < 500ms latency |
| **AI Response Time** | < 3 seconds |
| **Smooth Scrolling** | 60 FPS |
| **Animation Duration** | 200-300ms |

---

## ✅ Accessibility Requirements

- WCAG 2.1 AA compliance
- Keyboard navigation for all interactions
- Screen reader compatible
- Color contrast ratio 4.5:1 minimum
- Focus indicators visible
- Alt text for all icons/images
- Reduced motion option

---

## 📋 Summary: User Journey

```
1. USER LANDS ON LIVE FEED DASHBOARD
   ↓
   Sees real-time attack list
   ↓
2. USER CLICKS ON AN ATTACK ROW
   ↓
   PAGE 2: ATTRIBUTION DETAILS OPENS
   ↓
   Reviews WHO, WHAT, WHEN, HOW
   ↓
3. USER CLICKS "GET AI EXPLANATION" BUTTON
   ↓
   PAGE 3: AI CHAT OPENS
   ↓
   Receives plain-language explanation
   ↓
   Asks follow-up questions
   ↓
   Gets defensive recommendations
   ↓
4. USER TAKES ACTION
   ↓
   Blocks IP, resolves incident, exports report
```

---

**Document Version:** 1.0  
**Last Updated:** January 29, 2026  
**Author:** XAI-IDS Development Team

