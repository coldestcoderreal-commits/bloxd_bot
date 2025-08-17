import time
import os
import base64
from threading import Thread, Lock
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
    page = None
    
    try:
        with sync_playwright() as p:
            print("Initializing the browser...")
            with lock:
                bot_status_message = "Initializing the browser..."
            browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
            page = browser.new_page()

            print("Navigating to https://bloxd.io/")
            with lock:
                bot_status_message = "Navigating to bloxd.io..."
            page.goto("https://bloxd.io/", timeout=90000, wait_until="domcontentloaded")
            
            print("Page loaded. Waiting 15 seconds for initial animations to settle...")
            time.sleep(15)

            try:
                print("Looking for the 'Agree' button...")
                agree_button_selector = "div.PromptPopupNotificationBody .ButtonBody:has-text('Agree')"
                page.locator(agree_button_selector).click(timeout=15000)
                print("Clicked the 'Agree' button.")
            except Exception as e:
                print(f"Warning: Could not click 'Agree'. Moving on. Error: {e}")

            try:
                username_selector = "div.PlayerNamePreview .TextFromServerEntityName"
                username = page.locator(username_selector).inner_text(timeout=10000)
                print(f"SUCCESS: Logged in as: {username}")
                with lock:
                    bot_status_message = f"Logged in as: {username}"
            except Exception as e:
                print(f"Warning: Could not extract username. Error: {e}")

            game_card_selector = ".AvailableGameclassicsurvival"
            print(f"Waiting for game card '{game_card_selector}' to be visible...")
            page.wait_for_selector(game_card_selector, state='visible', timeout=30000)
            print("Clicking 'Sandbox Survival' game card (force click)...")
            page.locator(game_card_selector).dispatch_event('click')
            print("Clicked 'Sandbox Survival'.")
            
            # --- THIS IS THE FINAL CORRECTED LOGIC ---
            lobby_input_locator = page.get_by_placeholder("Lobby Name")
            print("Waiting for lobby input to be visible...")
            lobby_input_locator.wait_for(state="visible", timeout=30000)
            print("Clicking on lobby input to focus (force click)...")
            lobby_input_locator.dispatch_event('click') # Use dispatch_event to avoid timeout
            print("Typing lobby name sequentially...")
            lobby_input_locator.press_sequentially("🩸🩸lifesteal😈", delay=50)
            print("Lobby name entered.")

            print("Looking for the 'Join' button...")
            page.get_by_role("button", name="Join").dispatch_event('click')
            print("Clicked 'Join'. Waiting for game to load...")

            print("Waiting 15 seconds for the world to render...")
            time.sleep(15) 
            print("Activating game window and typing message...")
            page.keyboard.press("Enter")
            time.sleep(1)
            page.keyboard.type("Hello World By forgot :O")
            page.keyboard.press("Enter")
            print("Message sent in chat.")

            print("Bot has completed its task and will now pause indefinitely.")
            with lock:
                bot_status_message = "Task completed successfully! Bot is now idle."

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
