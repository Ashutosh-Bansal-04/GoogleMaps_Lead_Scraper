# utils/quality_score.py
import requests
from bs4 import BeautifulSoup
import re

def check_ssl(url):
    return url.startswith("https")

def check_mobile_friendly(soup):
    viewport = soup.find("meta", attrs={"name": "viewport"})
    return viewport is not None

def check_modern_tech(soup):
    # Heuristic: Check for modern frameworks or meta generators
    html_str = str(soup).lower()
    modern_keywords = [
        "react", "next.js", "gatsby", "vue", "nuxt", "tailwind", "bootstrap",
        "wix", "squarespace", "webflow", "shopify"
    ]
    for keyword in modern_keywords:
        if keyword in html_str:
            return True
    return False

def check_copyright_year(soup):
    html_str = str(soup).lower()
    # Simple regex to find "copyright 20XX" or "(c) 20XX"
    matches = re.findall(r"(?:copyright|©|\(c\))\s*(?:20\d{2})", html_str)
    if matches:
        # Get the max year found
        years = []
        for match in matches:
            try:
                year = int(re.search(r"20\d{2}", match).group(0))
                years.append(year)
            except:
                pass
        if years:
            return max(years)
    return None

def calculate_quality_score_from_response(response, soup):
    """
    Analyzes the website using an already-fetched response and parsed soup.
    Avoids making a duplicate HTTP request.
    
    Score meanings:
      10 = No website / Connection Error
       8 = Outdated / Not mobile friendly / HTTP only
       5 = Average
       0 = Modern / High Quality
    """
    if response is None or soup is None:
        return 10
    
    if response.status_code != 200:
        return 10
    
    score = 5  # Default average
    
    # Check 1: SSL
    if not check_ssl(response.url):
        return 8  # Not secure = Outdated
        
    # Check 2: Mobile Friendly (Viewport)
    if not check_mobile_friendly(soup):
        return 8  # Not mobile friendly
        
    # Check 3: Modern Tech
    if check_modern_tech(soup):
        return 0  # Modern high-quality website
        
    # Check 4: Copyright Year
    latest_year = check_copyright_year(soup)
    if latest_year and latest_year < 2020:
        return 8  # Old copyright
        
    return score

def calculate_quality_score(url):
    """
    Legacy function - fetches the URL and analyzes it.
    Prefer calculate_quality_score_from_response() to avoid duplicate requests.
    """
    if not url:
        return 10
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        if response.status_code != 200:
            return 10
    except Exception:
        return 10

    try:
        soup = BeautifulSoup(response.text, "lxml")
    except:
        soup = BeautifulSoup(response.text, "html.parser")
    
    return calculate_quality_score_from_response(response, soup)
