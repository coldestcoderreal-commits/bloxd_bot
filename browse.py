import time
import os
import base64
from threading import Thread, Lock
from flask import Flask
from playwright.sync_api import sync_playwright

# --- Part 1: Web Server and Shared Data ---

# Global variable to hold the screenshot bytes, with a lock for thread safety
latest_screenshot_bytes = None
lock = Lock()

app = Flask(__name__)

@app.route('/')
def health_check_and_screenshot():
    """
    This route serves an HTML page that displays the latest screenshot.
    It will show a "loading" message until the screenshot is ready.
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
                <style>
                    body {{ background-color: #121212; color: white; font-family: sans-serif; text-align: center; }}
                    img {{ border: 2px solid #555; max-width: 90%; height: auto; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <h1>Bloxd.io Bot Status</h1>
                <p>A single screenshot was taken at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>The bot is now idle. This page will not update.</p>
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
                <p>Waiting for the bot to take a screenshot. This page will refresh automatically.</p>
            </body>
        </html>
        """, 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Part 2: Simplified Playwright Bot ---
def run_bot():
    """
    Navigates to bloxd.io, takes one screenshot, and then stops.
    """
    global latest_screenshot_bytes
    browser = None
    try:
        with sync_playwright() as p:
            print("Initializing the browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Navigating to https://bloxd.io/")
            page.goto("https://bloxd.io/", timeout=90000, wait_until="load")

            print("Page loaded. Waiting 10 seconds for elements to render...")
            time.sleep(10)

            print("Taking screenshot...")
            # Take screenshot and store it in the global variable for Flask
            with lock:
                latest_screenshot_bytes = page.screenshot()
            
            print("Screenshot captured and is now available on the website.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if browser:
            browser.close()
        print("Browser session closed.")


if __name__ == "__main__":
    # Start the web server in a background thread
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run the bot's task
    run_bot()
    
    # Keep the container (and the web server) running
    print("Bot has finished its task. Container will now idle.")
    while True:
        time.sleep(60)
