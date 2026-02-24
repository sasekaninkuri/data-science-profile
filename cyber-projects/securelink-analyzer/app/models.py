from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    verdict = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "verdict": self.verdict,
            "score": self.score,
            "scan_date": self.scan_date.strftime("%Y-%m-%d %H:%M:%S")
        }
