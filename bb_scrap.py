# Import the libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import random

# Ensure the "data" folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Setup WebDriver
try:
    driver = webdriver.Chrome()
    print("[INFO] WebDriver initialized successfully.")
except Exception as e:
    print(f"[ERROR] Error initializing WebDriver: {e}")
    exit()

query = "ready to eat"
file = 0
max_retries = 3  # Maximum number of retries
retry_delay = random.uniform(5, 10)  # Random delay between retries


for i in range(1,10):
    attempt = 0
    success = False

    while attempt < max_retries and not success:
        try:
            url = f"https://www.bigbasket.com/ps/?q={query}&nc=as&page={i}"
            driver.get(url)
            time.sleep(3)  # Allow time for the page to load
            print("[INFO] Page loaded successfully.")

            # Scroll to load more items
            for _ in range(3):  
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)

            # Find product elements
            elems = driver.find_elements(By.CLASS_NAME, "SKUDeck___StyledDiv-sc-1e5d9gk-0")  
            print(f"[INFO] {len(elems)} products found.")

            for elem in elems:
                d = elem.get_attribute("outerHTML")

                with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
                    f.write(d)

                file += 1
                print(f"[INFO] Saved: data/{query}_{file}.html")

            success = True  # Mark as successful if no errors occur

        except Exception as e:
            attempt += 1
            print(f"[ERROR] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay:.2f} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached.")

# Close WebDriver
try:
    driver.quit()
    print("[INFO] WebDriver closed successfully.")
except Exception as e:
    print(f"[ERROR] Error closing WebDriver: {e}")
