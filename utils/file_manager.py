# utils/file_manager.py
import csv
import os
from datetime import datetime
import config

def setup_output_dir():
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

def save_to_csv(data, filename=None):
    setup_output_dir()
    
    if filename is None:
        filename = config.CSV_FILENAME
        
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    
    # All available columns in the CSV
    headers = [
        "Business Name", "Category", "Website", "Phone", "Email", "Address",
        "City", "Rating", "Reviews",
        "Instagram", "Facebook", "LinkedIn", "Twitter", "TikTok", "YouTube", "WhatsApp",
        "Quality Score", "Notes"
    ]
    
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()
            
        for row in data:
            # Filter row to ensure only valid headers are written
            filtered_row = {k: row.get(k, "") for k in headers}
            writer.writerow(filtered_row)
            
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved {len(data)} leads to {filepath}")

def generate_summary(data):
    total_leads = len(data)
    with_email = len([d for d in data if d.get('Email')])
    with_phone = len([d for d in data if d.get('Phone')])
    with_website = len([d for d in data if d.get('Website')])
    with_socials = len([d for d in data if any(d.get(s) for s in ['Instagram', 'Facebook', 'LinkedIn', 'Twitter'])])
    
    summary = f"""
    --- Scraping Summary ---
    Total Leads Scraped: {total_leads}
    With Email: {with_email}
    With Phone: {with_phone}
    With Website: {with_website}
    With Social Media: {with_socials}
    Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    summary_path = os.path.join(config.OUTPUT_DIR, "summary.txt")
    with open(summary_path, "a") as f:
        f.write(summary + "\n")
        
    return summary
