# scraper/website_scraper.py
import re
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Suppress SSL warnings for sites with bad certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Email Regex
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
# Phone Regex (US focused) - non-capturing group so findall returns full match
PHONE_REGEX = r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_emails(text):
    """Extract emails, filtering out common false positives like image files."""
    raw = set(re.findall(EMAIL_REGEX, text))
    # Filter out image/file extensions that look like emails
    filtered = set()
    for email in raw:
        lower = email.lower()
        if not any(lower.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js']):
            filtered.add(email)
    return filtered

def extract_phones(text):
    return set(re.findall(PHONE_REGEX, text))

def get_social_links(soup, base_url):
    socials = {
        "Instagram": "",
        "Facebook": "",
        "LinkedIn": "",
        "Twitter": "",
        "TikTok": "",
        "YouTube": "",
        "WhatsApp": ""
    }
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        lower_href = href.lower()
        
        if "instagram.com" in lower_href:
            socials["Instagram"] = href
        elif "facebook.com" in lower_href:
            socials["Facebook"] = href
        elif "linkedin.com" in lower_href:
            socials["LinkedIn"] = href
        elif "twitter.com" in lower_href or "x.com" in lower_href:
            socials["Twitter"] = href
        elif "tiktok.com" in lower_href:
            socials["TikTok"] = href
        elif "youtube.com" in lower_href:
            socials["YouTube"] = href
        elif "wa.me" in lower_href or "whatsapp.com" in lower_href or "api.whatsapp.com" in lower_href:
            socials["WhatsApp"] = href
            
    return socials

def _fetch_page(url):
    """Fetch a page and return (response, soup) or (None, None) on failure."""
    try:
        response = requests.get(url, timeout=10, headers=HEADERS, verify=False)
        if response.status_code != 200:
            return response, None
        try:
            soup = BeautifulSoup(response.text, 'lxml')
        except:
            soup = BeautifulSoup(response.text, 'html.parser')
        return response, soup
    except Exception:
        return None, None

def _find_contact_page_url(soup, base_url):
    """Try to find a contact or about page link on the homepage."""
    contact_keywords = ['contact', 'about', 'about-us', 'contact-us', 'get-in-touch']
    for a in soup.find_all('a', href=True):
        href_lower = a['href'].lower()
        text_lower = a.get_text(strip=True).lower()
        for keyword in contact_keywords:
            if keyword in href_lower or keyword in text_lower:
                full_url = urljoin(base_url, a['href'])
                # Only follow links on the same domain
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    return full_url
    return None

def analyze_website(url):
    """
    Visits the website and extracts contact details and quality score.
    Also checks the contact/about page for additional details.
    Returns a dictionary with extracted data.
    """
    data = {
        "Website": url,
        "Emails": [],
        "Phones": [],
        "Socials": {},
        "Quality Score": 10,
        "Notes": ""
    }
    
    if not url:
        data["Notes"] = "No Website"
        return data

    print(f"   [Website] Visiting: {url}")
    try:
        response, soup = _fetch_page(url)
        
        if response is None:
            data["Notes"] = "Connection Error"
            return data
        
        print(f"   [Website] Status Code: {response.status_code}")
        
        if soup is None:
            data["Notes"] = f"Error: {response.status_code}"
            return data
        
        # Extract from homepage
        text_content = soup.get_text()
        emails = extract_emails(text_content)
        phones = extract_phones(text_content)
        socials = get_social_links(soup, url)
        
        # Also check contact/about page for more details
        contact_url = _find_contact_page_url(soup, url)
        if contact_url and contact_url != url:
            print(f"   [Website] Also checking: {contact_url}")
            _, contact_soup = _fetch_page(contact_url)
            if contact_soup:
                contact_text = contact_soup.get_text()
                emails.update(extract_emails(contact_text))
                phones.update(extract_phones(contact_text))
                # Merge socials (prefer non-empty values)
                contact_socials = get_social_links(contact_soup, contact_url)
                for key, val in contact_socials.items():
                    if val and not socials.get(key):
                        socials[key] = val
        
        # Check for booking keywords
        booking_keywords = ["book online", "schedule appointment", "request appointment", "book now", "reserve", "make a reservation"]
        has_booking = any(keyword in text_content.lower() for keyword in booking_keywords)
        
        data["Emails"] = list(emails)
        data["Phones"] = list(phones)
        data["Socials"] = socials
        
        # Calculate Quality Score using already-fetched response (avoids double request)
        from utils.quality_score import calculate_quality_score_from_response
        score = calculate_quality_score_from_response(response, soup)
        data["Quality Score"] = score
        
        notes = []
        if not has_booking:
            notes.append("No booking system detected")
        if not emails:
            notes.append("No email found")
        if socials.get("Instagram"):
            notes.append("Has Instagram")
        if socials.get("Facebook"):
            notes.append("Has Facebook")
        data["Notes"] = ". ".join(notes) + "." if notes else ""
            
    except Exception as e:
        data["Notes"] = f"Scraping Error: {str(e)}"
        
    return data
