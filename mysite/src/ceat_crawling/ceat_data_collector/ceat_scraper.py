import os
import sys
import time
import random

from ..ceat_common.ceat_common import *

import pandas as pd
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import subprocess
from webdriver_manager.firefox import GeckoDriverManager
class ceat_scraper:
    def __init__(self, url):
        self.crawler = ceat_crawler(url)
        self.parser = ceat_parser()

class ceat_crawler():

    def __init__(self, url):
        self.url = url

    def sleep_random(self):
        time.sleep(random.uniform(2, 4))

    def init_crawler(self):
        # option = Options()
        # # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # # subprocess.Popen(r'C:\Program Files\Mozilla Firefox\firefox.exe -marionette -start-debugger-server 2828 //only use 2828')
        # option.add_argument('-profile.set_preference("dom.webdriver.enabled", False)')
        # self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(),option=option))
        #
        # # self.driver.options.add_argument(r'--profile.set_preference("dom.webdriver.enabled", False)')

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(time_to_wait=5)

    def open_crawler(self, url=None):
        if url == None:
            self.driver.get(self.url)
        else:
            self.driver.get(url)

        self.sleep_random()

        self.driver.maximize_window()
        # self.driver.minimize_window()

    def close_crawler(self):
        self.driver.quit()

    def open_tab(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url)
        self.sleep_random()

    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def find_elements(self, by, elements_key):
        try:
            elements = ""

            if by == "class":
                elements = self.driver.find_elements(By.CLASS_NAME, elements_key)
            elif by == "tag":
                elements = self.driver.find_elements(By.TAG_NAME, elements_key)
            elif by == "id":
                elements = self.driver.find_elements(By.ID, elements_key)
            elif by == "css_selector":
                elements = self.driver.find_elements(By.CSS_SELECTOR, elements_key)
            elif by == "xpath":
                elements = self.driver.find_elements(By.XPATH, elements_key)
            elif by == "partial_link_text":
                elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, elements_key)
            else:
                print("Wrong by value")

            return elements
        except NoSuchElementException:
            print("{}".format(NoSuchElementException))
            return False

    def find_element(self, by, element_key):
        try:
            element = ''

            if by == "class":
                element = self.driver.find_element(By.CLASS_NAME, element_key)
            elif by == "tag":
                element = self.driver.find_element(By.TAG_NAME, element_key)
            elif by == "id":
                element = self.driver.find_element(By.ID, element_key)
            elif by == "css_selector":
                element = self.driver.find_element(By.CSS_SELECTOR, element_key)
            elif by == "xpath":
                element = self.driver.find_element(By.XPATH, element_key)
            elif by == "partial_link_text":
                element = self.driver.find_element(By.PARTIAL_LINK_TEXT, element_key)
            else:
                print("Wrong by value")

            return element
        except NoSuchElementException:
            print("{}".format(NoSuchElementException))
            return False

    def click_btn(self, by, element_key, mode, desc):
        print("click_btn() : {}".format(desc))

        try:
            element = self.find_element(by, element_key)
            if mode == "click":
                if element is False:
                    return False
                else:
                    element.click()
            elif mode == "send_key":
                if element is False:
                    return False
                else:
                    element.send_keys(Keys.ENTER)
            else:
                print("Wrong by mode")
        except ElementNotInteractableException:
            print("{}".format(ElementNotInteractableException))
            return False

        self.sleep_random()

    def search_item(self, by, element_key, item):
        print("search_item() : {}".format(item))

        try:
            search_box = self.find_element(by, element_key)
            search_box.clear()
            search_box.send_keys(item)
            search_box.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("{}".format(ElementNotInteractableException))
            return False

        self.sleep_random()

    def scroll(self):
        # 최초 페이지 스크롤 설정
        # 스크롤 시키지 않았을 때의 전체 높이
        last_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            # 윈도우 창을 0에서 위에서 설정한 전체 높이로 이동
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            self.sleep_random()
            # 스크롤 다운한 만큼의 높이를 신규 높이로 설정
            new_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            # 직전 페이지 높이와 신규 페이지 높이 비교
            if new_page_height == last_page_height:
                self.sleep_random()
                # 신규 페이지 높이가 이전과 동일하면, while문 break
                if new_page_height == self.driver.execute_script("return document.documentElement.scrollHeight"):
                    break
            else:
                last_page_height = new_page_height

        self.sleep_random()

    def refresh(self):
        self.driver.refresh()
        self.sleep_random()

    def get_cur_url(self):
        return self.driver.current_url

