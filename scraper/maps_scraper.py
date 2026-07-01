# -*- coding: utf-8 -*-
# scraper/maps_scraper.py
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import config

class MapsScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        
        # Stealth options — hide automation signals
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        
        # Container/Server options (always apply for stability)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--lang=en-US")
        
        # Headless mode for deployment
        if os.environ.get("HEADLESS") == "true":
            options.add_argument("--headless=new")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--blink-settings=imagesEnabled=false")
            # Use /tmp for user data on containers to avoid /dev/shm issues
            options.add_argument("--user-data-dir=/tmp/chrome-user-data")
            options.add_argument("--disk-cache-dir=/tmp/chrome-cache")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self._search_success = False

    def _dismiss_consent(self):
        """Dismiss Google cookie consent page that appears on data center IPs."""
        try:
            # Look for common consent button texts
            consent_selectors = [
                # "Accept all" button (English)
                '//button[contains(text(), "Accept all")]',
                '//button[contains(text(), "Accept")]',
                '//button[contains(text(), "Reject all")]',
                # Consent form buttons by aria-label
                '//button[@aria-label="Accept all"]',
                '//button[@aria-label="Accept cookies"]',
                # Google's consent form specific
                '//form[@action="https://consent.google.com/save"]//button',
                # Material-design styled buttons
                '//button[contains(@class, "tHlp8d")]',
            ]
            
            for xpath in consent_selectors:
                try:
                    btn = self.driver.find_element(By.XPATH, xpath)
                    if btn.is_displayed():
                        btn.click()
                        print("  [Consent] Dismissed cookie consent banner")
                        time.sleep(2)
                        return True
                except:
                    continue
            
            # Also try CSS selectors for consent
            css_selectors = [
                'button#L2AGLb',           # Google "I agree" button
                'button[jsname="b3VHJd"]', # Another Google consent button
                '[aria-label="Accept all"]',
            ]
            for selector in css_selectors:
                try:
                    btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if btn.is_displayed():
                        btn.click()
                        print("  [Consent] Dismissed cookie consent banner (CSS)")
                        time.sleep(2)
                        return True
                except:
                    continue
                    
        except Exception as e:
            print(f"  [Consent] No consent banner found or error: {e}")
        
        return False

    def search(self, query):
        # Use consent-bypass parameters
        maps_url = 'https://www.google.com/maps?hl=en&consent=1'
        print(f"  [Nav] Opening Google Maps...")
        self.driver.get(maps_url)
        time.sleep(5)
        
        # Try to dismiss consent banner if present
        self._dismiss_consent()
        time.sleep(1)
        
        # If we got redirected to consent page, try direct Maps search URL instead
        current_url = self.driver.current_url
        if 'consent' in current_url.lower() or 'accounts.google' in current_url.lower():
            print("  [Nav] Consent redirect detected, trying direct search URL...")
            # Use the direct Maps search URL which sometimes bypasses consent
            direct_url = f'https://www.google.com/maps/search/{query.replace(" ", "+")}?hl=en'
            self.driver.get(direct_url)
            time.sleep(5)
            self._dismiss_consent()
            time.sleep(2)
            
            # Check if results loaded directly
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                print(f"  [Nav] Direct search worked! Results loaded for: {query}")
                self._search_success = True
                return
            except:
                pass
        
        # Find and use the search box
        selectors = [
            (By.ID, "searchboxinput"),
            (By.NAME, "q"),
            (By.CSS_SELECTOR, "input#searchboxinput"),
            (By.XPATH, "//input[@id='searchboxinput']"),
            (By.CSS_SELECTOR, "input[aria-label='Search Google Maps']")
        ]
        
        search_box_input = None
        for by, value in selectors:
            try:
                element = self.driver.find_element(by, value)
                if element.is_displayed():
                    search_box_input = element
                    print(f"  [Search] Found search box using {by}={value}")
                    break
            except:
                continue
                
        if not search_box_input:
            # Last resort: try direct search URL
            print("  [Search] Search box not found. Trying direct URL search...")
            direct_url = f'https://www.google.com/maps/search/{query.replace(" ", "+")}?hl=en'
            self.driver.get(direct_url)
            time.sleep(8)
            self._dismiss_consent()
            time.sleep(2)
            
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                print(f"  [Search] Direct URL search succeeded for: {query}")
                self._search_success = True
                return
            except:
                # Save debug info
                print("  [Search] FAILED - Could not load results. Saving debug info...")
                try:
                    self.driver.save_screenshot("output/debug_screenshot.png")
                    with open("output/debug_page.html", "w", encoding="utf-8") as f:
                        f.write(self.driver.page_source)
                    print(f"  [Debug] Screenshot saved. Current URL: {self.driver.current_url}")
                    print(f"  [Debug] Page title: {self.driver.title}")
                except Exception as e:
                    print(f"  [Debug] Failed to save debug info: {e}")
                self._search_success = False
                return

        try:
            search_box_input.clear()
            search_box_input.send_keys(query)
            time.sleep(1)
            search_box_input.send_keys(Keys.ENTER)
            print(f"  [Search] Searching for: {query}")
            self._search_success = True
        except Exception as e:
            print(f"  [Search] Error interacting with search box: {e}")
            self._search_success = False
            return
            
        time.sleep(random.uniform(4, 6))

    def get_leads(self):
        """
        Scrolls the results list and collects details for up to MAX_LEADS_PER_RUN.
        """
        leads = []
        processed_names = set()
        
        # Guard: if search() failed, don't attempt to scrape
        if not self._search_success:
            print("Search was not successful. Skipping lead extraction.")
            return leads
        
        try:
            # Locate the scrollable feed
            # Usually strict role="feed"
            feed = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
        except:
            print("Could not find results feed.")
            return leads

        # Scroll loop with empty-scroll safety limit
        empty_scroll_count = 0
        max_empty_scrolls = 5
        
        while len(leads) < config.MAX_LEADS_PER_RUN:
            # Check stop flag
            if config.STOP_SCRAPING:
                print(">> STOP REQUESTED. Finishing current batch and exiting...")
                break
            
            # Re-find all items FRESH each iteration to avoid stale references
            try:
                items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[role="article"]')
            except Exception:
                items = []
            
            # Find the FIRST unprocessed item (one at a time to avoid stale refs)
            target_item = None
            target_name = None
            for item in items:
                try:
                    aria_label = item.get_attribute("aria-label")
                    if aria_label and aria_label not in processed_names:
                        target_item = item
                        target_name = aria_label
                        break
                except StaleElementReferenceException:
                    continue
                except Exception:
                    continue

            if not target_item:
                empty_scroll_count += 1
                if empty_scroll_count >= max_empty_scrolls:
                    print("No new results after multiple scrolls. Reached end of list.")
                    break
                # Scroll down to load more results
                try:
                    feed = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                    self.driver.execute_script("arguments[0].scrollBy(0, 1000);", feed)
                except Exception:
                    pass
                time.sleep(random.uniform(2, 4))
                continue
            
            # Reset counter when we find a new item
            empty_scroll_count = 0
            
            # Process this single item
            try:
                print(f"Processing: {target_name}")
                target_item.click()
                
                # Wait for the detail panel to fully load
                # The detail panel is loaded when the address or phone button appears
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 
                            'button[data-item-id="address"], button[data-item-id^="phone"], a[data-item-id="authority"]'))
                    )
                except:
                    pass  # Continue anyway, some businesses may not have these
                
                # Extra delay to let all detail fields render
                time.sleep(random.uniform(config.ACTION_DELAY_MIN, config.ACTION_DELAY_MAX))
                
                details = self.extract_details()
                details["Business Name"] = target_name
                
                leads.append(details)
                processed_names.add(target_name)
                print(f"  [OK] Scraped lead {len(leads)}/{config.MAX_LEADS_PER_RUN}: {target_name}")
                print(f"       Phone: {details.get('Phone', 'N/A')} | Website: {'Yes' if details.get('Website') else 'No'} | Rating: {details.get('Rating', 'N/A')}")
                
            except StaleElementReferenceException:
                print(f"Stale element for '{target_name}', skipping.")
                processed_names.add(target_name)
            except Exception as e:
                print(f"Error processing '{target_name}': {e}")
                processed_names.add(target_name)

            # === NAVIGATE BACK to the results list ===
            self._go_back_to_results()
            # Wait for the results list to fully re-render
            time.sleep(random.uniform(2, 3.5))

        return leads

    def extract_details(self):
        details = {
            "Business Name": "",
            "Rating": "",
            "Reviews": "",
            "Address": "",
            "Website": "",
            "Phone": "",
            "Category": "",
            "Socials": {} 
        }
        
        def safe_get_text(selector):
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, selector)
                return el.text
            except:
                return ""

        def safe_get_attr(selector, attr):
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, selector)
                return el.get_attribute(attr)
            except:
                return ""

        # Website
        website_url = safe_get_attr('a[data-item-id="authority"]', 'href')
        if not website_url:
             website_url = safe_get_attr('a[aria-label^="Website:"]', 'href')
        details["Website"] = website_url

        # Phone
        phone = safe_get_text('button[data-item-id^="phone"]')
        if not phone:
             phone = safe_get_attr('button[data-item-id^="phone"]', 'aria-label')
        
        if phone:
            phone = phone.replace("Phone: ", "")
            phone = "".join([c for c in phone if c.isascii()]).strip()
        else:
            phone = ""
            
        details["Phone"] = phone

        # Address
        address = safe_get_text('button[data-item-id="address"]')
        if not address:
             address = safe_get_attr('button[data-item-id="address"]', 'aria-label')
        details["Address"] = address.replace("Address: ", "") if address else ""

        # Category - usually shown as a button/link near the business name
        try:
            # Try the category button (common in Maps detail view)
            category_el = self.driver.find_element(By.CSS_SELECTOR, 'button[jsaction*="category"]')
            details["Category"] = category_el.text.strip()
        except:
            try:
                # Fallback: look for the category link
                cat_els = self.driver.find_elements(By.CSS_SELECTOR, 'button.DkEaL')
                if cat_els:
                    details["Category"] = cat_els[0].text.strip()
            except:
                pass

        # Rating & Reviews
        try:
             rating_el = self.driver.find_element(By.XPATH, '//span[@role="img" and contains(@aria-label, "stars")]')
             rating_text = rating_el.get_attribute("aria-label")
             if rating_text:
                 # Format: "4.5 stars 123 Reviews" or similar
                 parts = rating_text.split()
                 details["Rating"] = parts[0]
        except:
            pass
        
        # Reviews count - try dedicated reviews button/text
        try:
            reviews_text = safe_get_attr('button[jsaction*="reviews"]', 'aria-label')
            if reviews_text:
                # Extract number from text like "123 reviews"
                import re
                nums = re.findall(r'[\d,]+', reviews_text)
                if nums:
                    details["Reviews"] = nums[0].replace(",", "")
            
            if not details["Reviews"]:
                # Fallback: look for review count in the rating area
                review_els = self.driver.find_elements(By.CSS_SELECTOR, 'span[aria-label*="review"]')
                for el in review_els:
                    text = el.get_attribute("aria-label") or el.text
                    import re
                    nums = re.findall(r'[\d,]+', text)
                    if nums:
                        details["Reviews"] = nums[0].replace(",", "")
                        break
        except:
            pass
            
        return details

    def _go_back_to_results(self):
        """Navigate back from detail panel to the results list."""
        try:
            # Method 1: Click the back button in the Google Maps UI
            back_selectors = [
                'button[aria-label="Back"]',
                'button[jsaction*="back"]',
                'button.hYkMUe',  # Common Maps back button class
            ]
            
            for selector in back_selectors:
                try:
                    back_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if back_btn.is_displayed():
                        back_btn.click()
                        print("  ← Navigated back to results list")
                        # Wait for the feed to reappear
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                            )
                        except:
                            pass
                        return
                except:
                    continue
            
            # Method 2: Use browser back
            self.driver.back()
            print("  ← Used browser back to return to results")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
            except:
                pass
                
        except Exception as e:
            print(f"  Warning: Could not navigate back: {e}")

    def close(self):
        try:
            self.driver.quit()
        except:
            pass
