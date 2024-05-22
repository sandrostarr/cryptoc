import time

from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as ec


def click_element(wait, element_selector: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    time.sleep(1)
    element.click()
    time.sleep(0.5)


# функция для клика на элементы, которых может не быть на странице и которые можно пропустить и не падать в фатал
def try_click_element_and_continue(wait, element_selector: str, extra_sleep: int = 0):
    try:
        click_element(wait, element_selector, extra_sleep)
    except TimeoutException:
        pass


def send_keys_to_element(wait, element_selector: str, input_text: str, extra_sleep: int = 0):
    if extra_sleep > 0:
        time.sleep(extra_sleep)

    element = wait.until(ec.presence_of_element_located((By.XPATH, element_selector)))
    element.send_keys(input_text)
