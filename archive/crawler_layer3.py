import os
import time
import undetected_chromedriver as uc

from dotenv import load_dotenv
from selenium import webdriver
from fake_useragent import UserAgent
from lib.proxy import get_plugin_file as plugin_file
from selenium.webdriver.support.wait import WebDriverWait

from lib.rabby_connector import rabby_wallet_login

from lib.form_functions import click_element
from lib.form_functions import send_keys_to_element
from lib.form_functions import try_click_element_and_continue

load_dotenv()

url_quest_1 = os.getenv('URL_QUEST_1')
url_quest_15 = os.getenv('URL_QUEST_15')
url_quest_66 = os.getenv('URL_QUEST_66')
url_quest_101 = os.getenv('URL_QUEST_101')
url_quest_34 = os.getenv('URL_QUEST_34')
url_quest_35 = os.getenv('URL_QUEST_35')
url_quest_44 = os.getenv('URL_QUEST_44')
url_quest_58 = os.getenv('URL_QUEST_58')
url_quest_13 = os.getenv('URL_QUEST_13')
url_quest_51 = os.getenv('URL_QUEST_51')
url_quest_17 = os.getenv('URL_QUEST_17')
url_quest_28 = os.getenv('URL_QUEST_28')
url_quest_29 = os.getenv('URL_QUEST_29')
url_quest_64 = os.getenv('URL_QUEST_64')
url_quest_20 = os.getenv('URL_QUEST_20')
url_quest_19 = os.getenv('URL_QUEST_19')
url_quest_47 = os.getenv('URL_QUEST_47')
url_quest_49 = os.getenv('URL_QUEST_49')
url_quest_50 = os.getenv('URL_QUEST_50')
url_quest_41 = os.getenv('URL_QUEST_41')

metamask_pw = os.getenv('METAMASK_PW')

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

    # undetected_chromedriver (для того, чтобы cloudflare не палил нас)
    driver = uc.Chrome(options=options)
    return driver


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


# функция для выполнения первого квеста в layer3
def layer3_connect_wallet_and_login(driver):
    driver.get(url_quest_1)

    # connect wallet
    selector = '//*[@id="__next"]/div/div/div/div[2]/header/div/div[2]/div/div[2]/div[1]/button'
    click_element(selector)

    # rabby wallet
    selector = '//*[@id="radix-:rg:-content-evm"]/div/button[1]'
    click_element(selector, 1)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    # rabby wallet click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(1)

    driver.switch_to.window(driver.window_handles[2])
    create_sign_sent_rabby(driver, 1)


def layer3_quest_1(driver):
    driver.get(url_quest_1)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # start part 1
    selector = '/html/body/div[1]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # click continue (x6)
    for x in range(0, 6):
        selector = '/html/body/div[1]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
        click_element(selector)

    # open layer3 bridge
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[3]/div/div/a/button'
    click_element(selector)

    time.sleep(1)
    # переход на layer3 bridge
    driver.switch_to.window(driver.window_handles[2])

    # TODO здесь должна быть свапалка
    print('Свапалка, здесь нужно выбрать валюты и что-то делать')
    time.sleep(3000)

    # review route
    selector = '/html/body/div[1]/div/div/div/div[3]/div[1]/section[2]/button'
    click_element(selector)

    # approve transfer
    selector = '/html/body/div[1]/div/div/div/div[3]/div/section/div/div/div/button'
    click_element(selector)


