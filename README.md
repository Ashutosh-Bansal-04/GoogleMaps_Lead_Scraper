# 🗺️ Google Maps Lead Scraper

An autonomous lead generation tool that scrapes Google Maps for business listings, enriches them with website data (emails, social links, quality scores), and exports clean CSV files.

## ✨ Features

- **Google Maps Scraping** — Searches Google Maps and extracts business name, phone, address, rating, and website
- **Website Enrichment** — Visits each business website to extract emails, phone numbers, and social media links
- **Quality Scoring** — Rates each lead (SSL, mobile-friendly, modern tech stack, copyright year)
- **Smart Filtering** — Skips franchise chains and low-quality leads automatically
- **Web UI** — Clean, modern interface to run scrapes from the browser
- **CLI Mode** — Run scrapes directly from the command line
- **CSV Export** — Download results as a clean CSV file
- **Stop Control** — Gracefully stop a running scrape from the UI

## 📁 Project Structure

```
├── app.py                  # Flask web server
├── main.py                 # Core scraper orchestration + CLI entry point
├── config.py               # Search queries, filters, and settings
├── scraper/
│   ├── maps_scraper.py     # Selenium-based Google Maps scraper
│   └── website_scraper.py  # Website data extraction (emails, socials)
├── utils/
│   ├── file_manager.py     # CSV export and summary generation
│   └── quality_score.py    # Website quality analysis
├── templates/
│   └── index.html          # Web UI template
├── static/
│   ├── style.css           # UI styles
│   └── script.js           # Frontend logic
├── Dockerfile              # Docker config for cloud deployment
├── vercel.json             # Vercel deployment config
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Google Chrome installed

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/GoogleMaps-Lead-Scraper.git
cd GoogleMaps-Lead-Scraper

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Web Interface

```bash
python app.py
```

Open [http://127.0.0.1:5002](http://127.0.0.1:5002) in your browser.

#### Command Line

```bash
# Basic usage
python main.py --city "New York"

# Custom query
python main.py --city "San Francisco" --query "Coffee shops"

# Limit results
python main.py --city "Austin" --query "Dentist" --max-leads 5
```

## ⚙️ Configuration

Edit `config.py` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `SEARCH_QUERIES` | Default search templates | Dentist queries |
| `SKIP_KEYWORDS` | Franchise names to skip | Major dental chains |
| `MAX_LEADS_PER_RUN` | Max leads per scrape | 100 |
| `SCROLL_PAUSE_TIME` | Pause between scrolls (seconds) | 2 |

## 🌐 Deployment

### Vercel (Web UI Only)

> **Note:** Vercel's serverless environment does not support Selenium/Chrome. The web UI will deploy, but scraping routes require a Docker-capable platform.

```bash
vercel deploy
```

### Docker (Full Functionality)

```bash
docker build -t maps-scraper .
docker run -p 5000:5000 maps-scraper
```

### Render / Railway (Recommended for Full Deployment)

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

## 📊 Output

Scraped leads are saved as CSV files in the `output/` directory with the following columns:

| Column | Description |
|--------|-------------|
| Business Name | Name from Google Maps |
| Website | Business website URL |
| Phone | Phone number(s) |
| Email | Email address(es) from website |
| Instagram / Facebook / LinkedIn | Social media links |
| Rating | Google Maps rating |
| Quality Score | 0 (modern) to 10 (no website) |
| Notes | Additional observations |

## 📄 License

This project is for educational purposes. Please respect Google's Terms of Service and robots.txt when scraping.
