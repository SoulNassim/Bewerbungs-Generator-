#!/usr/bin/env python3
"""
Capture screenshots of the Applify app for documentation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os

# Screenshots directory
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Initialize driver
try:
    driver = webdriver.Chrome(options=chrome_options)
    print("✓ Chrome driver started")
except Exception as e:
    print(f"✗ Failed to start Chrome driver: {e}")
    print("  Make sure ChromeDriver is installed and in PATH")
    exit(1)

try:
    # Navigate to app
    driver.get("http://localhost:5000")
    print("✓ Opened http://localhost:5000")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    time.sleep(2)  # Extra time for animations
    
    # Screenshot 1: Firma tab (should already be visible)
    screenshot1_path = os.path.join(SCREENSHOTS_DIR, "applify-firma.jpg")
    driver.save_screenshot(screenshot1_path)
    print(f"✓ Saved: {screenshot1_path}")
    
    # Click on Tools tab
    tools_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Tools')]")
    tools_tab.click()
    time.sleep(1)
    print("✓ Clicked Tools tab")
    
    # Screenshot 2: Tools tab
    screenshot2_path = os.path.join(SCREENSHOTS_DIR, "applify-tools.jpg")
    driver.save_screenshot(screenshot2_path)
    print(f"✓ Saved: {screenshot2_path}")
    
    print("\n✓ All screenshots captured successfully!")
    
except Exception as e:
    print(f"✗ Error capturing screenshots: {e}")
    
finally:
    driver.quit()
    print("✓ Chrome driver closed")
