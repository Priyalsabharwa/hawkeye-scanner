# Hawkeye 🦅

> **Scan files and links. Know why.**

[![Project Status](https://img.shields.io/badge/status-active%20development-blue.svg)](#roadmap)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-brightgreen.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

---

## 📌 Overview

**Hawkeye** is a multi-engine security scanning platform designed to inspect URLs and files for malware, phishing attempts, and spoofed services—with a dedicated focus on **fake government portals**.

Instead of returning an opaque score (such as *"Phishing, 95%"*), Hawkeye combines threat intelligence feeds, rule-based URL heuristics, government impersonation detectors, YARA rules, and antivirus engines. It produces a clear, risk-weighted verdict accompanied by transparent, plain-language explanations.

---

## 🎯 Why Hawkeye?

### The Problem: Impersonation & Opaque Scanning
Fraudulent websites impersonating government bodies—such as subsidy schemes, scholarship applications, Aadhaar/PAN record updates, or traffic challan payment gateways—rely on deceptive domain names and copied visual assets to trick users. Victims compromise sensitive personal identification data, bank credentials, and direct monetary payments.

Most standard scanners present two key limitations:
1. They rely on single-engine machine learning classifiers that provide a raw confidence score without actionable justification.
2. They do not account for jurisdictional domain hierarchies (e.g., verifying `.gov.in` vs. lookalike `.com` or `.org` domains).

### How Hawkeye Compares

| Feature | Common Scanners | Hawkeye |
| :--- | :--- | :--- |
| **Target Scope** | URLs only | Both URLs and uploaded files |
| **Decision Logic** | Single ML model | Multi-engine aggregator with rule-based heuristics |
| **Output Type** | Label & probability (e.g., `Phishing: 92%`) | Actionable verdict (`Safe`, `Suspicious`, `Malicious`) with breakdown |
| **Government Impersonation** | Generic phishing detection | Dedicated engine verifying authentic government TLDs & lookalikes |
| **Explainability** | Opaque | Human-readable points explaining exact trigger causes |
| **Alerting** | Passive display | Real-time notifications via In-App UI, Email, and Telegram |
| **Deep Inspection** | Static string checking | Sandbox inspection (DOM checks, iframes, deceptive logos) |

---

## 🚀 Key Features

* **URL Heuristic Engine:** Flags IP-based addresses, excessive subdomains, missing HTTPS, open redirects, `@` credential-abuse syntax, shorteners, punycode lookalikes, and low-reputation domain ages.
* **Government Impersonation Detection:** Cross-references requested URLs against verified public registers (e.g., Indian official digital domains) to catch fake subsidy, fee payment, and identity capture portals.
* **Aggregated Threat Intelligence:** Integrates with VirusTotal, Google Safe Browsing, URLhaus, and PhishTank for active threat signals.
* **File Analysis Pipeline:** Validates true MIME signatures (Python-Magic), computes SHA-256 hashes, scans byte patterns using YARA rules, and checks binaries against ClamAV.
* **Standardized Engine Contract:** Every detection engine yields a deterministic JSON shape containing risk-weight contributions and findings.
* **Multilingual AI Explainability (Planned):** Contextualizes technical findings into easily digestible warnings across regional languages (including Hindi and Hinglish).

---

## ⚙️ Architecture & Data Flow

```text
       User / Browser / Extension
                   │
                   ▼
       API Gateway (FastAPI)       ──► [Rate Limiting, Schema Validation]
                   │
                   ▼
         Scan Orchestrator         ──► [Routes payload to active engines]
                   │
    ┌──────────────┴──────────────────────────┐
    ▼                                         ▼
[URL Engines]                             [File Engines]
  ├─ Threat Feeds (VT, URLhaus)             ├─ SHA-256 Hash Matching
  ├─ Domain Heuristics & Age                ├─ True MIME vs. Fake Extension
  ├─ Gov Impersonation Rules                ├─ YARA Rule Matching
  └─ Live DOM Sandbox (Forms, Iframes)      └─ ClamAV Antivirus
    │                                         │
    └──────────────┬──────────────────────────┘
                   ▼
            Verdict Engine         ──► [Combines risks, caps at 100, assigns verdict]
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
Database Logging     Notification Service
 (SQLite/Postgres)    (Email, Telegram, UI)
```

### Standardized Engine Payload

Every engine implements a common interface:

```json
{
  "engine": "gov_impersonation",
  "risk": 45,
  "findings": [
    "Domain claims to represent a public portal but is hosted on a commercial TLD (.info)",
    "Site uses known keywords matching welfare disbursement forms"
  ]
}
```

### Scoring Matrix

| Aggregate Score | Final Verdict | Recommended Action |
| :---: | :---: | :--- |
| **$0 - 30$** | `Safe` | Low risk; standard operations permitted. |
| **$31 - 70$** | `Suspicious` | Caution advised; anomalous patterns or recent domain creation detected. |
| **$71 - 100$** | `Malicious` | Threat confirmed; instant alert dispatched, domain/file flagged. |

---

## 🛠️ Tech Stack

| Domain | Technology / Library |
| :--- | :--- |
| **Runtime & Language** | Python 3.11+ |
| **Web Framework** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Semantic HTML5, CSS3, Modern JavaScript |
| **Domain & URL Analysis** | `tldextract`, `python-whois`, `requests`, `urllib3` |
| **Threat Intelligence Feeds** | Google Safe Browsing API, VirusTotal API, URLhaus, PhishTank |
| **File Inspection** | `hashlib`, `python-magic`, `yara-python`, ClamAV daemon |
| **Persistence** | SQLite (Default / Local), PostgreSQL (Production ready) |
| **Alerting** | `smtplib` (Email), Telegram Bot API |
| **Testing & Tooling** | `pytest`, `flake8`, `pre-commit` |
| **Containerization** | Docker, Docker Compose |

---

## 📁 Repository Structure

```text
hawkeye/
├── backend/
│   ├── rules/                    # YARA signatures (.yar)
│   └── app/
│       ├── main.py               # FastAPI entrypoint and router bindings
│       ├── config.py             # App settings and environment variables
│       ├── schemas.py            # Pydantic schemas for request/response bodies
│       ├── orchestrator.py       # Engine orchestration and dispatch
│       ├── verdict.py            # Aggregator and score-mapping engine
│       ├── explain.py            # Plain-language explanation engine
│       ├── security.py           # Rate limiting and upload sanitation
│       ├── database.py           # DB session and setup
│       ├── models.py             # ORM database models
│       ├── alerts.py             # Dispatchers for email and Telegram
│       ├── data/                 # Whitelists, known gov domains, TLD sets
│       └── engines/              # Modular detection engines
├── frontend/                     # Web dashboard assets
├── extension/                    # Browser extension source (optional)
├── ml/                           # Experimental heuristic models
├── tests/                        # Pytest suite
├── .env.example                  # Template for required environment variables
├── requirements.txt              # Production and dev dependencies
└── README.md
```

---

## 🚦 Getting Started

### Prerequisites

* Python **3.11** or newer
* Git
* ClamAV (optional, for local file scanning capabilities)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/Priyalsabharwa/hawkeye-scanner.git
cd hawkeye-scanner
```

#### 2. Configure the virtual environment

* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  venv\Scripts\activate
  ```

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Populate your API keys inside `.env`:
```ini
VIRUSTOTAL_API_KEY="your_virustotal_key"
SAFE_BROWSING_API_KEY="your_google_safe_browsing_key"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_target_chat_id"
```

#### 5. Launch the application
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, access:
* **Health Check:** `http://127.0.0.1:8000/health`
* **Interactive API Documentation:** `http://127.0.0.1:8000/docs`

---

## 📡 API Reference

| Method | Endpoint | Status | Description |
| :---: | :--- | :---: | :--- |
| `GET` | `/health` | ✅ Live | Checks running application status and database availability. |
| `POST` | `/scan/url` | 🟡 Planned | Evaluates a provided URL across all configured heuristic and feed engines. |
| `POST` | `/scan/file` | 🟡 Planned | Validates file header, matches hash, and evaluates against YARA/ClamAV. |
| `GET` | `/history` | 🟡 Planned | Returns paginated inspection history with scores and trigger reasons. |

### Example Scan Response (`POST /scan/url`)

```json
{
  "target": "http://pm-kisan-portal.payment-verify.in",
  "verdict": "Malicious",
  "score": 85,
  "reasons": [
    "Portal targets government welfare schemes but is registered on an unverified TLD (.in vs .gov.in)",
    "Domain was registered fewer than 7 days ago",
    "Contains deceptive identity-harvesting keywords: 'payment-verify', 'kisan'",
    "Active threat listing reported on URLhaus"
  ],
  "timestamp": "2026-10-26T00:15:00Z"
}
```

---

## 🗺️ Roadmap

- [x] **Phase 1:** Core setup, FastAPI initialization, configuration management, `/health` route.
- [ ] **Phase 2:** Static URL heuristic engine (regex patterns, entropy checks, domain age).
- [ ] **Phase 3:** Threat feed integration (VirusTotal, URLhaus, Safe Browsing).
- [ ] **Phase 4:** Government impersonation module and centralized scoring engine.
- [ ] **Phase 4b:** Human-friendly AI summary generation (including Hindi & Hinglish).
- [ ] **Phase 5:** Interactive frontend dashboard (submission interface, risk badges, alert popups).
- [ ] **Phase 6:** Static file evaluation (MIME matching, SHA-256 caching, YARA, ClamAV).
- [ ] **Phase 7:** Scan persistence layer and audit history endpoints.
- [ ] **Phase 8:** Real-time alerting framework (SMTP notifications and Telegram bot integration).
- [ ] **Phase 9:** Deep analysis (live sandboxed DOM inspection) / browser extension.
- [ ] **Phase 10:** Comprehensive test suites, Docker packaging, and deployment hardening.

---

## 🛡️ Security & Safe Handling

Because Hawkeye inspects hostile data inputs by design, the following architectural guardrails are enforced:

1. **Zero Execution Policy:** Uploaded files are never executed on the host system. Binaries and documents are analyzed strictly using static headers, hash matching, and isolated engine passes, then scrubbed from disk.
2. **Path Sanitization & Random IDs:** Uploaded payloads are given cryptographically random UUIDs and held outside web-accessible roots.
3. **SSRF Mitigation:** URL retrieval modules restrict calls destined for loopback addresses, RFC 1918 private subnets, and local link-local boundaries.
4. **Output Escaping:** Target URLs, parameters, and findings are output as inert text to prevent stored XSS vulnerabilities.
5. **Safe Testing Standards:** When testing file detection mechanics, use the standardized **EICAR Standard Anti-Virus Test File** instead of actual malware samples.

---

## ⚖️ Legal Disclaimer

Hawkeye provides risk assessments, not absolute guarantees. A `Safe` assessment does not ensure absolute safety, and a `Malicious` assessment should be independently verified before taking destructive remediation steps.

If you suspect you are the target of an online scam or financial fraud in India:
* File an official complaint via **[cybercrime.gov.in](https://cybercrime.gov.in/)**
* Call the **National Cyber Crime Helpline at `1930`**

*This project is created for awareness, education, and defense research. Never scan or probe targets without explicit permission.*

---

## 📄 License & Credits

* **Author:** [@Priyalsabharwa](https://github.com/Priyalsabharwa)
* **License:** [MIT License](LICENSE)
* **Acknowledgments:** Thank you to the teams and contributors behind VirusTotal, Google Safe Browsing, PhishTank, abuse.ch (URLhaus), and the open-source security community for public threat intelligence feeds.
