import os
import random
import time
import pickle
import pyautogui
import undetected_chromedriver as uc
import web3

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

from lib.rabby_connector import rabby_wallet_login

from lib.form_functions import click_element
from lib.form_functions import try_click_element_and_continue
from lib.form_functions import send_keys_to_element

debridge_link = ''

load_dotenv()

metamask_pw = os.getenv('METAMASK_PW')

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


# создание и подписание транз в rabby
#TODO переписать через TRY
def create_sign_sent_rabby(driver: uc.Chrome, wait, window_number_to_return: int | None = None):
    # rabby sign and create
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(wait, selector)

    # rabby sent
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(wait, selector)

    if window_number_to_return is not None:
        # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
        # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
        driver.switch_to.window(driver.window_handles[window_number_to_return])
        time.sleep(1)


# создание и подписание транз в rabby (для вариации в fullscreen mode rabby)
def create_sign_sent_rabby_full_window(driver: uc.Chrome, wait, window_number_to_open: int, window_number_to_return: int):
    time.sleep(4)

    # переключение на окно rabby (номер окна передаётся в параметре window_number_to_open
    driver.switch_to.window(driver.window_handles[window_number_to_open])

    # rabby sign and create
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(wait, selector)
    time.sleep(3)

    # rabby sent
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(wait, selector)

    # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
    # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
    driver.switch_to.window(driver.window_handles[window_number_to_return])
    time.sleep(3)


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


def deBridge_choose_roters(fromChain, toChain, wait):
    rpc_chain_link = rpc_chain[fromChain]

    from_Chain = deBridge_chains[fromChain]

    if fromChain == "linea":
        to_Chain = deBridge_chains_fromLinea[toChain]
    else:
        to_Chain = deBridge_chains[toChain]

    time.sleep(5)

    # select btn
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[1]/div/div[2]/div[2]'
    click_element(wait, selector)
    time.sleep(7)

    # select network
    click_element(wait, from_Chain)
    time.sleep(3)

    ETH = '//*[@id="dln-form-container"]/div/app-select-token/div/div[4]/div/cdk-virtual-scroll-viewport/div[1]/div[1]'
    try_click_element_and_continue(wait, ETH)
    time.sleep(2)

    # select where
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[3]/div[2]/div[2]'
    click_element(wait, selector)
    time.sleep(5)

    # select network
    click_element(wait, to_Chain)
    time.sleep(3)

    click_element(wait, ETH)

    # input value
    balance = check_wallet_balance(rpc_chain_link) * 0.85
    amount = balance / 10 ** 18
    selector = '//*[@id="dln-form-container"]/div/div[2]/div[1]/div/div[2]/div[1]/input'
    send_keys_to_element(wait, selector, str(amount))
    time.sleep(4)


def deBridge_connector(driver, wait):
    driver.get('https://app.debridge.finance/r/4503')
    time.sleep(10)

    # connect to app
    selector = '//*[@id="dln-form-container"]/div/div[3]/div/button'
    click_element(wait, selector)
    time.sleep(1)

    # rabby wallet
    selector = '//*[@id="mat-mdc-dialog-0"]/div/div/dlg-unlock-wallet/div[2]/div[1]/button[9]'
    click_element(wait, selector)

    # switch to rabby
    driver.switch_to.window(driver.window_handles[2])

    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(wait, selector)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)


def debridge_confirm_trade(driver, wait):
    time.sleep(3)
    # confirm trade
    selector = '//*[@id="dln-form-container"]/div/div[3]/div/button'
    click_element(wait, selector)
    time.sleep(3)

    # terms
    selector = '//*[@id="mat-mdc-dialog-1"]/div/div/app-dlg-terms-conditions-agreement/div[3]/button'
    try_click_element_and_continue(wait, selector)
    time.sleep(2)

    # rabby sign
    try:
        driver.switch_to.window(driver.window_handles[2])
    except:
        pass
    time.sleep(2)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    try_click_element_and_continue(wait, selector)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    try_click_element_and_continue(wait, selector)
    time.sleep(2)

    try:
        driver.switch_to.window(driver.window_handles[2])
    except:
        pass
    time.sleep(2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(wait, selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(wait, selector)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(30)


# работа с площадкой
def debridge_transfers(driver, wait):
    deBridge_connector(driver, wait)
    count_swaps = 0
    max_swaps = random.randint(7, 11)
    print(max_swaps)

    while max_swaps > count_swaps:
        print('Номер свапа: ', count_swaps + 1)
        fromChain = max_balance()

        toChain = deBridge_choose_to_chain(fromChain)

        deBridge_choose_roters(fromChain, toChain, wait)

        debridge_confirm_trade(driver, wait)
        count_swaps = count_swaps + 1

    print('DONE')


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    wait = WebDriverWait(driver, timeout=5)

    rabby_wallet_login(driver, wait)
    debridge_transfers(driver, wait)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(3000)
