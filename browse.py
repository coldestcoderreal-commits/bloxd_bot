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
        </head><body><h1>Bloxd.io Bot Status</h1><p>Screenshot taken at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>The bot is now paused.</p>
            <img src="data:image/png;base64,{b64_image}" alt="Live Screenshot">
        </body></html>"""
        return html_content, 200
    else:
        return """<html><head><title>Bot Starting</title><meta http-equiv="refresh" content="5"></head>
            <body style="background-color:#121212;color:white;font-family:sans-serif;"><h1>Bot is starting up...</h1>
            <p>Waiting for the bot to take a screenshot. This page will refresh automatically.</p>
            </body></html>""", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Part 2: Playwright Bot ---
def run_bot():
    global latest_screenshot_bytes
    browser = None
    page = None # Define page in the outer scope for the final error handler
    
    try:
        with sync_playwright() as p:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Navigating to https://bloxd.io/")
            page.goto("https://bloxd.io/", timeout=90000, wait_until="domcontentloaded")
            
            try:
                print("Looking for the 'Agree' button on the privacy pop-up...")
                agree_button_selector = "div.PromptPopupNotificationBody .ButtonBody:has-text('Agree')"
                # Wait for the button to be visible before clicking
                page.wait_for_selector(agree_button_selector, state='visible', timeout=30000)
                page.locator(agree_button_selector).click()
                print("Successfully clicked the 'Agree' button.")
            except Exception as e:
                print(f"Warning: Could not click the 'Agree' button. It might not have appeared. Error: {e}")

            # --- NEW, MORE ROBUST ACTION STEPS ---
            game_card_selector = ".AvailableGameclassicsurvival"
            
            print(f"Waiting for game card '{game_card_selector}' to be visible...")
            # Wait until the element is actually visible on the page
            page.wait_for_selector(game_card_selector, state='visible', timeout=30000)

            print("Taking a screenshot before clicking the game card...")
            with lock:
                latest_screenshot_bytes = page.screenshot(timeout=10000)

            print("Clicking 'Sandbox Survival' game card...")
            page.locator(game_card_selector).click()
            print("Successfully clicked 'Sandbox Survival'.")
            
            print("Waiting 5 seconds for the lobby screen to appear...")
            time.sleep(5)

            print("Taking final screenshot...")
            with lock:
                latest_screenshot_bytes = page.screenshot(timeout=10000)
            
            print("Screenshot captured. The bot is now paused with the browser open.")

            while True:
                time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")
        if page and not page.is_closed():
            print("Attempting to take error screenshot...")
            with lock:
                latest_screenshot_bytes = page.screenshot(timeout=10000)
            print("Error screenshot captured.")
        
        print("An error occurred, but the container will continue to idle.")
        while True:
            time.sleep(60)


if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    run_bot()
