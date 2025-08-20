import time
import os
import base64
from threading import Thread, Lock
from urllib.parse import quote
from flask import Flask
from playwright.sync_api import sync_playwright

# --- Part 1: Web Server and Shared Data ---
bot_status_message = "Bot is starting up..."
lock = Lock()
app = Flask(__name__)

@app.route('/')
def health_check_and_status():
    global bot_status_message
    with lock:
        current_status = bot_status_message
    
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
            <h2>Current Status: {current_status}</h2>
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
            print("Initializing the browser...")
            with lock:
                bot_status_message = "Initializing the browser..."
            browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
            page = browser.new_page()

            # Construct the direct URL, ensuring the lobby name is correctly URL-encoded.
            game_mode = "classic"
            lobby_name_raw = "🩸🩸lifesteal😈"
            lobby_name_encoded = quote(lobby_name_raw)
            direct_url = f"https://bloxd.io/play/{game_mode}/{lobby_name_encoded}"
            
            print(f"Navigating directly to server: {direct_url}")
            with lock:
                bot_status_message = f"Navigating directly to lobby: {lobby_name_raw}"
            
            # Go straight to the game server URL
            page.goto(direct_url, timeout=90000, wait_until="domcontentloaded")

            print("Waiting 20 seconds for the world to render...")
            with lock:
                bot_status_message = "In lobby, waiting for world to render..."
            time.sleep(20)

            print("Activating game window and typing message...")
            page.keyboard.press("Enter")
            time.sleep(1)
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

            print("Bot has completed its task and will now pause indefinitely.")
            with lock:
                bot_status_message = "Task completed successfully! Bot is now idle in-game."

            while True:
                time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")
        with lock:
            bot_status_message = f"An error occurred: {e}"
        
        print("An error occurred, but the container will continue to idle.")
        while True:
            time.sleep(60)


if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    run_bot_sequence()
