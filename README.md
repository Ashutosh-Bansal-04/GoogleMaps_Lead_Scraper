# GoogleMaps Lead Scraper

A web-based tool that scrapes Google Maps for business leads and enriches them with website data (emails, phone numbers, social media links, quality scores).

## Features

- **Google Maps Scraping** — Selenium-based scraper that extracts business details from Maps
- **Website Enrichment** — Visits each business website to extract emails, phones, social links
- **Contact Page Crawling** — Also checks /contact and /about pages for additional details
- **Quality Scoring** — Rates each website's quality (0=Modern, 5=Average, 8=Outdated, 10=None)
- **CSV Export** — Downloads results as a structured CSV with 18 columns
- **Web UI** — Beautiful glassmorphic interface accessible from any browser

## CSV Output Columns

| Column | Source |
|--------|--------|
| Business Name | Google Maps |
| Category | Google Maps |
| Website | Google Maps |
| Phone | Maps + Website |
| Email | Website |
| Address | Google Maps |
| City | User input |
| Rating | Google Maps |
| Reviews | Google Maps |
| Instagram | Website |
| Facebook | Website |
| LinkedIn | Website |
| Twitter | Website |
| TikTok | Website |
| YouTube | Website |
| WhatsApp | Website |
| Quality Score | Website analysis |
| Notes | Auto-generated |

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open in browser
# http://127.0.0.1:5002
```

## Deployment on Render (Recommended)

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

> **Note:** This app requires Chrome/Selenium which needs Docker. Vercel (serverless) cannot run this app. Use Render (free tier, Docker support).

## Tech Stack

- **Backend:** Python, Flask, Gunicorn
- **Scraping:** Selenium, BeautifulSoup, Requests
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Docker, Render
