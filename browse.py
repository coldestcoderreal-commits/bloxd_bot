import time
import os
from threading import Thread
from flask import Flask
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# --- Part 1: Web Server and Shared Data ---
bot_status_message = "Bot is starting up..."

app = Flask(__name__)

@app.route('/')
def health_check_and_status():
    global bot_status_message
    html_content = f"""
    <html>
        <head>
            <title>Bloxd.io Bot Status</title>
            <meta http-equiv="refresh" content="7">
            <style>
                body {{ background-color: #121212; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }}
                h1 {{ color: #4CAF50; }}
            </style>
        </head>
        <body>
            <h1>Bloxd.io Bot Status</h1>
            <h2>Current Status: {bot_status_message}</h2>
            <p>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
    </html>
    """
    return html_content, 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Part 2: Playwright Bot ---
def run_bot_sequence():
    global bot_status_message
    browser = None
    
    try:
        with sync_playwright() as p:
            bot_status_message = "Initializing browser..."
            print(bot_status_message)
            browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
            page = browser.new_page()

            lobby_name = "🩸🩸lifesteal😈"
            direct_url = f"https://bloxd.io/play/classic/{lobby_name}"
            
            bot_status_message = f"Navigating to lobby: {lobby_name}"
            print(bot_status_message)
            page.goto(direct_url, timeout=90000, wait_until="domcontentloaded")

            # --- THE FINAL FIX ---
            # Handle the intermediate "Enter Bloxd" screen if it appears.
            try:
                bot_status_message = "Looking for 'Enter Bloxd' button..."
                print(bot_status_message)
                enter_button_selector = "div.ButtonBody:has-text('Enter Bloxd')"
                page.locator(enter_button_selector).click(timeout=20000)
                bot_status_message = "Clicked 'Enter Bloxd'. Waiting for world to render..."
                print(bot_status_message)
                time.sleep(15) # Extra wait after clicking
            except PlaywrightTimeoutError:
                bot_status_message = "'Enter Bloxd' button not found, assuming direct entry. Waiting for world to render..."
                print(bot_status_message)
                time.sleep(15)

            bot_status_message = "Activating game window..."
            print(bot_status_message)
            # Click the center of the viewport to focus the game window
            page.mouse.click(640, 360) 
            time.sleep(1)

            print("Typing message...")
            page.keyboard.press("Enter")
            time.sleep(1)
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

            bot_status_message = "Task completed successfully! Bot is now idle in-game."
            print(bot_status_message)

            while True:
                time.sleep(60)

    except Exception as e:
        bot_status_message = f"An error occurred: {e}"
        print(bot_status_message)
        
        print("An error occurred, but the container will continue to idle.")
        while True:
            time.sleep(60)

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    run_bot_sequence()
