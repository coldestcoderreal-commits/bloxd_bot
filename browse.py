import time
from playwright.sync_api import sync_playwright

def run_bot():
    """
    Navigates to bloxd.io, takes a screenshot, and then idles.
    """
    browser = None
    try:
        with sync_playwright() as p:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Navigating to https://bloxd.io/")
            # Wait up to 90 seconds for the page to finish loading
            page.goto("https://bloxd.io/", timeout=90000, wait_until="load")

            print("Page loaded. Waiting 10 seconds for elements to render...")
            time.sleep(10)

            # Take a screenshot and save it inside the container
            screenshot_path = "status.png"
            page.screenshot(path=screenshot_path)
            
            print(f"Screenshot successfully saved to '{screenshot_path}' inside the container.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if browser:
            browser.close()
        print("Browser session closed.")


if __name__ == "__main__":
    run_bot()
    
    # Keep the container running so you can check the logs.
    print("Bot has finished its task. Container will now idle.")
    while True:
        time.sleep(60)
