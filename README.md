# ReconWizard

ReconWizard is a Python-based reconnaissance tool that collects **DNS**, **GeoIP**, **HTTP**, **open ports**, **WHOIS**, and basic **OSINT** data for a target domain/IP, then generates clean **HTML**, **JSON**, and **Markdown** reports.  
It also supports **change detection** (diff vs previous run), **charts**, **auto-open in browser**, optional **PDF export**, and **archiving** of older reports.

---

## ✨ Features

- DNS records (A/AAAA/MX/NS/TXT)
- HTTP probe (status, headers, cookies, final URL, favicon SHA256)
- Quick port scan (via `nmap -F`, non-blocking if missing)
- WHOIS (normalized dates, registrar, nameservers, emails)
- GeoIP (country/region/city/ISP)
- OSINT profile (crt.sh subdomains, GitHub mentions, HIBP hint)
- HTML report (Bootstrap + Chart.js) with risk hints and charts
- JSON + Markdown exports
- Auto-open HTML report, ZIP archive of older reports
- Diff vs previous report (ports/DNS A/HTTP key headers/WHOIS expiry)

---

## 📦 Requirements

- Python **3.8+**
- Python packages (see `requirements.txt`):
  - `requests`, `dnspython`, `python-whois`, `jinja2`
  - Optional: `fpdf` (for simple PDF export)
- Optional system tools:
  - **nmap** (for port scan)  
    - macOS: `brew install nmap`  
    - Debian/Ubuntu: `sudo apt install nmap`
  - **wkhtmltopdf** (if you later prefer HTML→PDF conversion via `pdfkit`)

> The tool gracefully skips optional parts if a dependency is missing (e.g., no nmap installed → no crash).

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/ReconWizard.git
cd ReconWizard

python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Run a scan (HTML opens automatically after completion)
python3 ReconWizard.py --target example.com
# ReconWizard

ReconWizard is a Python-based reconnaissance tool that collects **DNS**, **GeoIP**, **HTTP**, **open ports**, **WHOIS**, and basic **OSINT** data for a target domain/IP, then generates clean **HTML**, **JSON**, and **Markdown** reports.  
It also supports **change detection** (diff vs previous run), **charts**, **auto-open in browser**, optional **PDF export**, and **archiving** of older reports.

---

## ✨ Features

- DNS records (A/AAAA/MX/NS/TXT)
- HTTP probe (status, headers, cookies, final URL, favicon SHA256)
- Quick port scan (via `nmap -F`, non-blocking if missing)
- WHOIS (normalized dates, registrar, nameservers, emails)
- GeoIP (country/region/city/ISP)
- OSINT profile (crt.sh subdomains, GitHub mentions, HIBP hint)
- HTML report (Bootstrap + Chart.js) with risk hints and charts
- JSON + Markdown exports
- Auto-open HTML report, ZIP archive of older reports
- Diff vs previous report (ports/DNS A/HTTP key headers/WHOIS expiry)

---

## 📦 Requirements

- Python **3.8+**
- Python packages (see `requirements.txt`):
  - `requests`, `dnspython`, `python-whois`, `jinja2`
  - Optional: `fpdf` (for simple PDF export)
- Optional system tools:
  - **nmap** (for port scan)  
    - macOS: `brew install nmap`  
    - Debian/Ubuntu: `sudo apt install nmap`
  - **wkhtmltopdf** (if you later prefer HTML→PDF conversion via `pdfkit`)

> The tool gracefully skips optional parts if a dependency is missing (e.g., no nmap installed → no crash).

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/ReconWizard.git
cd ReconWizard

python3 -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Run a scan (HTML opens automatically after completion)
python3 ReconWizard.py --target example.com
python3 ReconWizard.py --target <domain-or-ip> [--no-open] [--no-archive] [--pdf]

# Basic scan
python3 ReconWizard.py --target google.com

# Run without auto-opening or archiving
python3 ReconWizard.py --target example.com --no-open --no-archive

# Try to also save a PDF (needs 'fpdf' installed)
python3 ReconWizard.py --target example.com --pdf

Example Output
[+] Starting reconnaissance: example.com
[+] HTML report saved: reports/example.com-20250815-132000.html
[+] JSON saved: reports/example.com-20250815-132000.json
[+] Markdown report saved: reports/example.com-20250815-132000.md
[+] No previous data to compare or no changes detected.
Open the HTML report in your browser to see:
Summary with risk badges (HTTP status, open ports, SSL expiry)
Port bar chart & security headers chart
Sections for DNS / GeoIP / HTTP / Ports / OSINT / WHOIS
Diff section (if a previous JSON exists)


Notes-Disclaimer
ReconWizard is for authorized security testing and research only.
Do not scan targets without permission.
Public APIs used (e.g., ip-api.com, crt.sh) may have rate limits.
The tool is an MVP; verify all findings manually before acting on them.

Developmen 
Format/linters: use your preferred tools (e.g., ruff, black).
Roadmap ideas:
Tech fingerprinting (Wappalyzer)
Better OSINT sources & enrichment
Headless screenshot capture
HTML→PDF via pdfkit/wkhtmltopdf
CI workflow (GitHub Actions) for smoke tests

License
MIT — see LICENSE (or choose a license you prefer).

Acknowledgements
nmap for port scanning
dnspython, requests, python-whois
Bootstrap & Chart.js for report UI# ReconWizard
# ReconWizard
# ReconWizard
# ReconWizard
# ReconWizard
# ReconWizard
# ReconWizard
# ReconWizard
