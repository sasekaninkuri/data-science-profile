from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def detect_anomalies(df):
    """
    Simple statistical anomaly detection using Z-Score on numerical columns.
    """
    results = df.copy()
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    anomalies_found = False
    results['is_anomaly'] = False
    results['anomaly_reason'] = ""
    
    for col in numerical_cols:
        mean = df[col].mean()
        std = df[col].std()
        if std == 0: continue
        
        z_scores = (df[col] - mean) / std
        is_anomaly = np.abs(z_scores) > 2.5 # Threshold for anomaly
        
        results.loc[is_anomaly, 'is_anomaly'] = True
        results.loc[is_anomaly, 'anomaly_reason'] += f" High {col} (Z={z_scores[is_anomaly].round(2)});"
        
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
                # Ensure we have some data
                if df.empty:
                    return render_template('index.html', error="CSV file is empty")
                
                results = detect_anomalies(df)
                
                # Summary stats
                total = len(results)
                anomalies = results[results['is_anomaly']]
                anomaly_count = len(anomalies)
                
                return render_template('index.html', 
                                     results=results.to_dict('records'),
                                     total=total,
                                     anomaly_count=anomaly_count,
                                     filename=filename)
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {str(e)}")
                
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
