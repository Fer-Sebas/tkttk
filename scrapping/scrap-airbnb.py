import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Firefox options
options = Options()
# Uncomment the next line to run Firefox in headless mode
# options.headless = True

# Path to the GeckoDriver (no need to specify if it's in the PATH)
service = Service('/usr/bin/geckodriver')

# Set up the WebDriver with options
driver = webdriver.Firefox(service=service, options=options)

try:
    logger.info("Start")
    driver.implicitly_wait(10)
    logger.info("10 secs should have passed")

    logger.info("Opening Airbnb login page...")
    # Open the website
    driver.get("https://airbnb.com/login")

    # Wait for the login button to be clickable
    logger.info("Waiting for login button...")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/div[3]/div/div[4]/button"))
    )
    login_button.click()
    logger.info("Clicked login button.")

    # Wait for the email input to be visible
    logger.info("Waiting for email input...")
    login_email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="email-login-email"]'))
    )
    login_email_input.clear()
    login_email_input.send_keys("info@thekeytothekeys.com")
    logger.info("Entered email.")

    # Click the next button
    logger.info("Waiting for next button...")
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/form/div[3]/button"))
    )
    next_button.click()
    logger.info("Clicked next button.")

    # Wait for the password input to be visible
    logger.info("Waiting for password input...")
    login_password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="email-signup-password"]'))
    )
    login_password_input.clear()
    login_password_input.send_keys("Loscayos2024")
    logger.info("Entered password.")

    # Click the submit button
    logger.info("Waiting for submit button...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/div/form/div[3]/button'))
    )
    submit_button.click()
    logger.info("Clicked submit button.")

    # Wait for the login process to complete and the URL to change
    logger.info("Waiting for login process to complete...")
    WebDriverWait(driver, 20).until(
        EC.url_to_be("https://www.airbnb.com/")
    )
    logger.info("Login successful. Current URL: %s", driver.current_url)

    # Now navigate to the hosting page
    logger.info("Navigating to hosting page...")
    driver.get("https://www.airbnb.com/hosting/reservations")
    logger.info("Navigated to hosting page.")

finally:
    # Close the browser
    logger.info("Closing the browser.")
    logger.info('Done')
