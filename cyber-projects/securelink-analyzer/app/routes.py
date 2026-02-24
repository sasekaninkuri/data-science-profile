from flask import Blueprint, render_template, request, redirect, url_for, make_response
from .analyzer import analyze_url
from .models import db, ScanHistory

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    history = ScanHistory.query.order_by(ScanHistory.scan_date.desc()).limit(10).all()
    
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                result = analyze_url(url)
                # Save to history
                new_scan = ScanHistory(
                    url=url, 
                    verdict=result['verdict'], 
                    score=result['score']
                )
                db.session.add(new_scan)
                db.session.commit()
                # Refresh history
                history = ScanHistory.query.order_by(ScanHistory.scan_date.desc()).limit(10).all()
            except Exception as e:
                result = {"error": str(e)}
    return render_template("index.html", result=result, history=history)

@main_bp.route("/export")
def export_history():
    history = ScanHistory.query.order_by(ScanHistory.scan_date.desc()).all()
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["URL", "Verdict", "Score", "Scan Date"])
    for item in history:
        writer.writerow([item.url, item.verdict, item.score, item.scan_date])
    
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=scan_history.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@main_bp.route("/clear-history")
def clear_history():
    ScanHistory.query.delete()
    db.session.commit()
    return redirect(url_for('main.index'))


