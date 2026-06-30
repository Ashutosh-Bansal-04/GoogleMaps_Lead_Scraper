# Deployment Guide

This guide explains how to deploy the Maps Lead Scraper to a cloud platform and how to run it locally.

## Option 1: Render (Recommended for Free Tier)
Render offers a free tier for web services and makes it easy to deploy Dockerized apps.

1.  **Push to GitHub**:
    - Initialize a git repo (if you haven't): `git init`
    - Add files: `git add .`
    - Commit: `git commit -m "Initial commit"`
    - Push to a new GitHub repository.

2.  **Create New Web Service on Render**:
    - Go to [dashboard.render.com](https://dashboard.render.com/).
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.

3.  **Configure**:
    - **Name**: `maps-scraper` (or similar)
    - **Runtime**: `Docker`
    - **Region**: Choose one close to you.
    - **Instance Type**: **Free** (Note: Free tier spins down after inactivity).

4.  **Environment Variables**:
    - Add the following variables under "Environment":
        - `HEADLESS`: `true`
        - `PYTHONUNBUFFERED`: `1`

5.  **Deploy**:
    - Click **Create Web Service**.
    - Render will automatically build the Docker image. This may take 5-10 minutes as it installs Chrome and dependencies.

## Option 2: Railway
Railway is another excellent option with a slightly different pricing model (trial credits).

1.  **Deploy from GitHub**:
    - Go to [railway.app](https://railway.app/).
    - Click **New Project** -> **Deploy from GitHub repo**.
    - Select your repository.
2.  **Variables**:
    - Go to the **Variables** tab.
    - Add `HEADLESS=true`.
3.  **Domain**:
    - Railway automatically generates a domain for you.

## Local Execution (Testing)

You can run the scraper locally without Docker if you have Python installed.

### Prerequisites
- Python 3.9+
- Google Chrome installed

### Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Web Interface**:
    ```bash
    python app.py
    ```
    Then open [http://127.0.0.1:5002](http://127.0.0.1:5002) in your browser.

3.  **Run via CLI (Command Line)**:
    You can run the scraper directly from the terminal.
    ```bash
    # Basic usage
    python main.py --city "New York" --query "Dentist"
    
    # Limit number of leads (Good for testing)
    python main.py --city "New York" --query "Dentist" --max-leads 3
    ```

## Notes & Troubleshooting
- **Performance**: Scraping uses a significant amount of RAM. On free tiers (like Render's 512MB RAM), the app might crash if you try to scrape too many leads or if Chrome consumes too much memory.
    - **Solution**: Keep default `MAX_LEADS` low (e.g., 20) or use the `--max-leads` argument to limit it.
- **Storage**: The generated CSV files are stored in the container's ephemeral file system on platforms like Render. They will disappear if the app restarts.
    - **Solution**: Download your leads immediately after scraping.
- **Timeouts**: Cloud providers often have timeout limits (Render Free Tier: 100 seconds for HTTP requests).
    - **Solution**: The scraping process is blocking. For large scrapes, you might hit a timeout error 504. The scraping *might* continue in the background, but the web request will fail. For production use, this should be refactored to use a task queue (like Celery/Redis).
