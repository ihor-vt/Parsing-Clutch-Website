from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--enable-features=NetworkService,\
                            NetworkServiceInProcess")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("chromedriver_mac/chromedriver")


with webdriver.Chrome(service=service, options=chrome_options) as driver:
    driver.get("https://account.clutch.co/?next=https%3A%2F%2Fclutch.co%2Fit-services%3Floginsalt%3Diw81l32b0s&_gl=1%2a4f13yu%2a_ga%2aMTE5NjA2NjQ0Ny4xNjg5ODUzNTQ5%2a_ga_D0WFGX8X3V%2aMTY5MDAxNDg1NC40LjEuMTY5MDAxNDg5Ny4xNy4wLjA.%2a_fplc%2aYk5heFNzUjdpNWJFZm9JaXZJRmg2cVd6ajd6eVpUdGY2R0ZpeFRhMlJXTU5TdjRiV2FxUnNyVkVFcGFwTktaMENQM0tZdzFEOG1FRkRUc3Q1MHglMkY1N01mOWxIWmNrclMyMGtKZFhzY1FRT3RYMUZ5YVN4WXdSdFAzTmcyMGclM0QlM0Q.")

    wait = WebDriverWait(driver, 20)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "social-auth")))

    auth_google = driver.find_element(By.CLASS_NAME, "google_button")
    auth_google.click()

    sleep(2)

    try:
        auth_mail = wait.until(
            EC.presence_of_element_located((By.ID, "identifierId"))
            )
        auth_mail.send_keys("igor.voyt98@gmail.com")

        sleep(2)

        next_button = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[@jsname='V67aGc' and contains(@class, 'VfPpkd-vQzf8d')\
                    and text()='Далі']")))
        next_button.click()

        sleep(2)

        password_input = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@name='password']"))
                )
        password_input.send_keys("your_password_here")

        sleep(2)

        login_button = wait.until(
            EC.presence_of_element_located((
                By.XPATH, "//span[@jsname='V67aGc' and contains(@class, \
                    'VfPpkd-vQzf8d') and text()='Далі']")))
        login_button.click()
    except Exception as e:
        print("Елемент не знайдений або тайм-аут. \
            Перевірте сторінку та селектори.", e)
