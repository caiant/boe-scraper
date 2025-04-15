import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import pandas as pd

def capture_screenshot_and_rate():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the driver (GitHub Actions has Chrome pre-installed)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Bank of England homepage
        driver.get("https://www.bankofengland.co.uk")
        time.sleep(5)
        
        # Create directory for screenshots
        os.makedirs("boe_screenshots", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"boe_screenshots/boe_{timestamp}.png"
        
        # Take screenshot
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Scrape the bank rate
        try:
            rate_element = driver.find_element(By.CSS_SELECTOR, "div.bank-rate__rate")
            current_rate = rate_element.text.strip()
            
            # Save to CSV
            data = {
                'date': [datetime.now().strftime("%Y-%m-%d")],
                'time': [datetime.now().strftime("%H:%M:%S")],
                'bank_rate': [current_rate]
            }
            
            df = pd.DataFrame(data)
            
            # Append to existing CSV or create new
            if os.path.exists('boe_rates.csv'):
                df.to_csv('boe_rates.csv', mode='a', header=False, index=False)
            else:
                df.to_csv('boe_rates.csv', index=False)
                
            print(f"Bank rate recorded: {current_rate}")
            
        except Exception as e:
            print(f"Error scraping bank rate: {e}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_screenshot_and_rate()
