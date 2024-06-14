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
    logger.info("Scrapping AirBnb to retrieve reservations")

    logger.info("Opening Airbnb login page...")
    # Open the website
    driver.get("https://airbnb.com/login")

    # Wait for the login button to be clickable
    logger.info("LOGIN: Waiting for login button...")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/div[3]/div/div[4]/button"))
    )
    login_button.click()
    logger.info("LOGIN: Clicked login button.")

    # Wait for the email input to be visible
    logger.info("LOGIN: Waiting for email input...")
    login_email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="email-login-email"]'))
    )
    login_email_input.clear()
    login_email_input.send_keys("info@thekeytothekeys.com")
    logger.info("LOGIN: Entered email.")

    # Click the next button
    logger.info("LOGIN: Waiting for next button...")
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/form/div[3]/button"))
    )
    next_button.click()
    logger.info("LOGIN: Clicked next button.")

    # Wait for the password input to be visible
    logger.info("LOGIN: Waiting for password input...")
    login_password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="email-signup-password"]'))
    )
    login_password_input.clear()
    login_password_input.send_keys("Loscayos2024")
    logger.info("LOGIN: Entered password.")

    # Click the submit button
    logger.info("LOGIN: Waiting for submit button...")
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/main/div/div/div/div/div/div/form/div[3]/button'))
    )
    submit_button.click()
    logger.info("LOGIN: Clicked submit button.")

    # Wait for the login process to complete and the URL to change
    logger.info("LOGIN: Waiting for login process to complete...")
    WebDriverWait(driver, 20).until(
        EC.url_to_be("https://www.airbnb.com/")
    )
    logger.info("LOGIN: Login successful. Current URL: %s", driver.current_url)

    # Now navigate to the hosting page
    logger.info("Navigating to reservations page...")
    driver.get("https://www.airbnb.com/hosting/reservations/all")
    logger.info("Navigated to reservations page.")

    logger.info("Exporting all reservations")
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div/main/div[1]/section/div[2]/div[1]/div/div/div[2]/div/button').click()
    driver.find_element(By.XPATH, '/html/body/div[8]/div/div/section/div/div/div[2]/div/div/div[1]/div/div/div/span/button').click()
    driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/footer/a').click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "~/Downloads/reservations.csv")))

    logger.info("All reservations exported")

finally:
    # Close the browser
    logger.info("Closing the browser.")
    driver.quit()
    logger.info('Done')

https://www.lodgify.com/oh/PropertyOwner/QuoteReport?filter=eyJQcm9wZXJ0eU93bmVySWQiOjAsIlVucmVwbGllZCI6ZmFsc2UsIlVucmVhZCI6ZmFsc2UsIlRyYXNoIjpmYWxzZSwiT3ZlcmR1ZSI6ZmFsc2UsIkJvb2tpbmdTdGF0dXNlcyI6W10sIlF1b3RlU3RhdHVzZXMiOltdLCJCb29raW5nU291cmNlc1NlY3Rpb24iOnsiSXNJbnZlcnNlZCI6ZmFsc2UsIlNvdXJjZXNDb250YWlucyI6W10sIlNvdXJjZXNOb3RDb250YWlucyI6WyJPSCIsIk1hbnVhbCIsIkFpcmJuYiIsIkFpcmJuYkludGVncmF0aW9uIiwiQm9va2luZ0NvbSIsIkV4cGVkaWEiLCJIb21lQXdheSIsIkd2ciJdLCJJc0VtcHR5Ijp0cnVlfSwiUm9vbVR5cGVzIjpbXSwiUHJvcGVydGllcyI6W10sIlNlYXJjaFRleHQiOiIiLCJDb3VudCI6ODB9

https://www.lodgify.com/oh/PropertyOwner/QuoteReport?filter=eyJQcm9wZXJ0eU93bmVySWQiOjAsIkRhdGVTZWN0aW9uIjp7IlR5cGUiOiJSYW5nZSIsIlN0YXJ0RGF0ZSI6IjIwMjQtMDYtMDFUMDA6MDA6MDAiLCJFbmREYXRlIjoiMjAyNC0wNi0zMFQwMDowMDowMCIsIkNoZWNrSW4iOnRydWUsIkNoZWNrT3V0Ijp0cnVlLCJTdGF5Ijp0cnVlLCJJc1ZhbGlkIjp0cnVlfSwiVW5yZXBsaWVkIjpmYWxzZSwiVW5yZWFkIjpmYWxzZSwiVHJhc2giOmZhbHNlLCJPdmVyZHVlIjpmYWxzZSwiQm9va2luZ1N0YXR1c2VzIjpbIkJvb2tlZCIsIk9wZW4iLCJUZW50YXRpdmUiXSwiUXVvdGVTdGF0dXNlcyI6WyJBZ3JlZWQiLCJOb3RTZW50IiwiUGVuZGluZ0Zvck93bmVyIiwiUGVuZGluZ0Zvckd1ZXN0IiwiUGVuZGluZ0ZvclBheW1lbnQiLCJSZWplY3RlZCIsIk5vbmUiXSwiQm9va2luZ1NvdXJjZXNTZWN0aW9uIjp7IklzSW52ZXJzZWQiOnRydWUsIlNvdXJjZXNDb250YWlucyI6WyJCb29raW5nQ29tIiwiRXhwZWRpYSIsIkhvbWVBd2F5IiwiTWFudWFsIiwiT0giXSwiU291cmNlc05vdENvbnRhaW5zIjpbIkFpcmJuYiIsIkFpcmJuYkludGVncmF0aW9uIiwiR3ZyIl0sIklzRW1wdHkiOmZhbHNlfSwiUm9vbVR5cGVzIjpbXSwiUHJvcGVydGllcyI6W10sIlNlYXJjaFRleHQiOiIiLCJDb3VudCI6ODB9