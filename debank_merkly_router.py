import os
import random
import time
import pickle
import pyautogui
import undetected_chromedriver as uc
import web3

from typing import ClassVar
from dotenv import load_dotenv
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from lib.proxy import get_plugin_file as plugin_file
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from web3 import Web3, Account
from web3.contract import Contract

debridge_link = ''

load_dotenv()

metamask_pw = os.getenv('METAMASK_PW')
wait: ClassVar[WebDriverWait]

cookies = 'cookies.dat'

deBridge_chains = {
    "arbitrum": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[4]',
    "linea": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[7]',
    "op": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[8]',
    "base": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[9]',
    # "polygon": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[3]',
    "bnb": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[2]'
}

deBridge_chains_fromLinea = {
    "arbitrum": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[4]',
    "op": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[7]',
    "base": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[8]',
    # "polygon": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[3]',
    "bnb": '//*[@id="dln-form-container"]/div/app-select-token/div/div[2]/app-networks-list/div/div/div[2]'
}

rpc_chain = {
    "arbitrum": 'https://arbitrum.llamarpc.com',
    "linea": 'https://linea.drpc.org',
    "op": 'https://optimism.llamarpc.com',
    "base": 'https://1rpc.io/base',
    # "polygon": 'https://1rpc.io/matic',
    "bnb": 'https://1rpc.io/bnb'

}


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

    # undetected_chromedriver (для того, чтобы cloudflare не палил нас)
    driver = uc.Chrome(options=options)
    return driver


