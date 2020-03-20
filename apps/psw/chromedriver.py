from selenium import webdriver
import os


def start_driver():

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.binary_location = "/bin/chromium"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--silent-launch")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    driver = webdriver.Chrome(executable_path="chromedriver/chromedriver", options=chrome_options)

    return driver
