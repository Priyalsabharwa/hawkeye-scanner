# Hawkeye

**Scan files and links. Know why.**

Hawkeye is a multi-engine web platform that scans files and links for malware and phishing, with a special focus on **fake government websites**. Instead of a bare "safe or unsafe" answer, it combines threat-intelligence feeds, URL heuristics, impersonation checks, YARA rules and antivirus scanning, then explains exactly why something is dangerous and raises an instant alert.

> **Project status:** in active development. Phase 1 (project setup) is complete. See the [Roadmap](#roadmap) for what is built and what is planned.

---

## Why Hawkeye?

Fake websites that copy government portals (subsidy schemes, scholarship forms, Aadhaar/PAN updates, challan payments) trick people because they look official. Victims pay "fees" and hand over identity and bank details.

Many existing detection projects use a single machine learning model and return only a label such as "Phishing, 95%". Hawkeye takes a different approach:

| Common approach | Hawkeye |
|---|---|
| URLs only | Files **and** URLs |
| One ML model decides | Several engines contribute, ML (optional) is only a supporting signal |
| Output: a label and a percentage | Output: a verdict **with plain-language reasons** |
| No alerts | Instant alerts (in-app banner, email, Telegram) |
| Judges the URL text only | Can inspect the live page in a sandbox |
| No government-site focus | Dedicated fake government site detection |

---

## Planned features

- **URL analysis:** IP-based URLs, long URLs, `@` tricks, excessive subdomains, missing HTTPS, URL shorteners, suspicious keywords, lookalike domains and domain age
- **Threat intelligence:** Google Safe Browsing, URLhaus, PhishTank and VirusTotal lookups
- **Fake government site detection:** verified official domain list, domain-ending checks, lookalike names and urgency/payment language
- **File scanning:** SHA-256 hash lookup, real file type vs. fake extension, YARA rules and ClamAV
- **Explainable verdicts:** Safe, Suspicious or Malicious, with a list of reasons
- **Alerts:** red warning banner, email and Telegram notifications
- **Scan history:** every scan saved and viewable
- **AI explanations (planned):** an LLM turns technical findings into a friendly warning, including Hindi and Hinglish
- **Page sandbox (planned):** inspect login forms, hidden iframes and fake emblems on a live page
- **Browser extension, email scanner, QR scanner (optional):** pick one

---

## How it works

```
Browser / Extension
        |
        v
   API gateway (FastAPI)   -- validation, rate limiting
        |
        v
  Scan orchestrator        -- routes a URL or a file to the right engines
        |
        v
  Detection engines        -- each returns {engine, risk, findings}
  |  URL: threat feeds
  |  URL: heuristics
  |  URL: gov impersonation
  |  URL: page sandbox
  |  File: hash lookup
  |  File: YARA rules
  |  File: ClamAV
        |
        v
  Verdict engine           -- weighted score, reasons, optional AI explanation
        |
        v
  Database + Alert service
```

Every engine returns the same shape, which keeps the code simple and testable:

```json
{
  "engine": "url_heuristics",
  "risk": 40,
  "findings": [
    "Domain is 3 days old",
    "Not on the verified government domain list"
  ]
}
```

The verdict engine adds the scores (capped at 100) and maps them:

| Score | Verdict |
|---|---|
| 0 to 30 | Safe |
| 31 to 70 | Suspicious |
| 71 and above | Malicious |

---

## Tech stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| API | FastAPI, Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| URL analysis | `tldextract`, `python-whois`, `requests` |
| Threat feeds | Google Safe Browsing, URLhaus, PhishTank, VirusTotal |
| File scanning | `hashlib`, `python-magic`, `yara-python`, ClamAV |
| Storage | SQLite (PostgreSQL optional) |
| Alerts | `smtplib`, Telegram Bot API |
| Testing | `pytest` |
| Deployment | Docker, Docker Compose |

---

## Project structure

```
hawkeye/
├── backend/
│   ├── rules/                    # YARA rules
│   └── app/
│       ├── main.py               # API routes
│       ├── config.py             # settings and API keys
│       ├── schemas.py            # request/response shapes
│       ├── orchestrator.py       # picks which engines to run
│       ├── verdict.py            # scoring and reasons
│       ├── explain.py            # friendly explanations
│       ├── security.py           # rate limiting, upload validation
│       ├── database.py
│       ├── models.py
│       ├── alerts.py
│       ├── data/                 # gov domains, brands, shorteners (JSON)
│       └── engines/              # one file per detection engine
├── frontend/                     # HTML, CSS, JS
├── extension/                    # optional browser extension
├── ml/                           # optional URL classifier
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting started

### Prerequisites

- Python 3.11 or newer
- Git
- VS Code (recommended)

### Setup (Windows PowerShell)

```powershell
git clone https://github.com/Priyalsabharwa/hawkeye-scanner.git
cd hawkeye-scanner

python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
venv\Scripts\activate

pip install -r requirements.txt
```

### Setup (macOS / Linux)

```bash
git clone https://github.com/Priyalsabharwa/hawkeye-scanner.git
cd hawkeye-scanner

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Configure API keys

Create a `.env` file in the project root (this file is ignored by Git and must never be committed):

```
VIRUSTOTAL_API_KEY=your_key_here
SAFE_BROWSING_API_KEY=your_key_here
```

### Run the server

```
uvicorn backend.app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/health` for a status check
- `http://127.0.0.1:8000/docs` for the interactive API docs

---

## API

| Endpoint | Method | Status | Description |
|---|---|---|---|
| `/health` | GET | Available | Confirms the server is running |
| `/scan/url` | POST | Planned | Scan a URL |
| `/scan/file` | POST | Planned | Scan an uploaded file |
| `/history` | GET | Planned | List past scans |

Planned response format:

```json
{
  "verdict": "Malicious",
  "score": 85,
  "reasons": [
    "Page claims to be a government portal but the domain is not verified",
    "Domain was registered 3 days ago",
    "URL appears on a threat feed"
  ]
}
```

---

## Roadmap

- [x] **Phase 1:** project setup, FastAPI server, `/health` endpoint
- [ ] **Phase 2:** URL heuristics engine
- [ ] **Phase 3:** threat feed integration (Safe Browsing, URLhaus, VirusTotal)
- [ ] **Phase 4:** verdict engine and fake government site detection
- [ ] **Phase 4b:** AI-written explanations
- [ ] **Phase 5:** frontend (scan page, verdict badge, alert banner)
- [ ] **Phase 6:** file scanning (hash, file type, YARA, ClamAV)
- [ ] **Phase 7:** database and scan history
- [ ] **Phase 8:** alerts (in-app, email, Telegram)
- [ ] **Phase 9:** one extra feature (page sandbox, browser extension, or email/QR scanner)
- [ ] **Phase 10:** security hardening, tests, Docker, documentation

---

## Security notes

Hawkeye handles hostile input by design, so it follows these rules:

- Uploaded files are **never executed**. They are analysed, then deleted.
- Uploads are renamed to random IDs and stored outside any public folder.
- File size and type limits are enforced on the server.
- URL fetching will block private and internal addresses (SSRF protection).
- Scanned URLs and findings are displayed as plain text, never as clickable links or raw HTML.
- API keys live in `.env` and are never committed.
- To test file detection safely, use the harmless [EICAR test file](https://www.eicar.org/), not real malware.

---

## Disclaimer

Hawkeye gives a **risk assessment, not a guarantee**. A "Safe" result does not prove a file or link is harmless, and a "Malicious" result should be verified before acting. If you believe you have been targeted by a scam, report it at [cybercrime.gov.in](https://cybercrime.gov.in) or call the national cybercrime helpline at **1930** (India).

This project is built for learning and awareness. Do not use it to scan systems you do not have permission to test.

---

## Acknowledgments

Threat data and inspiration from Google Safe Browsing, URLhaus, PhishTank, VirusTotal and the open-source security community.

---

## Author

Built by [@Priyalsabharwa](https://github.com/Priyalsabharwa)

---

## License

License to be decided. MIT is a common choice for projects like this.