def click_element(element_selector: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    time.sleep(1)
    element.click()
    time.sleep(0.5)


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
#TODO переписать через TRY
def create_sign_sent_rabby(driver: uc.Chrome, window_number_to_return: int | None = None):
    # rabby sign and create
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(selector)

    # rabby sent
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(selector)

    if window_number_to_return is not None:
        # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
        # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
        driver.switch_to.window(driver.window_handles[window_number_to_return])
        time.sleep(1)


# создание и подписание транз в rabby (для вариации в fullscreen mode rabby)
def create_sign_sent_rabby_full_window(driver: uc.Chrome, window_number_to_open: int, window_number_to_return: int):
    time.sleep(4)

    # переключение на окно rabby (номер окна передаётся в параметре window_number_to_open
    driver.switch_to.window(driver.window_handles[window_number_to_open])

    # rabby sign and create
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(3)

    # rabby sent
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
    # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
    driver.switch_to.window(driver.window_handles[window_number_to_return])
    time.sleep(3)


# функция для логина в rabby wallet
def rabby_wallet_login(driver):
    time.sleep(5)
    # клики на расширениях для использования
    # TODO надо использовать через url расширения и убрать клики
    # open extensions
    ext_location = pyautogui.locateOnScreen('IMG/extense.png')
    ext_locationX = ext_location.left / 2 + ext_location.width / 4
    ext_locationY = ext_location.top / 2 + ext_location.height / 4
    pyautogui.moveTo(ext_locationX, ext_locationY)
    pyautogui.click(button='left')

    time.sleep(0.1)

    # click rabby
    rabby_location = pyautogui.locateOnScreen('IMG/rabbi_wall.png')
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


def check_wallet_balance(chain_rpc):
    w3 = Web3(Web3.HTTPProvider(chain_rpc))
    address = w3.eth.account.from_key(os.getenv('PRIVATE_KEY')).address
    wallet_address = Web3.to_checksum_address(address)

    balance = w3.eth.get_balance(wallet_address)
    return balance


def max_balance():
    arb_balance = check_wallet_balance(rpc_chain["arbitrum"])
    op_balance = check_wallet_balance(rpc_chain["op"])
    linea_balance = check_wallet_balance(rpc_chain["linea"])
    base_balance = check_wallet_balance(rpc_chain["base"])
    # polygon_balance = int(check_wallet_balance(rpc_chain["polygon"])) / 3000
    bnb_balance = int(check_wallet_balance(rpc_chain["bnb"])) * 0.19

    max_balance = max(arb_balance, op_balance, linea_balance, base_balance, bnb_balance)

    if max_balance == arb_balance:
        return "arbitrum"
    elif max_balance == op_balance:
        return "op"
    elif max_balance == linea_balance:
        return "linea"
    elif max_balance == base_balance:
        return "base"
    elif max_balance == bnb_balance:
        return "bnb"
    # elif max_balance == polygon_balance:
    #     return "polygon"


def deBridge_choose_to_chain(fromChain):
    if fromChain == "linea":
        db_ch = list(deBridge_chains_fromLinea)
    else:
        db_ch = list(deBridge_chains)

        db_ch.remove(fromChain)

    random_chain = random.choice(db_ch)

    return random_chain


def deBridge_choose_roters(fromChain, toChain):
    rpc_chain_link = rpc_chain[fromChain]

    from_Chain = deBridge_chains[fromChain]

    if fromChain == "linea":
        to_Chain = deBridge_chains_fromLinea[toChain]
    else:
        to_Chain = deBridge_chains[toChain]

    time.sleep(5)

    # select btn
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[1]/div/div[2]/div[2]'
    click_element(selector)
    time.sleep(7)

    # select network
    click_element(from_Chain)
    time.sleep(3)

    ETH = '//*[@id="dln-form-container"]/div/app-select-token/div/div[4]/div/cdk-virtual-scroll-viewport/div[1]/div[1]'
    try_click_element_and_continue(ETH)
    time.sleep(2)

    # select where
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[3]/div[2]/div[2]'
    click_element(selector)
    time.sleep(5)

    # select network
    click_element(to_Chain)
    time.sleep(3)

    click_element(ETH)

    # input value
    balance = check_wallet_balance(rpc_chain_link) * 0.85
    amount = balance / 10 ** 18
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[1]/div/div[2]/div[1]/input'
    send_keys_to_element(selector, str(amount))
    time.sleep(4)


def deBridge_connector(driver):
    driver.get('https://app.debridge.finance/r/4503')
    time.sleep(10)

    # connect to app
    selector = '//*[@id="dln-form-container"]/div/div[3]/div/button'
    click_element(selector)
    time.sleep(1)

    # rabby wallet
    selector = '//*[@id="mat-mdc-dialog-0"]/div/div/dlg-unlock-wallet/div[2]/div[1]/button[9]'
    click_element(selector)

    # switch to rabby
    driver.switch_to.window(driver.window_handles[2])

    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)


def debridge_confirm_trade(driver):
    time.sleep(3)
    # confirm trade
    selector = '//*[@id="dln-form-container"]/div/div[3]/div/button'
    click_element(selector)
    time.sleep(3)

    # terms
    selector = '//*[@id="mat-mdc-dialog-1"]/div/div/app-dlg-terms-conditions-agreement/div[3]/button'
    try_click_element_and_continue(selector)
    time.sleep(2)

    # rabby sign
    try:
        driver.switch_to.window(driver.window_handles[2])
    except:
        pass
    time.sleep(2)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    try_click_element_and_continue(selector)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    try_click_element_and_continue(selector)
    time.sleep(2)

    try:
        driver.switch_to.window(driver.window_handles[2])
    except:
        pass
    time.sleep(2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(30)


# работа с площадкой
def debridge_transfers(driver):
    deBridge_connector(driver)
    count_swaps = 0
    max_swaps = random.randint(7, 11)
    print(max_swaps)

    while max_swaps > count_swaps:
        print('Номер свапа: ', count_swaps + 1)
        fromChain = max_balance()

        toChain = deBridge_choose_to_chain(fromChain)

        deBridge_choose_roters(fromChain, toChain)

        debridge_confirm_trade(driver)
        count_swaps = count_swaps + 1

    print('DONE')


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    global wait
    wait = WebDriverWait(driver, timeout=5)

    rabby_wallet_login(driver)
    debridge_transfers(driver)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(3000)
