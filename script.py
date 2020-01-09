# -*- coding: utf-8 -*-

import json
import asyncio
from urllib.parse import urljoin
from selenium.webdriver import chrome, Chrome
from selenium.common.exceptions import NoSuchElementException

class ChromeDriver:
    def __init__(self):
        self.options = self.get_options()
        self.driver = Chrome(chrome_options=self.options)
        self.implicitly_wait(10)

    def __getattr__(self, attr):
        return getattr(self.driver, attr)

    # overwrite
    def get(self, url, cookies=None, refresh=True):
        self.driver.get(url)
        if cookies is not None:
            for name, value in cookies.items():
                self.driver.add_cookie({
                    'name': name,
                    'value': value
                })
            if refresh:
                self.refresh()

    def get_options(self):
        options = chrome.options.Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--proxy-server=http://127.0.0.1:10809')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')
        return options

class HaremScript:
    URL = {
        'index': 'https://eroges.gayharem.com/',
        'arena': 'https://eroges.gayharem.com/arena.html'
    }

    SETTINGS = {
        'battle': {
            'duration': 300
        }
    }

    def __init__(self):
        with open('cookies.json') as f:
            self.cookies = json.load(f)

    async def run(self):
        try:
            while True:
                self.run_battle()
                await asyncio.sleep(self.SETTINGS['battle']['duration'])
        except KeyboardInterrupt:
            pass

    def run_battle(self):
        driver = self.get_driver()
        self.battle(driver)
        driver.quit()

    def get_driver(self):
        driver = ChromeDriver()
        driver.get(self.URL['index'], self.cookies, False)
        return driver

    def battle(self, driver):
        driver.get(self.URL['arena'])
        while True:
            for opponent in driver.find_elements_by_css_selector('.one_opponent'):
                try:
                    name = opponent.find_element_by_css_selector('div.name').text
                    opponent.find_element_by_css_selector('button.blue_text_button').click()
                    driver.find_element_by_css_selector('button.green_button_L[rel=launch]').click()
                    driver.find_element_by_css_selector('button.blue_text_button[rel=skip]').click()
                    driver.find_element_by_css_selector('button.blue_button_L[confirm_blue_button]').click()
                    print('[+] A battle with %s has been finished.' % name)
                    break
                except NoSuchElementException:
                    pass
            else:
                print('[-] No one could be battled.')
                break

def main():
    task = HaremScript().run()
    asyncio.run(task)

if __name__ == '__main__':
    main()