import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def automate_bloxd():
    """
    Automates a sequence of actions on bloxd.io.
    """
    chrome_options = Options()
    # Essential options for headless/Docker environments
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # --- New options to reduce memory ---
    chrome_options.add_argument("--disable-gpu") # Disables GPU hardware acceleration, essential for headless
    chrome_options.add_argument("--window-size=1280,800") # A smaller window can use less memory
    chrome_options.add_argument("--disable-features=NetworkService,NetworkServiceInProcess")

    # Load the unpacked ad-blocker extension from the directory
    chrome_options.add_argument('--load-extension=/app/ublock')

    driver = None
    try:
        print("Initializing the browser with ad blocker...")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)

        # Go to the website
        print("Navigating to https://www.bloxd.io/...")
        driver.get("https://www.bloxd.io/")

        # 1. Click the "Agree" button
        print("Looking for the 'Agree' button...")
        agree_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ButtonBody' and text()='Agree']")))
        agree_button.click()
        print("Clicked 'Agree'.")

        # 2. Click the "Sandbox Survival" game card
        print("Looking for the 'Sandbox Survival' game card...")
        survival_card = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "AvailableGameclassicsurvival")))
        survival_card.click()
        print("Clicked 'Sandbox Survival'.")

        # 3. Enter the lobby name
        print("Entering lobby name...")
        lobby_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Lobby Name']")))
        lobby_input.send_keys("🩸🩸lifesteal😈")
        print("Lobby name entered.")

        # 4. Click the "Join" button
        print("Looking for the 'Join' button...")
        join_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ButtonBody' and text()='Join']")))
        join_button.click()
        print("Clicked 'Join'. Joining the game...")

        # 5. Wait for the game to load and interact
        print("Waiting 5 seconds for the game to load...")
        time.sleep(5)

        print("Activating game window and typing message...")
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER).pause(1).send_keys("Hello World By forgot :O").send_keys(Keys.ENTER).perform()
        print("Message sent in chat.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Saving a screenshot can be helpful for debugging
        # driver.save_screenshot("error_screenshot.png")

    finally:
        print("Automation script has finished its tasks.")
        
if __name__ == "__main__":
    automate_bloxd()
    
    # Keep the container running
    print("Container will now idle.")
    while True:
        time.sleep(60)
