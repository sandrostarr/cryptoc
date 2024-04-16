import os

from chrome_crawler_berachain import click_element

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


def layer3_quest_15_intro_to_paragraph(driver):
    driver.get(url_quest_15)

    # click introducing cubes
    selector = '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/button'
    click_element(selector)

    # click continue (x9)
    for x in range(0, 9):
        selector = '//*[@id="radix-:rq:"]/div/div[3]/div/div/div/button'
        click_element(selector)
