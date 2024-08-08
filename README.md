# AutomaticDeviantArtSearch

This Python script automates the process of navigating through DeviantArt search result pages, extracting URL of the results from each page, and checking for specific patterns within the content of those URL pages. The script uses Selenium WebDriver to interact with the website and handle the browser automation tasks.

Features
Automated Navigation: The script automatically navigates through multiple pages of search results on DeviantArt.
Pattern Matching: Extracted URLs are checked for specific patterns (words, phrases, or series of letters) within their content.
Incognito Mode: The script uses Chrome's incognito mode to prevent any browser history or cookies from being saved.
Randomized Delays: Random sleep intervals are used to mimic human behavior and reduce the chances of getting blocked.
Prerequisites
Python 3.x
Selenium: Install using pip install selenium.
ChromeDriver: Download and place the chromedriver.exe file in the specified directory. Ensure the version matches your installed Chrome browser version.
Google Chrome: Ensure Google Chrome is installed on your system.
