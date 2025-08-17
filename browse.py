import time
import os
import base64
from threading import Thread, Lock
from flask import Flask
from playwright.sync_api import sync_playwright

# --- Part 1: Web Server and Shared Data ---

# Global variable to hold the latest screenshot bytes, with a lock for thread safety
latest_screenshot_bytes = None
lock = Lock()

app = Flask(__name__)

@app.route('/')
def health_check_and_screenshot():
    """
    This route now serves an HTML page that displays the latest screenshot.
    The page will auto-refresh every 15 seconds.
    """
    with lock:
        screenshot_data = latest_screenshot_bytes
    
    if screenshot_data:
        # Encode the bytes to a Base64 string to embed in HTML
        b64_image = base64.b64encode(screenshot_data).decode('utf-8')
        html_content = f"""
        <html>
            <head>
                <title>Bloxd.io Bot Status</title>
                <meta http-equiv="refresh" content="15">
                <style>
                    body {{ background-color: #121212; color: white; font-family: sans-serif; text-align: center; }}
                    img {{ border: 2px solid #555; max-width: 90%; height: auto; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <h1>Bloxd.io Bot Status</h1>
                <p>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <img src="data:image/png;base64,{b64_image}" alt="Live Screenshot">
            </body>
        </html>
        """
        return html_content, 200
    else:
        # If no screenshot is available yet
        return """
        <html>
            <head><title>Bot Starting</title><meta http-equiv="refresh" content="5"></head>
            <body style="background-color: #121212; color: white; font-family: sans-serif;">
                <h1>Bot is starting up...</h1>
                <p>A screenshot will be available shortly. This page will refresh automatically.</p>
            </body>
        </html>
        """, 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Part 2: Playwright Bot ---
def automate_bloxd():
    global latest_screenshot_bytes
    
    with sync_playwright() as p:
        try:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
            page = browser.new_page()

            print("Navigating to https://www.bloxd.io/")
            page.goto("https://www.bloxd.io/", timeout=90000)

            # Resilient pop-up handling
            try:
                print("Attempt 1: Clicking 'Agree' in Google consent iframe (5s timeout)...")
                consent_frame = page.frame_locator('iframe[name="googlefcPresent"]')
                consent_frame.get_by_text("Agree").click(timeout=5000)
                print("Clicked 'Agree' in Google iframe.")
            except Exception:
                print("Info: Google iframe not found or timed out.")
                print("Attempt 2: Clicking 'Agree' on the main page (5s timeout)...")
                try:
                    page.get_by_role("button", name="Agree").click(timeout=5000)
                    print("Clicked 'Agree' on the main page.")
                except Exception:
                    print("Info: No consent button found, continuing.")

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

            # Take the first screenshot
            print("Taking initial screenshot...")
            with lock:
                latest_screenshot_bytes = page.screenshot()

            # Loop to keep taking screenshots
            while True:
                time.sleep(30)
                print("Taking updated screenshot...")
                with lock:
                    latest_screenshot_bytes = page.screenshot()

        except Exception as e:
            print(f"An error occurred in the main automation flow: {e}")
        
        finally:
            print("Automation script has finished.")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    automate_bloxd()