def layer3_quest_15(driver):
    driver.get(url_quest_15)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # start part 1
    selector = '/html/body/div[1]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # click continue (x3)
    for x in range(0, 3):
        selector = '/html/body/div[1]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
        click_element(selector)

    # part 2 open paragraph
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(1)

    # переход на параграф
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div/div[2]/div/span'
    click_element(selector)

    selector = '//*[@id="para-document"]/div/div/div[1]/div[1]/a/div/div/div[1]/img'
    click_element(selector)

    selector = '//*[@id="para-document"]/div/div/div/div[2]/header/div/div/div/aside/div[2]/div[4]/div[1]/button'
    click_element(selector)

    selector = '//*[@id="para-document"]/div/div/div/div[2]/header/div/div/div/aside/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div/div/div[1]/div/div/button'
    click_element(selector)

    selector = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[3]/div[2]/div/div/div[3]/button'
    click_element(selector)

    # click wallet
    selector = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/button'
    click_element(selector)

    # при открытии окна кошелька нужна небольшая пауза перед переключением на другое окно, т.к. оно не сразу появляется
    time.sleep(2)
    # переключение на рабби
    driver.switch_to.window(driver.window_handles[3])

    # коннект в рабби
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(2)

    # sign msg
    driver.switch_to.window(driver.window_handles[2])
    selector = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/div[2]/button[1]'
    click_element(selector)
    time.sleep(2)

    # sing and create
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    time.sleep(2)

    # click collect
    selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[4]/div[1]/button'
    click_element(selector)

    # click collect
    selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div/div[1]/div/button'
    click_element(selector)

    time.sleep(3)

    # закрыть окно парагарафа
    driver.close()

    time.sleep(1)
    # вернуться в окно layer3
    driver.switch_to.window(driver.window_handles[1])

    # verif этап 2
    selector = '/html/body/div[1]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
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