class ceat_parser:
    # logger = ''
    # data_series = ''

    def findAttrs(self, web_element, tag_name, attrs={}):
        html = BeautifulSoup(web_element.get_attribute('innerHTML'), 'html.parser')
        return html.find_all(tag_name, attrs)

    def findAttr(self, web_element, tag_name, attrs={}):
        html = BeautifulSoup(web_element.get_attribute('innerHTML'), 'html.parser')
        return html.find(tag_name, attrs)

    def select(self, web_element, css_selector):
        html = BeautifulSoup(web_element.get_attribute('innerHTML'), 'html.parser')
        return html.select(css_selector)

    def select_one(self, web_element, css_selector):
        html = BeautifulSoup(web_element.get_attribute('innerHTML'), 'html.parser')
        return html.select_one(css_selector)

    def find_elements(self, web_element, by, elements_key):
        try:
            elements = ""

            if by == "class":
                elements = web_element.find_elements(By.CLASS_NAME, elements_key)
            elif by == "tag":
                elements = web_element.find_elements(By.TAG_NAME, elements_key)
            elif by == "id":
                elements = web_element.find_elements(By.ID, elements_key)
            elif by == "css_selector":
                elements = web_element.find_elements(By.CSS_SELECTOR, elements_key)
            elif by == "xpath":
                elements = web_element.find_elements(By.XPATH, elements_key)
            elif by == "partial_link_text":
                elements = web_element.find_elements(By.PARTIAL_LINK_TEXT, elements_key)
            else:
                print("Wrong by value")

            return elements
        except NoSuchElementException:
            print("{}".format(NoSuchElementException))
            return False

    def find_element(self, web_element, by, element_key):
        try:
            element = ''

            if by == "class":
                element = web_element.find_element(By.CLASS_NAME, element_key)
            elif by == "tag":
                element = web_element.find_element(By.TAG_NAME, element_key)
            elif by == "id":
                element = web_element.find_element(By.ID, element_key)
            elif by == "css_selector":
                element = web_element.find_element(By.CSS_SELECTOR, element_key)
            elif by == "xpath":
                element = web_element.find_element(By.XPATH, element_key)
            elif by == "partial_link_text":
                element = web_element.find_element(By.PARTIAL_LINK_TEXT, element_key)
            else:
                print("Wrong by value")

            return element
        except NoSuchElementException:
            print("{}".format(NoSuchElementException))
            return False

    def click_btn(self, web_element, mode, desc):
        print("click_btn() : {}".format(desc))

        try:
            if mode == "click":
                if web_element is False:
                    return False
                else:
                    web_element.click()
            elif mode == "send_key":
                if web_element is False:
                    return False
                else:
                    web_element.send_keys(Keys.ENTER)
            else:
                print("Wrong by mode")
        except ElementNotInteractableException:
            print("{}".format(ElementNotInteractableException))
            return False

    # def __init__(self, data = None, data_name = None):
    #     print("init")
    #     # self.data_series = pd.Series([], dtype=float)
    #     #
    #     # if data is not None and data_name is not None:
    #     #     self.data_series[data_name] = data
    #     # else:
    #     #     self.logger.logger.debug("Data empty, Need to add data")
    #
    # def add_dataframe(self, data_name):
    #     self.data_series[data_name] = pd.DataFrame()
    #
    # def del_dataframe(self, data_name):
    #     del self.data_series[data_name]
    #
    # def read_to_excel(self, file_full):
    #     return pd.read_excel(file_full)
    #
    # def list_to_series(self, list):
    #     return pd.Series(list)
    #
    #
    #
    # def print_dataframe(self, name):
    #     print("================================================")
    #     print(self.data_series[name])
    #     print("================================================")



