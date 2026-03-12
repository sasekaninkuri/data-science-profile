from flask import Flask, render_template, request, redirect, url_for
import email
from email import policy
from email.parser import BytesParser
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Common phishing keywords
SUSPICIOUS_KEYWORDS = [
    'urgent', 'immediate action', 'account suspended', 'verify your account',
    'password reset', 'bank', 'login', 'security alert', 'unauthorized access',
    'prize', 'winner', 'free', 'click here'
]

def analyze_email_content(raw_content):
    msg = email.message_from_string(raw_content, policy=policy.default)
    
    subject = msg.get('Subject', '(No Subject)')
    sender = msg.get('From', '(No Sender)')
    to = msg.get('To', '(No Recipient)')
    date = msg.get('Date', '(No Date)')
    
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body += part.get_payload(decode=True).decode(errors='ignore')
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    # 1. Extract URLs
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_regex, body)
    
    # 2. Key word analysis
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw.lower() in body.lower() or kw.lower() in subject.lower()]
    
    # 3. Risk Scoring
    score = 0
    reasons = []
    
    if len(urls) > 3:
        score += 20
        reasons.append(f"High number of links ({len(urls)}) detected.")
    
    for url in urls:
        if 'bit.ly' in url or 't.co' in url or 'tinyurl' in url:
            score += 15
            reasons.append("Shortened URLs detected (often used to hide malicious links).")
            break
            
    if found_keywords:
        score += len(found_keywords) * 10
        reasons.append(f"Suspicious keywords found: {', '.join(found_keywords[:3])}...")

    # Header analysis (Simplified)
    received_headers = msg.get_all('Received', [])
    if len(received_headers) > 5:
        score += 10
        reasons.append("Email passed through many relays.")

    risk_level = "LOW"
    if score > 60:
        risk_level = "CRITICAL"
    elif score > 30:
        risk_level = "MEDIUM"
        
    return {
        "subject": subject,
        "from": sender,
        "to": to,
        "date": date,
        "body_preview": body[:500] + "..." if len(body) > 500 else body,
        "urls": list(set(urls)),
        "risk_score": min(score, 100),
        "risk_level": risk_level,
        "reasons": reasons,
        "keywords": found_keywords
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    if request.method == 'POST':
        raw_email = request.form.get('raw_email')
        file = request.files.get('file')
        
        content = ""
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        elif raw_email:
            content = raw_email
            
        if content:
            try:
                analysis = analyze_email_content(content)
            except Exception as e:
                return render_template('index.html', error=f"Analysis failed: {str(e)}")
                
    return render_template('index.html', analysis=analysis)

if __name__ == '__main__':
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    app.template_folder = template_dir
    app.run(debug=True, port=5003)
