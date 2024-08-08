import re
import os
import time
import random
import msvcrt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

# URL of the website
website_url = 'DeviantArtSearchUrl'

# Path to the web driver executable
driver_path = r'path/to/chromedriver.exe'

# Words, phrases, or series of letters to check in the new pages
patterns_to_check = ['Words','to','search']

# Check if the ChromeDriver path is correct
if not os.path.exists(driver_path):
    raise FileNotFoundError(f"ChromeDriver not found at the specified path: {driver_path}")

print("ChromeDriver path verified.")

# Set up Chrome options to use incognito mode and set a user agent
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

print("Chrome options set up.")

# Start a new Chrome session
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def random_sleep(min_sleep=1, max_sleep=3):
    time.sleep(random.uniform(min_sleep, max_sleep))

def search_patterns_in_hrefs(driver):
    try:
        # Wait for the main content to load
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='grid-row']"))
        )

        # Scroll down to ensure all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2, 5)
        driver.execute_script("window.scrollTo(0, 0);")
        random_sleep(2, 5)

        content_rows = driver.find_elements(By.XPATH, "//div[@data-testid='grid-row']")
        print(f"Found {len(content_rows)} content rows.")

        hrefs = []
        for content_row in content_rows:
            links = content_row.find_elements(By.XPATH, ".//div/div/a[@href and @title]")
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href:
                        hrefs.append(href)
                       # print(f"Extracted href: {href}")
                except WebDriverException as e:
                    print(f"Error extracting href: {e}")

        #print(f"Total hrefs collected: {len(hrefs)}")
        if not hrefs:
            print("No hrefs found on this page.")
        else:
            print("Hrefs exist on this page.")

        for href in hrefs:
            #print(f"Opening href: {href}")
            driver.execute_script(f"window.open('{href}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            random_sleep(2, 5)
            
            page_content = driver.page_source
            patterns_found = [pattern for pattern in patterns_to_check if re.search(pattern, page_content, re.IGNORECASE)]
            if patterns_found:
                print(f"Patterns found in {href}: {patterns_found}")
            #else:
            #    print(f"No patterns found in {href}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            random_sleep(1, 3)

    except TimeoutException:
        print("Timeout waiting for content rows.")
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")

def go_to_next_page(driver, page_number):
    try:
        next_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, '_1OGeq') and contains(., 'Next')]"))
        )
        next_href = next_link.get_attribute('href')
        if next_href:
            print(f"Next page {page_number}: {next_href}")

            driver.execute_script(f"window.open('{next_href}', '_blank');")
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            return True
        else:
            print("No href found for the next page.")
            return False
    except TimeoutException:
        print("Next link not found.")
        return False
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
        return False

# Record the start time
start_time = time.time()

try:
    driver.get(website_url)

    page_number = 1
    while True:
        if msvcrt.kbhit() and msvcrt.getch() == b' ':
            print("User requested to end the program.")
            break

        search_patterns_in_hrefs(driver)

        if not go_to_next_page(driver, page_number):
            break
        
        page_number += 1

except WebDriverException as e:
    print(f"Error starting the incognito browser session: {e}")

finally:
    # Close the browser session
    driver.quit()
    print("ChromeDriver session ended.")

    # Record the end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")

