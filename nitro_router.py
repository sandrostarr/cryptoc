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

project_link = 'https://app.routernitro.com/swap?referal=RT1709811819842'

load_dotenv()

metamask_pw = os.getenv('METAMASK_PW')
wait: ClassVar[WebDriverWait]

cookies = 'cookies.dat'

nitro_chains = {
    "arbitrum": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[4]',
    "scroll": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[2]',
    "zksync": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[3]',
    # "blast": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[7]',
    "manta": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[14]',
    "mode": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[16]',
    "linea": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[5]',
    "op": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[9]',
    "base": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[6]',
    "polygon": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[8]',
    # "bnb": '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[11]',
}
# TODO вынести в файл RPC
rpc_chain = {
    "arbitrum": 'https://arbitrum.llamarpc.com',
    "linea": 'https://linea.drpc.org',
    "op": 'https://optimism.llamarpc.com',
    "base": 'https://1rpc.io/base',
    "polygon": 'https://1rpc.io/matic',
    # "bnb": 'https://1rpc.io/bnb',
    "scroll": 'https://1rpc.io/scroll',
    "zksync": 'https://1rpc.io/zksync2-era',
    # "blast": 'https://rpc.blast.io',
    "manta": 'https://1rpc.io/manta',
    "mode": 'https://1rpc.io/mode',
}

network_tiker = {
    "arbitrum": 'ETH',
    "linea": 'ETH',
    "op": 'ETH',
    "base": 'ETH',
    "polygon": 'POLYGON',
    # "bnb": 'BNB',
    "scroll": 'ETH',
    "zksync": 'ETH',
    # "blast": 'ETH',
    "manta": 'ETH',
    "mode": 'ETH',
}


# TODO вынести в доп функции
def low_pause():
    t = random.randint(3, 15)
    time.sleep(t)


def mid_pause():
    t = random.randint(15, 30)
    time.sleep(t)


def long_pause():
    t = random.randint(30, 90)
    time.sleep(t)


# TODO вынести в отдельный файл все данные по созданию окружения брайузера
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


