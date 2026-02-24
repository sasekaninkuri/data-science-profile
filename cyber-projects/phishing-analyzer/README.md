# Phishing Email Forensics Analyzer

## Overview
A tool to analyze suspicious emails and detect potential phishing attempts.

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`

## Setup
1. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the analyzer:
    ```bash
    python main.py <email_file>
    ```

## Usage
- Provide the path to the email file as an argument.
- The tool will analyze the email and generate a report.

## Files
- `blacklisted_urls.txt`: List of known malicious URLs.
- `training_data.csv`: Optional training data for machine learning.