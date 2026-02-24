import whois
import re
import ssl
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime

def analyze_url(url):
    parsed = urlparse(url)
    hostname = parsed.hostname

    # 1. Check HTTPS
    uses_https = parsed.scheme == "https"

    # 2. Check for IP address instead of domain
    is_ip = bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname or ""))

    # 3. Suspicious TLDs
    tld = hostname.split(".")[-1] if hostname else ""
    suspicious_tlds = ["ru", "cn", "tk"]
    suspicious_tld = tld in suspicious_tlds

    # 4. WHOIS data
    try:
        w = whois.whois(hostname)
        registrar = w.registrar
        creation_date = w.creation_date
        expiration_date = w.expiration_date
    except Exception:
        registrar = creation_date = expiration_date = None

    def calculate_domain_age(created):
        if isinstance(created, list):
            created = created[0]
        if isinstance(created, datetime):
            return (datetime.now() - created).days
        return None

    domain_age_days = calculate_domain_age(creation_date)

    # 5. Check if URL is shortened
    def is_shortened_url(domain):
        short_domains = ['bit.ly', 't.co', 'tinyurl.com', 'goo.gl', 'ow.ly']
        return domain.lower() in short_domains

    shortened = is_shortened_url(parsed.netloc)

    # 6. Phishing keywords in URL
    def contains_phishing_keywords(url):
        keywords = ['login', 'verify', 'account', 'update', 'banking', 'secure', 'ebay', 'paypal']
        return any(kw in url.lower() for kw in keywords)

    phishing_keywords = contains_phishing_keywords(url)

    # 7. Obfuscated URL (percent encoding or hex)
    def is_obfuscated(url):
        return '%' in url or bool(re.search(r'0x[0-9a-fA-F]+', url))

    obfuscated = is_obfuscated(url)

    # 8. SSL Certificate Expiry
    def get_ssl_expiry(domain):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    expiry = cert.get('notAfter')
                    if expiry:
                        return datetime.strptime(expiry, '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d')
        except Exception:
            return None

    ssl_expiry = get_ssl_expiry(hostname) if uses_https and hostname else None

    # 9. Geolocation
    def get_geo_location(domain):
        try:
            ip = socket.gethostbyname(domain)
            res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
            return res.json().get("country_name", "Unknown")
        except Exception:
            return "Unknown"

    geo_location = get_geo_location(hostname) if hostname else "Unknown"

    # 10. Redirect count
    def count_redirects(url):
        try:
            r = requests.get(url, allow_redirects=True, timeout=5)
            return len(r.history)
        except Exception:
            return None

    redirects = count_redirects(url)

    # 11. Suspicious subdomains
    suspicious_subdomain = len(hostname.split(".")) > 3 if hostname else False

    # 12. IDN detection
    idn_domain = hostname.startswith("xn--") if hostname else False

    # Final score
    score = sum([
        not uses_https,
        is_ip,
        suspicious_tld,
        registrar is None,
        shortened,
        phishing_keywords,
        obfuscated,
        redirects is not None and redirects > 3,
        suspicious_subdomain,
        idn_domain,
        domain_age_days is not None and domain_age_days < 30
    ])

    # Verdict
    if score >= 6:
        verdict = "Malicious"
    elif 3 <= score < 6:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    # Helper to format date
    def format_date(date):
        if isinstance(date, list):
            date = date[0]
        if isinstance(date, datetime):
            return date.strftime("%Y-%m-%d")
        return str(date) if date else "Unavailable"

    return {
        "url": url,
        "uses_https": uses_https,
        "is_ip": is_ip,
        "suspicious_tld": suspicious_tld,
        "registrar": registrar or "Unavailable",
        "creation_date": format_date(creation_date),
        "expiration_date": format_date(expiration_date),
        "domain_age_days": domain_age_days if domain_age_days is not None else "Unavailable",
        "shortened": shortened,
        "phishing_keywords": phishing_keywords,
        "obfuscated": obfuscated,
        "ssl_expiry": ssl_expiry or "Unavailable",
        "geo_location": geo_location,
        "redirects": redirects if redirects is not None else "Unavailable",
        "suspicious_subdomain": suspicious_subdomain,
        "idn_domain": idn_domain,
        "score": score,
        "verdict": verdict
    }

