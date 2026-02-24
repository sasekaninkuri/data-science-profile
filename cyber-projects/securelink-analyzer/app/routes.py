from flask import Blueprint, render_template, request, redirect, url_for
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

@main_bp.route("/clear-history")
def clear_history():
    ScanHistory.query.delete()
    db.session.commit()
    return redirect(url_for('main.index'))


