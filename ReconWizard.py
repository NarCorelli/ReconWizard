# ReconWizard.py (fixed English version)
import argparse
import os
import sys
import json
import zipfile
import webbrowser
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader

# Make modules importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.utils import ensure_dir
from modules.resolver import resolve_domain, get_dns_records
from modules.http_probe import probe_http
from modules.ports import scan_ports
from modules.whois_lookup import get_whois        # <- correct name
from modules.geoip_lookup import get_geoip        # <- correct name
from modules.osint_profile import osint_profile   # <- correct name


def save_markdown_report(target, timestamp, sections):
    """Save markdown version of the report."""
    report_path = os.path.join('reports', f"{target}-{timestamp}.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Recon Report: {target}\n\n")
        f.write(f"**Scan Time:** {timestamp} UTC\n\n")
        for section, data in sections.items():
            f.write(f"## {section}\n")
            f.write("```\n")
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
            f.write("\n```\n\n")
    print(f"[+] Markdown report saved: {report_path}")
    return report_path


def save_html_report(target, timestamp, sections):
    """Generate HTML report using Jinja2 template (templates/report.html)."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    html_content = template.render(target=target, timestamp=timestamp, sections=sections)
    html_path = os.path.join('reports', f"{target}-{timestamp}.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] HTML report saved: {html_path}")
    return html_path


def save_pdf_report(target, timestamp, sections):
    """
    Generate a simple PDF.
    Lazy-import fpdf so the app still runs if it's not installed.
    pip install fpdf  (optional)
    """
    try:
        from fpdf import FPDF
    except Exception as e:
        print(f"[i] Skipping PDF (fpdf not installed): {e}")
        return None

    pdf_path = os.path.join('reports', f"{target}-{timestamp}.pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, f"Recon Report: {target}", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Scan Time: {timestamp} UTC", ln=True)
    pdf.ln(4)
    for section, data in sections.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, section, ln=True)
        pdf.set_font("Courier", size=8)
        pdf.multi_cell(0, 5, json.dumps(data, indent=2, ensure_ascii=False))
        pdf.ln(2)
    pdf.output(pdf_path)
    print(f"[+] PDF report saved: {pdf_path}")
    return pdf_path


def archive_old_reports(max_keep: int = 5):
    """Zip older reports when there are more than `max_keep` markdown reports."""
    ensure_dir('reports')
    md_reports = sorted([f for f in os.listdir('reports') if f.endswith('.md')])
    if len(md_reports) <= max_keep:
        return
    zip_name = os.path.join('reports', 'archived_reports.zip')
    with zipfile.ZipFile(zip_name, 'a', compression=zipfile.ZIP_DEFLATED) as zf:
        for fname in md_reports[:-max_keep]:
            path = os.path.join('reports', fname)
            zf.write(path, fname)
            try:
                os.remove(path)
            except Exception:
                pass
    print("[+] Old reports archived.")


def compare_with_previous(target, sections):
    """Compare current scan with the most recent JSON for this target (if any)."""
    ensure_dir('reports')
    jsons = sorted([f for f in os.listdir('reports') if f.startswith(target) and f.endswith('.json')])
    if not jsons:
        return None
    latest = jsons[-1]
    try:
        with open(os.path.join('reports', latest), 'r', encoding='utf-8') as f:
            old = json.load(f)
    except Exception:
        return None
    changes = {}
    for k, v in sections.items():
        if k in old and old[k] != v:
            changes[k] = {"old": old[k], "new": v}
    return changes or None


def main():
    parser = argparse.ArgumentParser(description="ReconWizard: Automated Recon Tool")
    parser.add_argument('--target', default='example.com', help='Target domain or IP address')
    parser.add_argument('--no-open', action='store_true', help="Do not auto-open HTML report")
    args = parser.parse_args()

    target = args.target.strip()
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')

    ensure_dir('reports')
    print(f"[+] Starting reconnaissance: {target}")

    # Collect data
    sections = {}
    sections["Resolved IP"]   = resolve_domain(target)
    sections["DNS Records"]   = get_dns_records(target)
    sections["GeoIP Info"]    = get_geoip(target)          # <- fixed
    sections["HTTP Info"]     = probe_http(target)
    sections["Open Ports"]    = scan_ports(target)
    sections["WHOIS Info"]    = get_whois(target)          # <- fixed
    sections["OSINT Profile"] = osint_profile(target)      # <- fixed

    # Save raw JSON (for future comparisons)
    json_path = os.path.join('reports', f"{target}-{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    # Render reports
    md_path   = save_markdown_report(target, timestamp, sections)
    html_path = save_html_report(target, timestamp, sections)
    save_pdf_report(target, timestamp, sections)  # optional

    # Show changes vs last run
    changes = compare_with_previous(target, sections)
    if changes:
        print("[!] Changes since last scan:")
        print(json.dumps(changes, indent=2, ensure_ascii=False))
    else:
        print("[+] No previous data to compare or no changes detected.")

    # Archive if too many old reports
    archive_old_reports(max_keep=5)

    # Auto-open HTML
    if not args.no_open:
        webbrowser.open("file://" + os.path.abspath(html_path))


if __name__ == "__main__":
    main()
