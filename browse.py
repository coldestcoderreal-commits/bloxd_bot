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
            context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
            page = context.new_page()

            print("Navigating to https://bloxd.io/")
            with lock:
                bot_status_message = "Navigating to bloxd.io..."
            page.goto("https://bloxd.io/", timeout=90000, wait_until="domcontentloaded")
            
            print("Page loaded. Waiting 15 seconds for initial animations to settle...")
            time.sleep(15)

            # --- THIS IS THE FINAL, ROBUST POP-UP REMOVAL ---
            try:
                print("Looking for the privacy pop-up to remove it...")
                popup_selector = "div.PopupNotification"
                page.wait_for_selector(popup_selector, state='visible', timeout=15000)
                # Execute JavaScript to remove the element from the page
                page.evaluate("document.querySelector('.PopupNotification').remove()")
                print("Successfully removed the pop-up from the page.")
            except Exception as e:
                print(f"Warning: Could not find pop-up to remove. Moving on. Error: {e}")

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
            print("Clicking 'Sandbox Survival' game card...")
            page.locator(game_card_selector).click()
            print("Clicked 'Sandbox Survival'.")
            
            lobby_input_locator = page.get_by_placeholder("Lobby Name")
            lobby_name = "🩸🩸lifesteal😈"
            print(f"Waiting for lobby input to be ready...")
            lobby_input_locator.wait_for(state="visible", timeout=30000)
            
