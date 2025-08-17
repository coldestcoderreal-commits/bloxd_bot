import time
import os
import base64
from threading import Thread, Lock
from flask import Flask
from playwright.sync_api import sync_playwright

# --- Part 1: Web Server and Shared Data ---
latest_screenshot_bytes = None
lock = Lock()
app = Flask(__name__)

@app.route('/')
def health_check_and_screenshot():
    with lock:
        screenshot_data = latest_screenshot_bytes
    
    if screenshot_data:
        b64_image = base64.b64encode(screenshot_data).decode('utf-8')
        html_content = f"""
        <html><head><title>Bloxd.io Bot Status</title><meta http-equiv="refresh" content="15">
            <style>body{{background-color:#121212;color:white;font-family:sans-serif;text-align:center;}} img{{border:2px solid #555;max-width:90%;height:auto;margin-top:20px;}}</style>
        </head><body><h1>Bloxd.io Bot Status</h1><p>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <img src="data:image/png;base64,{b64_image}" alt="Live Screenshot">
        </body></html>"""
        return html_content, 200
    else:
        return """<html><head><title>Bot Starting</title><meta http-equiv="refresh" content="5"></head>
            <body style="background-color:#121212;color:white;font-family:sans-serif;"><h1>Bot is starting up...</h1>
            <p>A screenshot will be available shortly. This page will refresh automatically.</p>
            </body></html>""", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Part 2: Playwright Bot ---
def automate_bloxd():
    global latest_screenshot_bytes
    browser = None # Ensure browser is defined in the outer scope
    try:
        with sync_playwright() as p:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
            page = browser.new_page()

            print("Navigating to https://www.bloxd.io/")
            page.goto("https://www.bloxd.io/", timeout=90000)

            # 1. Reliably handle the main consent pop-up.
            try:
                print("Waiting for the 'Agree' button on the main pop-up (30s timeout)...")
                # This is a very specific selector to avoid ambiguity.
                agree_button_selector = "div.PromptPopupNotificationBody .ButtonBody:has-text('Agree')"
                page.locator(agree_button_selector).click(timeout=30000)
                print("Clicked 'Agree' button successfully.")
            except Exception as e:
                print(f"Warning: Could not click the 'Agree' button. It might not be present. ({e})")
                
            print("Taking a screenshot after handling pop-up...")
            with lock:
                latest_screenshot_bytes = page.screenshot()

            print("Looking for the 'Sandbox Survival' game card...")
            page.locator(".AvailableGameclassicsurvival").click()
            print("Clicked 'Sandbox Survival'.")

            print("Entering lobby name...")
            page.get_by_placeholder("Lobby Name").fill("🩸🩸lifesteal😈")
            print("Lobby name entered.")

            print("Looking for the 'Join' button...")
            page.get_by_role("button", name="Join").click()
            print("Clicked 'Join'. Joining the game...")

            print("Waiting 10 seconds for the game to fully load...")
            time.sleep(10)

            print("Activating game window and typing message...")
            page.keyboard.press("Enter")
            time.sleep(1)
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

            print("In-game. Starting screenshot loop.")
            # Loop to keep taking screenshots
            while True:
                with lock:
                    latest_screenshot_bytes = page.screenshot()
                time.sleep(30)
                print("Updated screenshot.")

    except Exception as e:
        print(f"An error occurred in the main automation flow: {e}")
        # On ANY error, take a screenshot so we can see what went wrong.
        if 'page' in locals():
            print("Attempting to take error screenshot...")
            with lock:
                latest_screenshot_bytes = page.screenshot()
            print("Error screenshot captured.")
    
    finally:
        if browser:
            browser.close()
        print("Automation script has finished.")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    automate_bloxd()
