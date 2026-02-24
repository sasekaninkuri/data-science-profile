import os

def analyze_attachment(file_path):
    if not os.path.isfile(file_path):
        return "File not found"
    
    suspicious_types = ['.exe', '.vbs', '.js']
    if any(file_path.endswith(ext) for ext in suspicious_types):
        return "Suspicious file type"
    
    return "Safe"