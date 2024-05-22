import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

load_dotenv()

# путь к профайлу пользователя файрфокса для открытия окна браузера с установленным расширением Metamask
firefox_profile_directory = os.getenv('FIREFOX_PROFILE_DIRECTORY')

url = os.getenv('URL')
metamask_pw = os.getenv('METAMASK_PW')

profile = webdriver.FirefoxProfile(profile_directory=firefox_profile_directory)

# настройки профиля proxy
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", os.getenv('PROXY_HOST'))
profile.set_preference("network.proxy.http_port", int(os.getenv('PROXY_PORT')))
profile.set_preference("network.proxy.ssl", os.getenv('PROXY_HOST'))
profile.set_preference("network.proxy.ssl_port", int(os.getenv('PROXY_PORT')))
profile.set_preference("network.proxy.no_proxies_on", "")

# настройка и подключение профайла пользователя файрфокса в веб-драйвер
options = webdriver.FirefoxOptions()

# фоновый запуск браузера в headless-режиме
# options.add_argument("--headless")

options.profile = profile

driver = webdriver.Firefox(options=options)

# неявное ожидание поиска элементов
# driver.implicitly_wait(20)

# явное ожидание поиска элементов
wait = WebDriverWait(driver, timeout=5)

# переход по ссылке
driver.get(url)

# развернуть окно
driver.maximize_window()


def click_element(element_selector: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    time.sleep(1)
    element.click()


# функция для клика на элементы, которых может не быть на странице и которые можно пропустить и не падать в фатал
def try_click_element_and_continue(element_selector: str, extra_sleep: int = 0):
    try:
        click_element(element_selector, extra_sleep)
    except TimeoutException:
        pass


def send_keys_to_element(element_selector: str, input_text: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    element.send_keys(input_text)


# функция для получения тестовых токенов
def get_test_tokens_from_faucet():
    # # popup checkbox
    # selector = "//*[@id='terms']"
    # try_click_element_and_continue(selector)
    #
    # # popup button
    # selector = "/html/body/div[1]/div[2]/div[2]/div[5]/button[1]"
    # try_click_element_and_continue(selector)

    # captcha
    selector = "/html/body/div/div/div[1]/div/label/input"
    try_click_element_and_continue(selector)

    # wallet address
    selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[2]/div[2]/div/input"
    send_keys_to_element(selector, os.getenv('WALLET'))

    # drip tokens
    selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[3]/button"
    click_element(selector)


# FAUCET START ########################################################################################################

get_test_tokens_from_faucet()

# FAUCET END ##########################################################################################################
