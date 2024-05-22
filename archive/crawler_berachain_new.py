import os
import time
import undetected_chromedriver as uc

from typing import ClassVar
from dotenv import load_dotenv
from selenium import webdriver

from fake_useragent import UserAgent
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from lib.proxy import get_plugin_file as plugin_file
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

load_dotenv()

# url = os.getenv('URL') TODO вынести berachain в отдельный скрипт
url_quest_1 = os.getenv('URL_QUEST_1')
url_quest_15 = os.getenv('URL_QUEST_15')

metamask_pw = os.getenv('METAMASK_PW')
wait: ClassVar[WebDriverWait]

cookies = 'cookies.dat'


def get_chromedriver(use_proxy=False, user_agent=None):
    # создание экземпляра настроек хрома
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    extensions = ['extensions/Rabby-Wallet']

    if use_proxy:
        extensions.append(plugin_file())
    if user_agent:
        options.add_argument('--user-agent=%s' % user_agent)

    extensions_string = ','.join(extensions)
    options.add_argument('--load-extension=' + extensions_string)

    # обычный драйвер
    # driver = webdriver.Chrome(options=options)
    # undetected_chromedriver (для того, чтобы cloudflare не палил нас)
    driver = uc.Chrome(options=options)
    return driver


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
    # popup checkbox
    selector = "//*[@id='terms']"
    try_click_element_and_continue(selector)

    # popup button
    selector = "/html/body/div[1]/div[2]/div[2]/div[5]/button[1]"
    try_click_element_and_continue(selector)

    # captcha
    selector = '/html/body/div/div/div[1]/div/label/input'
    try_click_element_and_continue(selector, 5)

    # wallet address
    selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[2]/div[2]/div/input"
    send_keys_to_element(selector, os.getenv('WALLET'))

    # drip tokens
    selector = "/html/body/div/div[2]/main/div/div[1]/div[1]/div[3]/button"
    click_element(selector)


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    global wait
    wait = WebDriverWait(driver, timeout=5)

    # функция для получения тестовых токенов
    get_test_tokens_from_faucet()

    # # читаем cookies из файла
    # with open(cookies, 'rb') as f:
    #     for cookie in pickle.load(f):
    #         driver.add_cookie(cookie)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(300)