def layer3_quest_66(driver):
    driver.get(url_quest_66)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # click continue
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # click continue
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # go to zora mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(1)

    # connect rabby to zora
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    time.sleep(2)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div/button'
    click_element(selector)

    selector = '/html/body/div[2]/div/div[2]/div/div/div/div/div/div/div/div[3]/a'
    click_element(selector)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[3])

    time.sleep(10)

    # create_sign_sent_rabby()
    time.sleep(1)
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(1)

    # close rabby back to layer3
    driver.switch_to.window(driver.window_handles[2])
    driver.close()

    time.sleep(1)

    driver.switch_to.window(driver.window_handles[1])

    time.sleep(1)

    # verif mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # claim box
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    time.sleep(1)
    # rabby sign
    driver.switch_to.window(driver.window_handles[2])

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    time.sleep(2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_101(driver):
    driver.get(url_quest_101)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    time.sleep(.1)
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # step 2
    # go to zora
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(.1)
    # switch to new window
    driver.switch_to.window(driver.window_handles[2])

    # connect to zora
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    # choose rabby
    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(1)
    # switch to rabby
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint collection
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    # chng netw
    selector = '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/button'
    click_element(selector)

    # mint
    selector = '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/button'
    click_element(selector)

    time.sleep(2)
    # switch to rabbby
    driver.switch_to.window(driver.window_handles[3])

    time.sleep(1)
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(1)
    # swtch to zora
    driver.switch_to.window(driver.window_handles[2])

    driver.close()
    time.sleep(.5)

    # #nack to layer
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(10)

    # step 3
    # verif btn
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # step 4
    # claim box
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    time.sleep(1)

    # swtch to rabby
    driver.switch_to.window(driver.window_handles[2])

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_34(driver):
    driver.get(url_quest_34)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # step 1 verif
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    time.sleep(.2)
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # step 2
    # go to zora
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])

    # mint btn to connect
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)
    time.sleep(.1)

    # select rabby
    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    # swtch rabby
    driver.switch_to.window(driver.window_handles[3])
    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(2)

    # sign create
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint nft
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    time.sleep(2)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[4]/div/div/button'
    click_element(selector)
    time.sleep(.1)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[4]/div/div/button'
    click_element(selector)
    time.sleep(1.5)

    # to rabby
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(10)

    # close zora
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    time.sleep(.1)

    # back to l3
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)

    # verif quest
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(5)

    # step 4
    # switch chain
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)
    time.sleep(.2)

    # mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    # swtch to rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(.2)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_35(driver):
    driver.get(url_quest_35)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    # step2
    # step 2
    # go to zora
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])

    # mint btn to connect
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)
    time.sleep(.1)

    # select rabby
    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    # swtch rabby
    driver.switch_to.window(driver.window_handles[3])
    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(2)

    # sign create
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint nft
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div/button'
    click_element(selector)
    time.sleep(2)

    # to rabby
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(10)

    # close zora
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    time.sleep(.1)

    # back to l3
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)

    # verif quest
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(5)

    # step 4
    # switch chain
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)
    time.sleep(.2)

    # mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    # swtch to rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_44(driver):
    driver.get(url_quest_44)

    #step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    # step 2
    # go to sound
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])

    # mint btn to connect
    selector = '//*[@id="right-container"]/div/div/div[2]/div/div/div/div[3]/button'
    click_element(selector)
    time.sleep(.5)
    # TODO дальше не тестировал не видит подключения к кошелькам
    # select rabby
    selector = ''
    click_element(selector)
    time.sleep(.2)

    selector = '//*[@id="dynamic-modal"]/div//div/div/div[2]/div[2]/div/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    # swtch rabby
    driver.switch_to.window(driver.window_handles[3])
    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(2)

    # sign create
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint nft
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[3]/div[3]/div/div/button'
    click_element(selector)
    time.sleep(2)

    # to rabby
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(10)

    # close zora
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    time.sleep(.1)

    # back to l3
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)

    # verif quest
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(5)

    # step 4
    # switch chain
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)
    time.sleep(.2)

    # mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    # swtch to rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_58(driver):
    driver.get(url_quest_58)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    # step2
    # step 2
    # go to zora
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])

    # mint btn to connect
    selector = '//*[@id="navigation"]/nav/div[3]/button[2]'
    click_element(selector)
    time.sleep(.1)

    # select rabby
    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    # swtch rabby
    driver.switch_to.window(driver.window_handles[3])
    # connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(2)

    # sign create
    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # mint nft
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div/div[1]/div[1]/div'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[6]/button'
    click_element(selector)
    time.sleep(.5)

    selector = '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[6]/button'
    click_element(selector)
    time.sleep(2)

    # to rabby
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(10)

    # close zora
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    time.sleep(.1)

    # back to l3
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)

    # verif quest
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(5)

    # step 4
    # switch chain
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)
    time.sleep(.2)

    # mint
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    # swtch to rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_13_51(driver):
    driver.get(url_quest_13)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # step 2 mintfun
    # go mintgun
    time.sleep(2)
    driver.get('https://mint.fun/base/0x7E0b40AF1D6f26F2141b90170C513e57b5EdD74e')

    # connect rabb
    selector = '//*[@id="__next"]/div[3]/div[2]/nav/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__CONNECTKIT__"]/div/div/div/div[2]/div[2]/div[4]/div/div/div/div[1]/button[3]'
    click_element(selector)
    time.sleep(1)

    # on rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(.5)

    driver.switch_to.window(driver.window_handles[1])

    # change netw
    selector = '//*[@id="__next"]/div[3]/div[2]/main/div/div[2]/div[2]/div[3]/div[1]/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div[3]/div[2]/main/div/div[2]/div[2]/div[3]/div[1]/button'
    click_element(selector)
    time.sleep(1)

    # appr on rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(10)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.2)

    driver.get(url_quest_13)

    # verif on l3
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # step claim
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(.5)

    # onrabby
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.3)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.3)

    driver.get(url_quest_51)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # verif
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(5)

    # claim rew
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_17(driver):
    driver.get(url_quest_17)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)
    time.sleep(.1)

    # step 2
    # swap om l3
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)
    time.sleep(.5)

    # chng netw
    driver.switch_to.window(driver.window_handles[2])
    selector = '//*[@id="__next"]/div/div/div/div[3]/div[1]/div[1]/section[1]/div/button/span/span'
    click_element(selector)

    # choose base
    selector = '//*[@id=":rt:"]/div/div[7]'
    click_element(selector)

    # swap from eth -> usdc
    selector = '//*[@id="__next"]/div/div/div/div[3]/div[1]/div[1]/section[2]/div[1]/section/div[1]/div[1]/div/input'
    send_keys_to_element(selector, '0.001')
    time.sleep(2)

    # route
    selector = '//*[@id="__next"]/div/div/div/div[3]/div[1]/section[2]/button'
    click_element(selector)
    time.sleep(1)

    # stch to base
    selector = '//*[@id="__next"]/div/div/div/div[3]/div/section/div/div/div/button'
    click_element(selector)
    time.sleep(2)

    # swap
    selector = '//*[@id="__next"]/div/div/div/div[3]/div/section/div/div/div/button'
    click_element(selector)
    time.sleep(1)

    # to rabb
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(0.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(.3)
    driver.close()

    # return to quest
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(8)

    # verif
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # swtch to base

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)
    # claim cube
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    # to rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(.5)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_28(driver):
    driver.get(url_quest_28)

    # open sound
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[1]/div/div/a/button'
    click_element(selector)

    # переход на параграф
    driver.switch_to.window(driver.window_handles[2])

    time.sleep(5)

    # click collect
    selector = '//*[@id="right-container"]/div/div/div[2]/div/div/div/div[3]/button'
    click_element(selector)

    # click rabby wallet
    selector = '//*[@id="dynamic-modal"]/div//div/div/div[2]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[2]/button[1]'
    click_element(selector)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[3])

    # rabby wallet click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(1)

    driver.switch_to.window(driver.window_handles[3])
    create_sign_sent_rabby(driver, 1)


