import os
import time
import pickle
import pyautogui
import undetected_chromedriver as uc

from typing import ClassVar
from dotenv import load_dotenv
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from lib.proxy import get_plugin_file as plugin_file
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

load_dotenv()

url_quest_1 = os.getenv('URL_QUEST_1')
url_quest_15 = os.getenv('URL_QUEST_15')
url_quest_68 = os.getenv('URL_QUEST_68')

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


# создание и подписание транз в rabby
def create_sign_sent_rabby(driver: uc.Chrome, window_number_to_return: int):
    # rabby sign and create
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(selector)

    # rabby sent
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(selector)

    # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
    # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
    driver.switch_to.window(driver.window_handles[window_number_to_return])
    time.sleep(1)


# функция для логина в rabby wallet
def rabby_wallet_login(driver):
    time.sleep(5)
    # клики на расширениях для использования
    # TODO надо использовать через url расширения и убрать клики
    # open extensions
    ext_location = pyautogui.locateOnScreen('IMG/extense.png')
    print(ext_location)
    ext_locationX = ext_location.left / 2 + ext_location.width / 4
    ext_locationY = ext_location.top / 2 + ext_location.height / 4
    pyautogui.moveTo(ext_locationX, ext_locationY)
    pyautogui.click(button='left')

    time.sleep(0.1)

    # click rabby
    rabby_location = pyautogui.locateOnScreen('IMG/rabbi_wall.png')
    print(ext_location)
    rabby_locationX = rabby_location.left / 2 + rabby_location.width / 4
    rabby_locationY = rabby_location.top / 2 + rabby_location.height / 4
    pyautogui.moveTo(rabby_locationX, rabby_locationY)
    pyautogui.click(button='left')

    # переключение на rabby
    driver.switch_to.window(driver.window_handles[2])

    # click next
    selector = '//*[@id="root"]/div/section/footer/button'
    click_element(selector)

    # click get ready
    selector = '//*[@id="root"]/div/section/footer/a/button'
    click_element(selector)

    # import private key
    selector = '//*[@id="root"]/div/div[3]/div[2]/div[2]'
    click_element(selector)

    # create pass
    selector = '//*[@id="password"]'
    send_keys_to_element(selector, os.getenv('WALLET_PASSWORD'))

    # confirm pass
    selector = '//*[@id="confirmPassword"]'
    send_keys_to_element(selector, os.getenv('WALLET_PASSWORD'))

    # click next button
    selector = '//*[@id="root"]/div/div/div/form/div[3]/button'
    click_element(selector)

    # send private key
    selector = '//*[@id="key"]'
    send_keys_to_element(selector, os.getenv('PRIVATE_KEY'))

    # click next button
    selector = '//*[@id="root"]/div/div/div/div/div/form/div[3]/div/button'
    try_click_element_and_continue(selector)

    # click done button
    selector = '//*[@id="root"]/div/div/div/div/div/form/div[2]/div/button'
    try_click_element_and_continue(selector)

    # click done button
    selector = '/html/body/div[2]/div/div[2]/div/div[2]/button'
    try_click_element_and_continue(selector)

    driver.switch_to.window(driver.window_handles[1])

    time.sleep(1)

    # это настройка расширения rabby без клика по экрану. В undetected_chromedriver почему-то не работает
    # TODO пофиксить и использовать вместо кликов
    # # open extension create password page
    # driver.get("chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/password")
    #
    # time.sleep(1)
    # driver.refresh()
    #
    # # create pass
    # selector = '//*[@id="password"]'
    # send_keys_to_element(selector, os.getenv('WALLET_PASSWORD'))
    #
    # # confirm pass
    # selector = '//*[@id="confirmPassword"]'
    # send_keys_to_element(selector, os.getenv('WALLET_PASSWORD'))
    #
    # # click next button
    # selector = '//*[@id="root"]/div/div/div/form/div[3]/button'
    # click_element(selector)
    #
    # # open extension import key page
    # driver.get("chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/import/key")
    #
    # # send private key
    # selector = '//*[@id="key"]'
    # send_keys_to_element(selector, os.getenv('PRIVATE_KEY'))
    #
    # # click next button
    # selector = '//*[@id="root"]/div/form/div[3]/div/button'
    # try_click_element_and_continue(selector)


# функция для выполнения первого квеста в layer3
def layer3_connect_wallet_and_login(driver):
    driver.get(url_quest_1)

    # connect wallet
    selector = '//*[@id="__next"]/div/div/div/div[2]/header/div/div[2]/div/div[2]/div[1]/button'
    click_element(selector)

    # rabby wallet
    selector = '//*[@id="radix-:rd:-content-evm"]/div/button[1]/div'
    click_element(selector, 1)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    # rabby wallet click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(1)

    driver.switch_to.window(driver.window_handles[2])

    create_sign_sent_rabby(driver, 1)


def layer3_quest_15(driver):
    # TODO переписать под новый интерфейс
    driver.get(url_quest_15)

    # начало задания
    selector = '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/div[2]/button'
    click_element(selector)

    # 1 часть
    selector = '//*[@id="radix-:ra:"]/div/div[3]/div/div/div/button/span'
    click_element(selector)

    selector = '//*[@id="radix-:ra:"]/div/div[3]/div/div/div/button/span'
    click_element(selector)

    selector = '//*[@id="radix-:ra:"]/div/div[3]/div/div/div/button/span'
    click_element(selector)

    selector = '//*[@id="radix-:ra:"]/div/div[3]/div/div/div/button/span'
    click_element(selector)

    # часть 2
    selector = '//*[@id="radix-:ra:"]/div/div[2]/div[2]/div/div/div/a/button'
    click_element(selector)

    # переход на параграф
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div/div[2]/div/span'
    click_element(selector)

    selector = '//*[@id="para-document"]/div/div/div[1]/div[1]/a/div/div/div[1]/img'
    click_element(selector)

    selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[3]/div[1]/button'
    click_element(selector)

    selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div/div[1]/div/div/button'
    click_element(selector)

    selector = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button/div/div'
    click_element(selector)

    # при открытии окна кошелька нужна небольшая пауза перед переключением на другое окно, т.к. оно не сразу появляется
    time.sleep(2)
    # переключение на рабби
    driver.switch_to.window(driver.window_handles[3])

    # коннект в рабби
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    # sign msg
    driver.switch_to.window(driver.window_handles[2])
    selector = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[2]/button[1]'
    click_element(selector)
    time.sleep(2)

    # sing and create
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(selector)
    # sent
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(1)
    # закрыть окно парагарафа
    driver.switch_to.window(driver.window_handles[2])
    driver.close()

    time.sleep(1)
    # вернуться в окно layer3
    driver.switch_to.window(driver.window_handles[1])

    # verif этап 2
    selector = '//*[@id="radix-:ra:"]/div/div[3]/div/div/div/button[2]'
    click_element(selector)

    # switch network
    selector = '//*[@id="radix-:ra:"]/div/div[2]/div/div/div/div/button'
    click_element(selector)

    # claim cube
    selector = '//*[@id="radix-:ra:"]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # rabby подписания
    time.sleep(3)
    print(driver.window_handles)
    # sing and create
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    # sent
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)


def layer3_quest_68(driver):
    driver.get(url_quest_68)


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    global wait
    wait = WebDriverWait(driver, timeout=5)

    rabby_wallet_login(driver)

    layer3_connect_wallet_and_login(driver)

    # layer3_quest_15(driver)
    layer3_quest_68(driver)

    # # читаем cookies из файла
    # with open(cookies, 'rb') as f:
    #     for cookie in pickle.load(f):
    #         driver.add_cookie(cookie)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(300)
