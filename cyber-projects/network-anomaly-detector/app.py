from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
from sklearn.ensemble import IsolationForest
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def detect_anomalies(df):
    """
    Advanced anomaly detection using Isolation Forest.
    """
    results = df.copy()
    
    # Select only numerical columns for detection
    numerical_df = df.select_dtypes(include=[np.number])
    
    if numerical_df.empty:
        results['is_anomaly'] = False
        results['score'] = 0
        return results

    # Initialize Isolation Forest
    # contamination is the expected proportion of outliers (anomalies)
    model = IsolationForest(contamination=0.05, random_state=42)
    
    # Fit the model and predict
    # -1 for outliers, 1 for inliers
    preds = model.fit_predict(numerical_df)
    scores = model.decision_function(numerical_df)
    
    results['is_anomaly'] = (preds == -1)
    results['anomaly_score'] = scores.round(4)
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                df = pd.read_csv(filepath)
                if df.empty:
                    return render_template('index.html', error="CSV file is empty")
                
                results = detect_anomalies(df)
                
                # Summary stats
                total = len(results)
                anomaly_count = int(results['is_anomaly'].sum())
                
                return render_template('index.html', 
                                     results=results.to_dict('records'),
                                     total=total,
                                     anomaly_count=anomaly_count,
                                     filename=filename)
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {str(e)}")
                
    return render_template('index.html')

@app.route('/sample-data')
def sample_data():
    """Generates a sample network traffic CSV file."""
    n_rows = 100
    data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=n_rows, freq='min'),
        'source_ip': [f'192.168.1.{np.random.randint(1, 255)}' for _ in range(n_rows)],
        'dest_ip': [f'10.0.0.{np.random.randint(1, 255)}' for _ in range(n_rows)],
        'packet_length': np.random.normal(500, 200, n_rows).clip(64, 1500),
        'protocol': np.random.choice(['TCP', 'UDP', 'ICMP'], n_rows),
        'flags': np.random.choice(['SYN', 'ACK', 'FIN', 'PSH'], n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Inject some anomalies
    df.loc[10, 'packet_length'] = 5000 # Massive packet
    df.loc[50, 'packet_length'] = 10   # Tiny packet
    df.loc[80, 'packet_length'] = 4500 # Another massive one
    
    proxy_file = io.BytesIO()
    df.to_csv(proxy_file, index=False)
    proxy_file.seek(0)
    
    return send_file(
        proxy_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='sample_traffic.csv'
    )

if __name__ == '__main__':
    # Use absolute path for template folder to avoid TemplateNotFound errors
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    app.template_folder = template_dir
    app.run(debug=True, port=5002)

