import os

from dotenv import load_dotenv

from lib.form_functions import click_element
from lib.form_functions import send_keys_to_element

load_dotenv()


# функция для логина в rabby wallet
def rabby_wallet_login(driver, wait):
    # open extension create password page
    driver.get("chrome-extension://" + os.getenv('RABBY_EXTENSION_ID') + "/index.html")

    # click next
    selector = '//*[@id="root"]/div/section/footer/button'
    click_element(wait, selector)

    # click get ready
    selector = '//*[@id="root"]/div/section/footer/a/button'
    click_element(wait, selector)

    # import private key
    selector = '//*[@id="root"]/div/div[3]/div[2]/div[2]'
    click_element(wait, selector)

    # create pass
    selector = '//*[@id="password"]'
    send_keys_to_element(wait, selector, os.getenv('WALLET_PASSWORD'))

    # confirm pass
    selector = '//*[@id="confirmPassword"]'
    send_keys_to_element(wait, selector, os.getenv('WALLET_PASSWORD'))

    # click next button
    selector = '//*[@id="root"]/div/div/div/form/div[3]/button'
    click_element(wait, selector)

    # send private key
    selector = '//*[@id="key"]'
    send_keys_to_element(wait, selector, os.getenv('PRIVATE_KEY'))

    # click confirm button
    selector = '//*[@id="root"]/div/form/div[3]/div/button'
    click_element(wait, selector)