def layer3_quest_29(driver):
    driver.get(url_quest_29)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # click continue
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    # click continue
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # open zora
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    # переход на zora
    driver.switch_to.window(driver.window_handles[2])

    time.sleep(1)

    # click collect
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    time.sleep(5)
    # click rabby wallet
    selector = '//*[@id="privy-modal-content"]/div/div[1]/div[3]/div/button[1]'
    click_element(selector)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[3])

    # rabby wallet click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    time.sleep(5)

    driver.switch_to.window(driver.window_handles[3])

    create_sign_sent_rabby(driver, 2)

    # click collect
    selector = '//*[@id="__next"]/div/div[3]/div[2]/div[2]/div/div[4]/div[1]/div[1]/div/button'
    click_element(selector)

    # click collect
    selector = '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/button'
    click_element(selector)

    # close zora
    driver.close()

    time.sleep(1)
    # вернуться в окно layer3
    driver.switch_to.window(driver.window_handles[1])

    # verify
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)


def layer3_quest_64(driver):
    driver.get(url_quest_64)

    # TODO скрипт для запуска уже пройденных этапов с начала
    selector = '/html/body/div[1]/div/div/div/div[3]/section[1]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # open jumper
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div/div/div/a/button'
    click_element(selector)

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[2])

    # click get started
    selector = '/html/body/div[2]/div/div/button'
    click_element(selector)

    # click connect wallet
    selector = '//*[@id=":r2:"]'
    click_element(selector)

    # click rabby wallet
    selector = '//*[@id="main-burger-menu"]/li[5]'
    click_element(selector)

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[3])

    # rabby click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])

    # click change token
    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[1]/button[2]'
    click_element(selector)

    # click usdc
    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[2]/ul/li[2]'
    click_element(selector)

    # send 0.1 to toeken amount
    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[2]/div/div/div[1]/input'
    send_keys_to_element(selector, '0.1')

    time.sleep(3)

    # click review swap
    selector = '/html/body/div[3]/div/div/div[1]/div/div/div[2]/div/div[3]/button[1]'
    click_element(selector)

    # click start swapping
    selector = '/html/body/div[3]/div/div/div[1]/div/div/div[2]/div/div[2]/button'
    click_element(selector)

    # click start swapping
    selector = '/html/body/div[3]/div/div/div[1]/div/div[2]/div[3]/div/div[6]/button[2]'
    click_element(selector)

    create_sign_sent_rabby_full_window(driver, 3, 2)

    time.sleep(20)

    # click done
    selector = '/html/body/div[3]/div/div/div[1]/div/div[2]/div[3]/div/div[4]/button'
    click_element(selector)

    # close jumper windows
    driver.close()

    time.sleep(1)
    # return to layer3
    driver.switch_to.window(driver.window_handles[1])

    # click verify
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button[2]'
    click_element(selector)

    # click switch to polygon
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)

    # click mint cube to claim
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    create_sign_sent_rabby_full_window(driver, 2, 1)

    # click continue
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/button'
    click_element(selector)


