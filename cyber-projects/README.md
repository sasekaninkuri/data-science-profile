# Cybersecurity Projects Suite

This suite contains three improved cybersecurity tools developed for your portfolio.

## 1. SecureLink Analyzer (Port 5000)
**Features Added:**
- **Persistent Scan History**: Uses SQLite/SQLAlchemy to remember previous scans.
- **Premium Dark Mode UI**: Modern, responsive design with risk-based color coding.
- **Enhanced Heuristics**: Analyzes SSL expiry, domain age, WHOIS registrar, and geo-location.

**How to run:**
```bash
cd securelink-analyzer
python run.py
```

## 2. Log-Sentinel SIEM (Port 5001)
**Features Added:**
- **SOC-Style Dashboard**: Integrated Chart.js for real-time log frequency visualization.
- **Anonymous/Mock Data Fallback**: Automatically generates sample logs if MongoDB is unavailable.
- **Compliance Mapping**: Directly maps security events to NIST CSF and ISO 27001 controls.
- **Exporting Suite**: Enhanced CSV and JSON export functionality.

**How to run:**
```bash
cd log-sentinel-siem
python run.py
```

## 3. Network Anomaly Detector (Port 5002)
**Features Added (New Implementation):**
- **Statistical Z-Score Engine**: Detects outliers in network traffic (e.g., packet length spikes).
- **Traffic Dashboard**: Visual summary of anomaly rates and total packet counts.
- **CSV Analysis**: Supports uploading standard network traffic captures for bulk analysis.

**How to run:**
```bash
cd network-anomaly-detector
python app.py
```
