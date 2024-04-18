import os
import time
import pyautogui

from crawler_layer3 import click_element

url_quest_1 = os.getenv('URL_QUEST_1')
url_quest_15 = os.getenv('URL_QUEST_15')


def layer3_quest_1_intro_to_cube(driver):
    # click introducing cubes
    selector = '//*[@id="__next"]/div/div/div[3]/div/div[2]/div[2]/div[1]'
    click_element(selector)

    # click continue (x9)
    for x in range(0, 9):
        selector = '//*[@id="radix-:rq:"]/div/div[3]/div/div/div/button'
        click_element(selector)


# функция для выполнения первого квеста в layer3
def layer3_connect_wallet_and_login(driver):
    driver.get(url_quest_1)

    # connect wallet
    selector = '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/button'
    click_element(selector)

    # rabby wallet
    selector = '//*[@id="radix-:rc:-content-evm"]/div/button[1]'
    click_element(selector, 1)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    # rabby wallet click connect
    selector = '//*[@id="root"]/div/div/div/div/div[3]/div/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])

    # log in to start
    selector = '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/button'
    click_element(selector)

    # rabby wallet
    selector = '//*[@id="radix-:ri:-content-evm"]/div/button[1]'
    click_element(selector, 2)

    time.sleep(2)

    driver.switch_to.window(driver.window_handles[2])

    # rabby wallet click sign and create
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button'
    click_element(selector)

    # rabby wallet click confirm
    selector = '//*[@id="root"]/div/footer/div/section/div[3]/div/button[1]'
    click_element(selector)

    driver.switch_to.window(driver.window_handles[1])

    time.sleep(3)

    # click captcha
    pyautogui.click(740, 593)


def layer3_quest_15(driver):
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
    # #collect
    # driver.switch_to.window(driver.window_handles[2])
    # selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[3]/div[1]/button'
    # click_element(selector)
    #
    # selector = '//*[@id="para-document"]/div[1]/div/div/div[2]/header/div/div/div/aside/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[1]/div/button'
    # click_element(selector)
    # time.sleep(3)
    #
    # # sing and create
    # driver.switch_to.window(driver.window_handles[3])
    #
    # selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button'
    # click_element(selector)
    # # sent
    # selector = '//*[@id="root"]/div/div[2]/section/div[3]/div/button[1]'
    # click_element(selector)

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