def layer3_quest_20(driver):
    driver.get(url_quest_20)
    time.sleep(2)
    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)
    time.sleep(0.5)

    # step 2
    # to aave
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    # connect to avve
    selector = '//*[@id="wallet-button"]'
    click_element(selector)

    selector = '/html/body/div[7]/div[3]/div[1]/button[1]'
    click_element(selector)
    time.sleep(1)

    # on rabby
    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(0.5)

    # back to aave
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)

    # switch to base
    selector = '//*[@id="mui-1"]'
    click_element(selector)
    time.sleep(0.5)

    selector = '//*[@id="menu-"]/div[3]/ul/li[6]'
    click_element(selector)
    time.sleep(2)

    # cook otp
    selector = '//*[@id="rcc-decline-button"]'
    click_element(selector)

    driver.get(
        'https://app.aave.com/reserve-overview/?underlyingAsset=0x833589fcd6edb6e08f4c7c32d4f71b54bda02913&marketName=proto_base_v3')
    time.sleep(2)

    # usdc supply
    selector = '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/button'
    click_element(selector)

    # swtch to base
    selector = '/html/body/div[8]/div[3]/div[1]/div/p/button'
    click_element(selector)

    # input usdc
    selector = '/html/body/div[8]/div[3]/div[1]/div[2]/div[1]/div[1]/input'
    send_keys_to_element(selector, '2')

    # approve
    selector = '/html/body/div[8]/div[3]/div[3]/button[1]'
    click_element(selector)

    # on rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(2)

    # ignore all
    selector = '//*[@id="root"]/div/div[2]/section/div[4]/span[2]'
    click_element(selector)

    # approve
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    # sent
    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(7)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)

    # supp tx
    selector = '/html/body/div[8]/div[3]/div[3]/button'
    click_element(selector)
    time.sleep(2)

    # rabby sign
    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(2)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(8)

    # back to l3 verif
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(.5)

    # withdraw form aave
    driver.switch_to.window(driver.window_handles[2])

    driver.get('https://app.aave.com/')
    time.sleep(2)

    # withdraw
    selector = '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/div[5]/button[2]'
    selector = '/html/body/div[1]/main/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div[2]/div[5]/button[2]'
    click_element(selector)

    # max
    selector = '/html/body/div[9]/div[3]/div[3]/div[2]/div[2]/button'
    click_element(selector)

    # withdraw
    selector = '/html/body/div[9]/div[3]/div[4]/button'
    click_element(selector)
    time.sleep(3)

    driver.switch_to.window(driver.window_handles[3])
    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(2)

    driver.close()

    # collect cube
    driver.switch_to.window(driver.window_handles[1])

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)
    time.sleep(.5)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])


def layer3_quest_19(driver):
    #TODO нужен USDCb
    driver.get(url_quest_19)
    time.sleep(1)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div/div/div/a/button'
    click_element(selector)

    # stg
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(2)

    # connect
    selector = '//*[@id="__next"]/header[1]/div/div[3]/button[2]'
    click_element(selector)

    selector = '/html/body/div[2]/div[3]/div/div[2]/div/a[4]'
    click_element(selector)

    # on rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(1)

    selector = '/html/body/div/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    # back stg
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(2)


def layer3_quest_47(driver):
    driver.get(url_quest_47)

    # # step 1
    # selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    # click_element(selector)

    # step 2
    # to compound
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)
    time.sleep(1)

    # on compaund
    driver.switch_to.window(driver.window_handles[2])

    # connect
    selector = '//*[@id="root"]/header/div[1]/div/div[2]/div/div[2]/div/div'
    click_element(selector)

    # choose rabby
    selector = '/html/body/div/div[2]/div[2]/div[4]/div[1]'
    click_element(selector)

    # on rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(2)

    selector = '/html/body/div/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)
    time.sleep(3)

    # to comp
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(5)

    #supp eth
    #TODO не видит кнопу  supply
    selector = '//*[@id="root"]/div[4]/div[1]/div[2]/div/button[1]/label'
    # click_element(selector)

    # # input value
    # selector = '/html/body/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/div[2]/input'
    # send_keys_to_element(selector, '0.001')


