from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, WebDriverException
from bs4 import BeautifulSoup
import time
import os
import subprocess
import traceback


username = ''
password = ''


def configure_firefox_driver():
    driver = webdriver.Firefox(
        executable_path="./geckodriver"
    )
    return driver


def login(driver, url):
    try:
        driver.get(url)
        input_username = driver.find_element_by_xpath(
            '//input[@type="email"]')
        input_password = driver.find_element_by_xpath(
            '//input[@type="password"]')
        btn_signin = driver.find_element_by_xpath(
            '//button[@type="submit"]')

        input_username.send_keys(username)
        input_password.send_keys(password)

        btn_signin.click()

    except TimeoutException:
        time.sleep(15)
        login(driver, url)


def select_skip_btn(driver):

    try:
        skip_btn = driver.find_element_by_xpath(
            "(//div[@class='css-59lkcz' and text()='Skip' ])[position()=1]")

        skip_btn.click()
        time.sleep(3)

    except NoSuchElementException:
        print('No Skip Button')
    except ElementNotInteractableException:
        print('Skip button not interactable, [this shouldn\'t occur]')


def download_clip(driver, url):
    try:

        driver.get(url)
        time.sleep(10)

        # Click the Skip button
        select_skip_btn(driver)

        audio_link = driver.find_element_by_tag_name('audio')

        print(f'Downloading {url}')
        subprocess.run(['aria2c', '-c', '--max-download-limit',
                        '10M', audio_link.get_attribute('src')])

        # Apped this url to the log that contains list of downloaded url's
        with open("last_downloaded.log", "a") as myfile:
            myfile.write(url + '\n')
        print("Sleeping for 30 seconds")
        time.sleep(60)

    except NoSuchElementException:
        print(f'{url} no audio found.')

    except Exception as e:
        with open("error.log", "a") as myfile:
            tb = traceback.format_exc()
            myfile.write(tb + '\n')


driver = configure_firefox_driver()

# Login
login(driver, 'https://www.headspace.com/login')
time.sleep(10)

# start 251
# end 2800
for i in range(451, 2757):
    download_clip(driver, f'https://my.headspace.com/play/{i}')


# download_clip(driver, 'https://my.headspace.com/play/451')
#download_clip(driver, 'https://my.headspace.com/play/452')
# download_clip(driver, 'https://my.headspace.com/play/630')
# download_clip(driver, 'https://my.headspace.com/play/640')

driver.quit()
