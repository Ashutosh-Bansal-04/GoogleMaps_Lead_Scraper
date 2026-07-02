# Deployment Guide — Host on Render (Free)

## Why Render and NOT Vercel?

This app uses **Selenium + Chrome** to scrape Google Maps. Vercel is serverless (no browser, 10s timeout) — it physically cannot run this app. **Render** supports Docker (free tier), which lets you run Chrome in a container.

| Feature | Vercel | Render |
|---------|--------|--------|
| Docker support | No | Yes |
| Chrome/Selenium | No | Yes |
| Request timeout | 10s (free) / 60s (pro) | 600s+ |
| Free tier | Yes (but useless for this) | Yes |
| Custom domain | Yes | Yes |

---

## Step 1: Push to GitHub

Open a terminal in `D:\GoogleMaps_Lead_Scraper` and run:

```bash
# Initialize git (skip if already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Maps Lead Scraper"

# Create a repo on GitHub (go to github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/GoogleMaps-Lead-Scraper.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render

### 2.1 — Create Render Account
1. Go to [render.com](https://render.com) and sign up (free)
2. Connect your GitHub account

### 2.2 — Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Connect your `GoogleMaps-Lead-Scraper` repo
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `maps-lead-scraper` |
| **Region** | Pick closest to you |
| **Runtime** | **Docker** |
| **Instance Type** | **Free** |

5. Click **"Deploy Web Service"**

### 2.3 — Wait for Build
- The first build takes **5-10 minutes** (it downloads Chrome + Python packages)
- You'll see a live build log
- When it says **"Your service is live"**, you're done!

### 2.4 — Access Your App
Your app will be live at:
```
https://maps-lead-scraper.onrender.com
```
You can access this URL from **any device** (phone, tablet, laptop) — anywhere in the world.

---

## Step 3: Use the App

1. Open `https://maps-lead-scraper.onrender.com` on any device
2. Enter a city (e.g., "New York")
3. Enter a search query (e.g., "Coffee shops")
4. Set max leads (start with 5 for testing)
5. Click **Start Scraping**
6. Wait for it to finish (takes ~1 min per lead)
7. Click **Download CSV** to get your leads file

---

## Important Notes

### Free Tier Limitations
- Render's free tier **spins down after 15 min of inactivity**
- First request after sleep takes ~30s to wake up
- For always-on, upgrade to Render's **Starter plan** ($7/month)

### Scraping Speed
- Each lead takes ~8-15 seconds (click → extract → go back)
- 5 leads ≈ 1-2 minutes
- 20 leads ≈ 5-8 minutes
- Website enrichment adds ~2-3 seconds per lead

### If Scraping Fails on Render
Google may block headless Chrome in some data centers. If you get 0 results:
1. Try a different Render region
2. Or run locally: `python app.py` and use from your own PC

---

## Updating the App

After making code changes:

```bash
git add .
git commit -m "Your change description"
git push
```

Render auto-deploys on every push to `main`.

---

## Project Structure

```
GoogleMaps_Lead_Scraper/
├── app.py                  # Flask web server
├── main.py                 # Scraper orchestrator
├── config.py               # Settings (queries, delays, etc.)
├── Dockerfile              # Container config for Render
├── requirements.txt        # Python dependencies
├── scraper/
│   ├── __init__.py
│   ├── maps_scraper.py     # Selenium Google Maps scraper
│   └── website_scraper.py  # BeautifulSoup website enricher
├── utils/
│   ├── __init__.py
│   ├── file_manager.py     # CSV export
│   └── quality_score.py    # Website quality analyzer
├── templates/
│   └── index.html          # Web UI template
├── static/
│   ├── style.css           # UI styling
│   └── script.js           # Frontend logic
└── output/                 # Generated CSV files
```
