# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006822AC9075BCA84C9A71288059F81F641A73739407730D62278EAA6717A353CA82DF4468C12F8E7D3EB41299BDCED8258DBFF33A695D1F7C26003E08FEA1847392857CDC61DCB0C04C06F5A41B25194FEB1949B3409C4FC8F139456821A7F6C2607F7FC8AAF94FEDE65922C52768C1C982C3947A416FBA44697473D660831CA5C2BBE5289F396DE7915F92817F0B77910B9DD1249660158B5BCA99042DCFC725307F8E65B5980FC82F7125C60D2DAB52F778227CA40B2F78D248A94260C0521B9A177D573B60DB074F4A4A948733F2A9D5354BF93E69AE5F02BE3D6F5F1D82D642EDB5423795B13257784739562A4AD6F61F516605B8498FBFEB9EDA0BA82FB5E3499225A2E7732247383EA50A94E416A5BAEBA4760FE29A4D5F4E77F665157EE0890E6739353588401F1F47044F22085DDCB9C98CF1A5C4C7D6578C7697C5BE5466087E3B508CBD85D87DF647F345680B0119CCC239337C879F6FC9D330CD2DBCAC4B84B2C62ECE212E1F7BA4F7A4A4"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
