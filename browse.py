import time
from playwright.sync_api import sync_playwright

def automate_bloxd():
    """
    Automates a sequence of actions on bloxd.io using Playwright.
    """
    with sync_playwright() as p:
        try:
            print("Initializing the browser...")
            # Launch a headless Chromium browser instance
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Go to the website
            print("Navigating to https://www.bloxd.io/...")
            page.goto("https://www.bloxd.io/", timeout=60000)

            # 1. Click the "Agree" button
            print("Looking for the 'Agree' button...")
            page.get_by_role("button", name="Agree").click()
            print("Clicked 'Agree'.")

            # 2. Click the "Sandbox Survival" game card
            print("Looking for the 'Sandbox Survival' game card...")
            page.locator(".AvailableGameclassicsurvival").click()
            print("Clicked 'Sandbox Survival'.")

            # 3. Enter the lobby name
            print("Entering lobby name...")
            page.get_by_placeholder("Lobby Name").fill("🩸🩸lifesteal😈")
            print("Lobby name entered.")

            # 4. Click the "Join" button
            print("Looking for the 'Join' button...")
            page.get_by_role("button", name="Join").click()
            print("Clicked 'Join'. Joining the game...")

            # 5. Wait for the game to load and interact
            print("Waiting 5 seconds for the game to load...")
            time.sleep(5)

            print("Activating game window and typing message...")
            page.keyboard.press("Enter")
            time.sleep(1) # A small pause for the chat box to appear
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            print("Automation script has finished its tasks.")

if __name__ == "__main__":
    automate_bloxd()
    
    # Keep the container running for Render's background worker
    print("Container will now idle.")
    while True:
        time.sleep(60)
