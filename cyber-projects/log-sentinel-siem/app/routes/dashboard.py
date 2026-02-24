
from flask import Blueprint, render_template, send_file, make_response, jsonify
from app.utils.db import get_all_logs
import csv, io, json, random, datetime

dashboard_bp = Blueprint('dashboard', __name__)

# ─────────────────────────────────────────────
# 🧠 ROUTES
# ─────────────────────────────────────────────

@dashboard_bp.route('/')
def dashboard():
    try:
        events = get_all_logs()
    except Exception:
        events = []

    # Mock Data Fallback if DB is empty or missing
    if not events:
        levels = ["INFO", "WARNING", "ERROR"]
        msgs = ["User login", "File deletion", "Unauthorized access", "Port scan detected"]
        for i in range(20):
            ts = (datetime.datetime.now() - datetime.timedelta(minutes=i*15)).strftime("%Y-%m-%d %H:%M:%S")
            lvl = random.choice(levels)
            events.append({
                "timestamp": ts,
                "level": lvl,
                "message": random.choice(msgs),
                "is_suspicious": lvl == "ERROR"
            })
    
    # Statistics
    total_events = len(events)
    suspicious_events = [e for e in events if e.get('is_suspicious')]
    suspicious_count = len(suspicious_events)
    
    # Frequency analysis (Simple Anomaly Detection)
    # Count events per hour
    from collections import Counter
    hours = [e.get('timestamp').split(' ')[1].split(':')[0] for e in events if e.get('timestamp')]
    freq = Counter(hours)
    
    # Calculate Risk Level
    risk_score = (suspicious_count / total_events * 100) if total_events > 0 else 0
    risk_level = "High" if risk_score > 20 else ("Medium" if risk_score > 5 else "Low")

    return render_template(
        'dashboard.html',
        events=events,
        total_count=total_events,
        suspicious_count=suspicious_count,
        risk_score=round(risk_score, 1),
        risk_level=risk_level,
        hour_data=json.dumps(list(freq.values())),
        hour_labels=json.dumps(list(freq.keys()))
    )

@dashboard_bp.route('/export/csv')
def export_csv():
    events = get_all_logs()

    proxy = io.StringIO()
    writer = csv.writer(proxy)
    writer.writerow(['Timestamp', 'Level', 'Message', 'Suspicious'])

    for event in events:
        writer.writerow([
            event.get('timestamp'),
            event.get('level'),
            event.get('message'),
            'Yes' if event.get('is_suspicious') else 'No'
        ])

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        download_name='logs_export.csv',
        mimetype='text/csv'
    )

@dashboard_bp.route('/export/json')
def export_json():
    events = get_all_logs()
    response = make_response(json.dumps(events, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=logs_export.json'
    response.mimetype = 'application/json'
    return response

@dashboard_bp.route('/compliance')
def compliance():
    return jsonify({
        "NIST_CSF": {
            "Identify": "ID.AM-1: Asset management for logs and hosts",
            "Detect": "DE.CM-1: Real-time monitoring of logs",
            "Respond": "RS.AN-1: Alerts generated on suspicious activity",
            "Recover": "RC.CO-1: Exporting logs to assist recovery"
        },
        "ISO_27001": {
            "A.12.4.1": "Event logging enabled",
            "A.16.1.2": "Incident detection and alerting"
        }
    })
