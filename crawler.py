from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurable variables
email = "t.com"
password = "YH1"
moderator_name = "smonov"
num_challenges = 10

# Set up Brave browser options
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Step 1: Log in automatically
driver.get("https://www.hackerrank.com/auth/login")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))).send_keys(email)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))).send_keys(password)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
wait.until(EC.url_contains("/dashboard"))

# Step 2: Navigate to challenges page
driver.get("https://www.hackerrank.com/administration/challenges")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))  

# Step 3: Iterate through challenges
for i in range(num_challenges):
    # Get all challenge links (fix selector to actual challenge links)
    challenge_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "tr[data-is-focus-visible='false']")
    ))
    if i >= len(challenge_links):
        break
    challenge_links[i].click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-tab='moderators']")))

    # Step 4: Go to Moderators tab
    moderators_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='moderators']")
    moderators_tab.click()
    time.sleep(2)

    # Step 5: Check if moderator exists
    moderators = driver.find_elements(By.CLASS_NAME, "moderator-container")
    moderator_exists = any(moderator_name in m.text for m in moderators)

    if not moderator_exists:
        moderator_input = wait.until(EC.presence_of_element_located((By.ID, "moderator")))
        moderator_input.clear()
        moderator_input.send_keys(moderator_name)
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add')]")))
        add_button.click()
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Save Changes')]")))
        save_button.click()
        time.sleep(1)

    # Step 6: Go back to challenges list
    driver.get("https://www.hackerrank.com/administration/challenges")
    time.sleep(2)

driver.quit()