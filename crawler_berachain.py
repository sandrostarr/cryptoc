import os
import time

from dotenv import load_dotenv

load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

# путь к профайлу пользователя файрфокса для открытия окна браузера с установленным расширением Metamask
firefox_profile_directory = os.getenv('FIREFOX_PROFILE_DIRECTORY')

url = os.getenv('URL')
metamask_pw = os.getenv('METAMASK_PW')

profile = webdriver.FirefoxProfile(profile_directory=firefox_profile_directory)

#proxy vars
proxy_host = "88.209.207.119"
proxy_port = "50100"
proxy_username = "Dropup"
proxy_password = "HJEhLSI9Cr"

#сощдание обьекта прокси
proxy = Proxy()
proxy.proxyType = ProxyType.MANUAL
proxy.http_proxy = f"{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
proxy.ssl_proxy = f"{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

#настройки профиля proxy
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", proxy_host)
profile.set_preference("network.proxy.http_port", int(proxy_port))
profile.set_preference("network.proxy.ssl", proxy_host)
profile.set_preference("network.proxy.ssl_port", int(proxy_port))
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
wait = WebDriverWait(driver, timeout=20)

# переход по ссылке
driver.get(url)

# развернуть окно
driver.maximize_window()


def click_element(element_selector: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(EC.presence_of_element_located((By.XPATH, element_selector)))
    time.sleep(1)
    element.click()


def send_keys_to_element(element_selector: str, input_text: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(EC.presence_of_element_located((By.XPATH, element_selector)))
    element.send_keys(input_text)


# FAUCET START ########################################################################################################

# popup checkbox
selector = "//*[@id='terms']"
click_element(selector)

# popup button
selector = "/html/body/div[1]/div[2]/div[2]/div[5]/button[1]"
click_element(selector)

# captcha
# selector = "/html/body/div/div/div[1]/div/label/input"
# click_element(selector)

# wallet address
selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[2]/div[2]/div/input"
send_keys_to_element(selector, os.getenv('WALLET'))

# drip tokens
selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[3]/button"
click_element(selector)

# FAUCET END ##########################################################################################################
