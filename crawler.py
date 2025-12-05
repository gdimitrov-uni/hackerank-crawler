from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Configurable variables
email = "mail"
password = "somepass"
moderator_name = "moderator"
num_challenges = 10
CHALLENGES_PER_PAGE = 10

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
challenges_processed = 0

while challenges_processed < num_challenges:
    # Get all challenge rows on the current page using proper selector
    challenge_rows = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "tr[role='row'][data-key]")
    ))
    
    # Calculate how many challenges to process on this page
    challenges_on_page = min(CHALLENGES_PER_PAGE, num_challenges - challenges_processed, len(challenge_rows))
    
    for i in range(challenges_on_page):
        # Re-fetch challenge rows to avoid stale element reference
        challenge_rows = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "tr[role='row'][data-key]")
        ))
        
        if i >= len(challenge_rows):
            break
            
        challenge_rows[i].click()
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
            time.sleep(1)

        # Step 6: Go back to challenges list
        driver.get("https://www.hackerrank.com/administration/challenges")
        time.sleep(2)
        
        challenges_processed += 1
        
        # Check if we've processed all required challenges
        if challenges_processed >= num_challenges:
            break
    
    # If we need more challenges and have processed a full page, go to next page
    if challenges_processed < num_challenges and challenges_on_page >= CHALLENGES_PER_PAGE:
        # Navigate to next page (implement pagination logic here)
        # This assumes there's a next page button or pagination control
        try:
            next_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Next page'], button[aria-label='next'], [data-testid='next-page']")
            ))
            next_button.click()
            time.sleep(2)
        except (TimeoutException, NoSuchElementException):
            # No more pages available
            break
    else:
        # No more challenges needed or no more challenges on this page
        break

driver.quit()