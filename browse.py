import time
import os
from threading import Thread
from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running.", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def automate_bloxd():
    with sync_playwright() as p:
        try:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Navigating to https://www.bloxd.io/...")
            page.goto("https://www.bloxd.io/", timeout=60000)

            print("Looking for the 'Agree' button...")
            page.get_by_role("button", name="Agree").click()
            print("Clicked 'Agree'.")

            print("Looking for the 'Sandbox Survival' game card...")
            page.locator(".AvailableGameclassicsurvival").click()
            print("Clicked 'Sandbox Survival'.")

            print("Entering lobby name...")
            page.get_by_placeholder("Lobby Name").fill("🩸🩸lifesteal😈")
            print("Lobby name entered.")

            print("Looking for the 'Join' button...")
            page.get_by_role("button", name="Join").click()
            print("Clicked 'Join'. Joining the game...")

            print("Waiting 5 seconds for the game to load...")
            time.sleep(5)

            print("Activating game window and typing message...")
            page.keyboard.press("Enter")
            time.sleep(1)
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            print("Automation script has finished its tasks.")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    automate_bloxd()
    
    print("Container will now idle.")
    while True:
        time.sleep(60)
