# 🗺️ Google Maps Lead Scraper

A powerful, autonomous lead generation tool that scrapes Google Maps for business details and enriches them by visiting each business website — extracting emails, phone numbers, social media links, and quality scores.

Built with **Python + Selenium + Flask**, it comes with a sleek web UI for easy use.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_UI-green?logo=flask&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Scraping-orange?logo=selenium&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Google Maps Scraping** | Extracts business name, address, phone, website, rating, reviews, category |
| 🌐 **Website Enrichment** | Visits each business website to find emails, phone numbers, social links |
| 📄 **Contact Page Crawling** | Automatically finds and scrapes `/contact` and `/about` pages |
| 📊 **Quality Scoring** | Rates each website (0 = Modern, 5 = Average, 8 = Outdated, 10 = None) |
| 📥 **CSV Export** | One-click download of all scraped data as a structured CSV |
| 🎨 **Web UI** | Beautiful glassmorphic dark-theme interface |
| ⏹️ **Stop Control** | Stop scraping mid-run from the UI |
| 🏙️ **Multi-City Support** | Search any city + any business type |

---

## 📸 Screenshot

> The app runs in your browser at `http://127.0.0.1:5002`

---

## 📋 CSV Output (18 Columns)

| # | Column | Source |
|---|--------|--------|
| 1 | Business Name | Google Maps |
| 2 | Category | Google Maps |
| 3 | Website | Google Maps |
| 4 | Phone | Maps + Website (merged) |
| 5 | Email | Website scraping |
| 6 | Address | Google Maps |
| 7 | City | Your input |
| 8 | Rating | Google Maps (e.g., 4.5) |
| 9 | Reviews | Google Maps (count) |
| 10 | Instagram | Website links |
| 11 | Facebook | Website links |
| 12 | LinkedIn | Website links |
| 13 | Twitter / X | Website links |
| 14 | TikTok | Website links |
| 15 | YouTube | Website links |
| 16 | WhatsApp | Website links |
| 17 | Quality Score | Website analysis |
| 18 | Notes | Auto-generated |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Google Chrome** — [Download](https://www.google.com/chrome/)
- ChromeDriver is installed automatically by `webdriver-manager`

### Installation

```bash
# Clone the repo
git clone https://github.com/Ashutosh-Bansal-04/GoogleMaps_Lead_Scraper.git
cd GoogleMaps_Lead_Scraper

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open **http://127.0.0.1:5002** in your browser.

### Usage

1. Enter a **Target City** (e.g., `Austin TX`)
2. Enter a **Search Query** (e.g., `HVAC Contractors`)
3. Set **Max Leads** (start with 5 for testing)
4. Click **Start Scraping**
5. Wait for results (~10 seconds per lead)
6. Click **Download CSV**

---

## 🖥️ Access From Other Devices (Same WiFi)

You can use the scraper from your **phone, tablet, or another laptop** on the same network:

1. Find your PC's local IP:
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.35)

   # Mac/Linux
   ifconfig
   ```

2. Open this URL on any device connected to the same WiFi:
   ```
   http://192.168.1.35:5002
   ```
   *(Replace with your actual IP)*

> **Note:** The scraper must be running on your PC (`python app.py`) for other devices to connect.

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Default search queries (used when no query is entered in the UI)
SEARCH_QUERIES = [
    "Dentist near {city}",
    "Dental clinic near {city}",
]

# Franchise chains to auto-skip
SKIP_KEYWORDS = [
    "Aspen Dental",
    "Heartland Dental",
    # Add more...
]

# Scraping speed (seconds between actions)
ACTION_DELAY_MIN = 2    # Minimum delay
ACTION_DELAY_MAX = 5    # Maximum delay

# Maximum leads per run (overridden by UI slider)
MAX_LEADS_PER_RUN = 100
```

---

## 🗂️ Project Structure

```
GoogleMaps_Lead_Scraper/
├── app.py                    # Flask web server + API endpoints
├── main.py                   # Scraper orchestrator (Maps → Website → CSV)
├── config.py                 # All configurable settings
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container config
│
├── scraper/
│   ├── maps_scraper.py       # Selenium-based Google Maps scraper
│   └── website_scraper.py    # BeautifulSoup website enricher
│
├── utils/
│   ├── file_manager.py       # CSV export & summary generation
│   └── quality_score.py      # Website quality analyzer
│
├── templates/
│   └── index.html            # Web UI (Jinja2 template)
│
├── static/
│   ├── style.css             # Glassmorphic dark theme
│   └── script.js             # Frontend logic
│
└── output/                   # Generated CSV files (git-ignored)
```

---

## 🔧 How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────┐
│  Web UI     │────▶│  Flask API   │────▶│  Maps Scraper   │────▶│  CSV     │
│  (Browser)  │     │  (app.py)    │     │  (Selenium)     │     │  Export  │
└─────────────┘     └──────────────┘     └────────┬────────┘     └──────────┘
                                                  │
                                         ┌────────▼────────┐
                                         │ Website Scraper  │
                                         │ (BeautifulSoup)  │
                                         │ • Emails         │
                                         │ • Phones         │
                                         │ • Social Links   │
                                         │ • Quality Score  │
                                         └─────────────────┘
```

1. **You enter** a city and search query in the web UI
2. **Selenium** opens Google Maps, searches, and clicks each result
3. For each business, it extracts: name, address, phone, website, rating, reviews, category
4. **BeautifulSoup** then visits each business website + its contact/about page
5. It extracts: emails, phone numbers, Instagram, Facebook, LinkedIn, Twitter, TikTok, YouTube, WhatsApp
6. **Quality Score** is calculated based on SSL, mobile-friendliness, modern tech, and copyright year
7. Everything is saved to a **CSV file** and made available for download

---

## ☁️ Why Not Cloud Hosting?

This app uses **Selenium + Chrome** to interact with Google Maps. Google actively blocks headless Chrome from data center IPs (Render, AWS, Vercel, etc.) by showing CAPTCHAs or empty results.

**The scraper must run locally** on a machine with a real Chrome browser. This is by design — local Chrome has a normal IP and browser fingerprint that Google trusts.

| Platform | Works? | Why |
|----------|--------|-----|
| Your PC (local) | ✅ Yes | Real Chrome, residential IP |
| Same WiFi (phone/tablet) | ✅ Yes | Connects to your local server |
| Vercel | ❌ No | Serverless — no Chrome, 10s timeout |
| Render (Docker) | ❌ No | Data center IP blocked by Google |
| AWS/GCP/Azure | ❌ No | Data center IP blocked by Google |

---

## 📝 CLI Mode

You can also run the scraper without the web UI:

```bash
# Basic usage
python main.py --city "New York" --query "Coffee shops" --max-leads 10
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -m 'Add my feature'`)
4. Push (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Scraping Google Maps may violate Google's Terms of Service. Use responsibly and at your own risk. The authors are not responsible for any misuse.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