def layer3_quest_49(driver):
    driver.get(url_quest_49)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)
    time.sleep(1)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # step 2
    # to seamless
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[2]/div/div/a/button'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(5)

    driver.get(
        'https://legacy.seamlessprotocol.com/reserve-overview/?underlyingAsset=0x4200000000000000000000000000000000000006&marketName=proto_base_v3')
    time.sleep(4)

    # connect
    selector = '//*[@id="wallet-button"]'
    click_element(selector)

    # rabby
    selector = '/html/body/div[8]/div[3]/div[1]/button[1]'
    click_element(selector)

    # on rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(2)

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    # back
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(10)

    # ETH
    selector = '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div[1]/div/button[2]'
    click_element(selector)

    # supply
    selector = '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/button'
    click_element(selector)

    # switch netw
    selector = '/html/body/div[8]/div[3]/div[1]/div/p/button'
    try_click_element_and_continue(selector)

    # inp ETH value
    selector = '/html/body/div[8]/div[3]/div[1]/div[2]/div[1]/div[1]/input'
    send_keys_to_element(selector, '0.001')

    # supp
    selector = '/html/body/div[8]/div[3]/div[3]/button'
    click_element(selector)

    create_sign_sent_rabby_full_window(driver, 3, 2)

    # verif
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(3)

    # wtihdraw from seal
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)

    # ok
    selector = '/html/body/div[8]/div[3]/div[2]/button'
    try_click_element_and_continue(selector)

    driver.get('https://legacy.seamlessprotocol.com/')
    time.sleep(3)

    selector = '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div[2]/div[5]/button[1]'
    click_element(selector)
    time.sleep(.5)

    # switch network
    selector = '/html/body/div[7]/div[3]/div[1]/div/p/button'
    try_click_element_and_continue(selector)

    # max
    selector = '/html/body/div[7]/div[3]/div[1]/div[2]/div[2]/button'
    click_element(selector)
    time.sleep(5)

    # approve
    selector = '/html/body/div[7]/div[3]/div[4]/button[1]'
    click_element(selector)
    time.sleep(2)

    create_sign_sent_rabby_full_window(driver, 3, 2)

    # withdraw
    selector = '/html/body/div[7]/div[3]/div[4]/button[2]'
    try_click_element_and_continue(selector)
    time.sleep(2)

    # withdraw 1
    selector = '/html/body/div[7]/div[3]/div[4]/button'
    try_click_element_and_continue(selector)
    time.sleep(2)

    create_sign_sent_rabby_full_window(driver, 3, 2)
    time.sleep(5)
    driver.close()

    # back to l3
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    # switch ntw
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)

    # claim
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # rabby
    create_sign_sent_rabby_full_window(driver, 2, 1)
    time.sleep(3)


def layer3_quest_50_40(driver):
    driver.get(url_quest_50)

    # step 1
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button'
    click_element(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button'
    click_element(selector)

    # step 2 check
    # TODO не прожал кнопку теперь не могу проверить оставить на потом для дебага
    time.sleep(5)
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # step 3 to uni
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div[3]/div/div/a/button'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)

    # connect uni
    selector = '//*[@id="root"]/span/span/div[1]/nav/div/div[3]/div/div[3]/div/button'
    click_element(selector)

    # choose rabby
    selector = '//*[@id="wallet-dropdown-scroll-wrapper"]/div/div/div[2]/div[1]/div/div[2]/button'
    click_element(selector)

    # connect rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(1)

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])

    # change to base
    selector = '//*[@id="root"]/span/span/div[1]/nav/div/div[3]/div/div[2]/div/div[1]/div/button'
    click_element(selector)

    selector = '//*[@id="root"]/span/span/div[1]/nav/div/div[3]/div/div[2]/div/div[2]/button[5]'
    click_element(selector)

    # USDC -> USDCb
    selector = '//*[@id="swap-currency-input"]/div/div[1]/div[2]/div/button'
    click_element(selector)

    selector = '//*[@id="token-search-input"]'
    send_keys_to_element(selector, 'USDC')
    time.sleep(3)

    # USDc
    selector = '/html/body/reach-portal[7]/div[2]/div/div/div/div/div[3]/div/div/div/div/div[2]'
    click_element(selector)


    # 2 choose
    selector = '//*[@id="swap-currency-output"]/div/div[1]/div[2]/div/button'
    click_element(selector)

    selector = '//*[@id="token-search-input"]'
    send_keys_to_element(selector, 'USDC')
    time.sleep(3)

    # USDCb
    selector = '/html/body/reach-portal[7]/div[2]/div/div/div/div/div[3]/div/div/div/div/div[3]'
    click_element(selector)

    # max
    selector = '//*[@id="swap-currency-input"]/div/div[2]/div/div[2]/button'
    click_element(selector)
    time.sleep(4)

    # swap
    selector = '//*[@id="swap-button"]'
    click_element(selector)
    time.sleep(1)

    # approve and swap
    selector = '//*[@id="confirm-swap-or-send"]'
    click_element(selector)

    # ignore all
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(1)

    selector = '//*[@id="root"]/div/div[2]/section/div[4]/span[2]'
    click_element(selector)
    time.sleep(1)

    create_sign_sent_rabby_full_window(driver,3,2)

    # swap on rabby
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(1)

    selector = '//*[@id="root"]/div/footer/div/section/div[4]/span[2]'
    click_element(selector)
    time.sleep(1)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(selector)
    time.sleep(1)

    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(3)

    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    click_element(selector)
    time.sleep(1)

    selector = '/html/body/div/div/div[2]/section/div[3]/div/button[1]'
    click_element(selector)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])
    driver.close()

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    # verif
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # claim
    # switch
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)

    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(1)

    create_sign_sent_rabby_full_window(driver,2,1)
    time.sleep(5)
    
