from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def open_website(url):
    """
    Opens a website in a headless Chrome browser.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None  # Initialize driver to None
    try:
        print(f"Navigating to {url}...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        print(f"Successfully opened: {driver.title}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    website_url = "https://www.bloxd.io/"
    open_website(website_url)
