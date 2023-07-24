from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def main():

    url = "https://kin.naver.com/qna/list.naver"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    test_list = driver.find_elements(By.CLASS_NAME,'title')
    for text in test_list:
        print(text.find_element(By.TAG_NAME,'a').text)

main()