def layer3_quest_41(driver):
    driver.get(url_quest_41)

    # to jumper
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[1]/div/div/div/a/button'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])
    time.sleep(1)


    selector = '//*[@id="connect-wallet-button"]'
    click_element(selector)
    time.sleep(1)


    selector = '//*[@id="main-burger-menu"]/li[5]'
    click_element(selector)
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[3])

    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[2])

    # choose token
    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[1]/button[1]'
    click_element(selector)
    time.sleep(2)

    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[2]/ul/li[2]'
    click_element(selector)

    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[1]/button[2]'
    click_element(selector)
    time.sleep(2)

    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[2]/ul/li[1]'
    click_element(selector)

    # max
    selector = '//*[@id="widget-scrollable-container-:r0:"]/div/div[2]/div/div[2]/div/div/div[1]/div/button'
    click_element(selector)
    time.sleep(4)

    # review
    selector = '//*[@id=":r12:"]'
    click_element(selector)
    time.sleep(2)

    # start
    selector = '//*[@id=":r19:"]'
    click_element(selector)
    time.sleep(2)

    # on rabby
    create_sign_sent_rabby_full_window(driver,3,2)
    time.sleep(8)

    # create_sign_sent_rabby_full_window(driver,3,2)
    time.sleep(3)


    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[3]/div/div/div/button[2]'
    click_element(selector)
    time.sleep(3)

    # claim
    # switch ntw
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/div/button'
    try_click_element_and_continue(selector)

    # claim
    selector = '//*[@id="__next"]/div/div/div/div[3]/section[2]/div/div[2]/div/div/div/button[2]'
    click_element(selector)

    # rabby
    create_sign_sent_rabby_full_window(driver, 2, 1)
    time.sleep(3)


def main():
    # генерация фейкового юзерагента
    useragent = UserAgent().getRandom
    driver = get_chromedriver(use_proxy=False, user_agent=None)

    # явное ожидание поиска элементов
    wait = WebDriverWait(driver, timeout=5)

    rabby_wallet_login(driver, wait)

    layer3_connect_wallet_and_login(driver)

    # base
    # layer3_quest_1(driver)
    # layer3_quest_15(driver)
    # layer3_quest_66(driver)
    # layer3_quest_28(driver)
    # layer3_quest_29(driver)
    # layer3_quest_101(driver)
    # layer3_quest_34(driver)
    # layer3_quest_35(driver)
    # layer3_quest_44(driver)
    # layer3_quest_58(driver)
    # layer3_quest_13_51(driver)
    # layer3_quest_17(driver)
    # layer3_quest_20(driver)
    # layer3_quest_19(driver)
    # layer3_quest_47(driver)
    # layer3_quest_50_40(driver)
    layer3_quest_41(driver)


    # polygon
    # layer3_quest_64(driver)

    # # читаем cookies из файла
    # with open(cookies, 'rb') as f:
    #     for cookie in pickle.load(f):
    #         driver.add_cookie(cookie)


if __name__ == '__main__':
    main()

    # временный костыль для дебага
    time.sleep(3000)
