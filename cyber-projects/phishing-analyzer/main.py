import sys
from email_parser import parse_email
from link_checker import check_url
from attachment_analyzer import analyze_attachment
from report_generator import generate_report

def main(email_file):
    with open(email_file, 'r') as file:
        raw_email = file.read()
    
    email_data = parse_email(raw_email)
    
    # Analyze URLs
    urls = extract_urls(email_data['body'])
    url_results = {url: check_url(url) for url in urls}
    
    # Analyze attachments (mockup)
    attachments = []  # Assume we extract attachment filenames somehow
    attachment_results = {att: analyze_attachment(att) for att in attachments}
    
    # Compile report data
    report_data = {
        "email": email_data,
        "url_results": url_results,
        "attachment_results": attachment_results
    }
    
    generate_report(report_data, "report.csv")

def extract_urls(body):
    # Simple URL extraction (placeholder)
    return ["http://example.com"]  # Replace with actual URL extraction logic

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <email_file>")
        sys.exit(1)
    
    email_file = sys.argv[1]
    main(email_file)