# TODO   вынести в отдельный файл функции для работы с вводом выводом данных и кликами
def click_element(element_selector: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    time.sleep(1)
    element.click()
    time.sleep(0.5)


# TODO   вынести в отдельный файл функции для работы с вводом выводом данных и кликами
# функция для клика на элементы, которых может не быть на странице и которые можно пропустить и не падать в фатал
def try_click_element_and_continue(element_selector: str, extra_sleep: int = 0):
    try:
        click_element(element_selector, extra_sleep)
    except TimeoutException:
        pass


# TODO   вынести в отдельный файл функции для работы с вводом выводом данных
def send_keys_to_element(element_selector: str, input_text: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    element.send_keys(input_text)


# TODO вынести отдельно в файл функции взаимодействия с кошельком
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


# TODO вынести отдельно в файл функции взаимодействия с кошельком
# создание и подписание транз в rabby (для вариации в fullscreen mode rabby)
def create_sign_sent_rabby_full_window(driver: uc.Chrome, window_number_to_open: int, window_number_to_return: int):
    time.sleep(3)

    # переключение на окно rabby (номер окна передаётся в параметре window_number_to_open
    driver.switch_to.window(driver.window_handles[window_number_to_open])

    #ignore mistakes
    selector = '//*[@id="root"]/div/div[2]/section/div[4]/span[2]'
    try_click_element_and_continue(selector)
    time.sleep(1)

    # rabby sign and create
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(2)

    # rabby sent
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    # после нажатия кнопки окно закрывается, selenium теряет фокус с окна и падает ошибка
    # поэтому надо вернуться на предыдущее окно сразу после нажатия на кнопку
    driver.switch_to.window(driver.window_handles[window_number_to_return])
    time.sleep(3)

def connect_to_project_rabby(driver: uc.Chrome, window_number_to_open: int, window_number_to_return: int):
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[window_number_to_open])

    # connect btn
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(0.5)

    driver.switch_to.window(driver.window_handles[window_number_to_return])
    time.sleep(3)




# TODO вынести в отдельный файл все данные по созданию окружения брайузера
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


# TODO вынести в файл работы с WEB3
def check_wallet_balance(chain_rpc):
    w3 = Web3(Web3.HTTPProvider(chain_rpc))
    address = w3.eth.account.from_key(os.getenv('PRIVATE_KEY')).address
    wallet_address = Web3.to_checksum_address(address)

    balance = w3.eth.get_balance(wallet_address)
    return balance


# TODO вынести в файл работы с WEB3
def max_balance():
    arb_balance = check_wallet_balance(rpc_chain["arbitrum"])
    op_balance = check_wallet_balance(rpc_chain["op"])
    linea_balance = check_wallet_balance(rpc_chain["linea"])
    base_balance = check_wallet_balance(rpc_chain["base"])
    polygon_balance = int(check_wallet_balance(rpc_chain["polygon"])) / 3000
    # bnb_balance = int(check_wallet_balance(rpc_chain["bnb"])) * 0.19
    scroll_balance = check_wallet_balance(rpc_chain["scroll"])
    mode_balance = check_wallet_balance(rpc_chain["mode"])
    # blast_balance = check_wallet_balance(rpc_chain["blast"])
    zksync_balance = check_wallet_balance(rpc_chain["zksync"])
    manta_balance = check_wallet_balance(rpc_chain["manta"])



    max_balance = max(arb_balance, op_balance, linea_balance, base_balance, polygon_balance, scroll_balance, mode_balance, zksync_balance,manta_balance)

    if max_balance == arb_balance:
        return "arbitrum"
    elif max_balance == op_balance:
        return "op"
    elif max_balance == linea_balance:
        return "linea"
    elif max_balance == base_balance:
        return "base"
    elif max_balance == polygon_balance:
        return "polygon"
    # elif max_balance == bnb_balance:
    #     return "bnb"
    elif max_balance == scroll_balance:
        return "scroll"
    elif max_balance == mode_balance:
        return "mode"
    # elif max_balance == blast_balance:
    #     return "blast"
    elif max_balance == zksync_balance:
        return "zksync"
    elif max_balance == manta_balance:
        return "manta"

# подклбчение к проекту
def project_connect_wallet(driver):
    driver.get(project_link)
    mid_pause()

    # push connect btn
    connect_btn = '//*[@id="root"]/div/div[3]/div[3]/div[2]'
    click_element(connect_btn)

    # choose wallet
    mm_rabby = '/html/body/div[2]/div[3]/div/div/div[2]/div/div/div[1]'
    click_element(mm_rabby)

    connect_to_project_rabby(driver,2,1)

# выбор сетей и указание суммы к отправке
def nitro_choose_routes(driver, fromChain, toChain):
    print('1')
    time.sleep(1)

    # open list of networks fromChain
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div[1]/div[2]'
    click_element(selector)
    time.sleep(2)

    print('2')
    # open all networks
    selector = '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[8]'
    click_element(selector)
    time.sleep(1)

    print('3')
    # choose from network
    selector = nitro_chains[fromChain]
    click_element(selector)


    print('4')
    # choose token input tiket
    selector = '/html/body/div[2]/div[3]/div/div/div[1]/div[1]/input'
    send_keys_to_element(selector, network_tiker[fromChain])
    time.sleep(10)

    print('5')
    # select token
    selector = '/html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[2]'
    click_element(selector)
    time.sleep(2)

    print('6')
    # open list network toChain
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[2]'
    click_element(selector)
    time.sleep(1)

    print('7')
    # open all networks
    selector = '/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button[8]'
    click_element(selector)

    print('8')
    # choose from network
    selector = nitro_chains[toChain]
    click_element(selector)
    time.sleep(2)

    print('9')
    # choose token input tiket
    selector = '/html/body/div[2]/div[3]/div/div/div[1]/div[1]/input'
    send_keys_to_element(selector, network_tiker[toChain])
    time.sleep(10)

    print('10')
    # select token
    selector = '/html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[2]'
    click_element(selector)
    time.sleep(2)

    print('11')
    # input token value
    wallet_balance = check_wallet_balance(rpc_chain[fromChain])
    coff = random.uniform(0.8,0.95)
    value = round(wallet_balance * coff / 10**18, 3)

    print('12')
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div[1]/div[1]/input'
    send_keys_to_element(selector, value)
    time.sleep(7)

    print('13')
    # switch network if need
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[4]/div/button'
    try_click_element_and_continue(selector)
    time.sleep(1)

    print('14')
    # tap continue
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[4]/div/button'
    click_element(selector)
    time.sleep(5)

    print('15')
    # tap transfer
    selector = '//*[@id="root"]/div/div[4]/div[3]/div[1]/div/div/div[2]/div[4]/div/button'
    click_element(selector)

    time.sleep(3)
    print('16')
    create_sign_sent_rabby_full_window(driver, 2, 1)

    long_pause()
    print('17')
    driver.get(project_link)
    time.sleep(5)


def nitro_choose_to_chain(fromChain):
    db_ch = list(nitro_chains)
    db_ch.remove(fromChain)
    random_chain = random.choice(db_ch)
    return random_chain


def nitro_reload_err(driver):
    driver.get(project_link)
    try:
        driver.switch_to.window(driver.window_handles[2])
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
    except:
        pass
    time.sleep(5)

# работа с площадкой
def project_work(driver):
    project_connect_wallet(driver)
    count_swaps = 0
    max_swaps = random.randint(4, 6)

    while max_swaps > count_swaps:
        try:
            mid_pause()
            print('Номер свапа: ', count_swaps + 1)
            fromChain = max_balance()
            toChain = nitro_choose_to_chain(fromChain)

            nitro_choose_routes(driver,fromChain, toChain)

            count_swaps = count_swaps + 1
            print('Закончил: ', count_swaps - 1)
        except:
            print('Ошибка')
            nitro_reload_err(driver)

    print('DONE')


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    global wait
    wait = WebDriverWait(driver, timeout=5)

    rabby_wallet_login(driver)

    project_work(driver)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(3000)
