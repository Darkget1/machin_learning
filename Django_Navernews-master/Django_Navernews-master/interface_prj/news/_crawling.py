import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
from datetime import datetime, timedelta

def extract_date(mystr):
    mystr = mystr.replace('<span class="bar"></span>','')
    return mystr

def check_today(indx):
    myday = datetime.today()-timedelta(indx)
    return myday.strftime("%Y%m%d%H%M%S")[0:8]

def new100_parsing(sid1,sid2):
    # 네이버 뉴스는 뉴스목록을 tb class= content로 하고 ul로 type06_headline , type06 상위10개 하위10개로 나눠놨음
    # 실행중에 가져올 title 리스트
    title=[]
    desc =[]
    writer =[]
    
    # 
    content= {}
    titles = []
    links = []
    dates = []
    descs=[]
    writers=[]
    
    indx = 0
    pindx=1
    maxPage =0

    while (len(title)) <100:    
        
        url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2='+sid2+'&sid1='+sid1+'&date='+ check_today(indx) + '&page='+str(pindx)
        req_header={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }

        res = requests.get(url, headers=req_header)
        
        if res.ok:
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')    
            content= {}
            if pindx == 1:
                pager = soup.select('#main_content > div.paging')
                for p in pager:
                    pagestr = p.text
                pagelist= pagestr.split('\n')
                pagelist.pop()
                if pagelist[len(pagelist)-1] == '다음':
                    pagelist.pop()
                maxPage = int(pagelist[len(pagelist)-1])
            elif pindx == maxPage:
                indx+=1 #날짜
                maxPage =0
                pindx = 0
            pindx+=1 
        


            title += soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li')
            title +=soup.select('div#main_content div.list_body.newsflash_body ul.type06 li')
            desc += soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li dl dd span.lede')
            desc += soup.select('div#main_content div.list_body.newsflash_body ul.type06 li dl dd span.lede')
            writer += soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li dl dd span.writing')
            writer += soup.select('div#main_content div.list_body.newsflash_body ul.type06 li dl dd span.writing')


    for data in zip(title, desc, writer):
        titles.append(data[0].find_all('dt', class_= not "photo")[0].text.strip())
        links.append(data[0].find_all('dt', class_= not "photo")[0].find('a')['href'])
        descs.append(data[1].text)
        writers.append(data[2].text)
        res2 = requests.get(data[0].find_all('dt', class_= not "photo")[0].find('a')['href'],headers=req_header )
        if res2.ok:
            published_date = BeautifulSoup(res2.text, 'html.parser').select('div#main_content div.article_header div.article_info div.sponsor span.t11')
            if len(published_date)>0:
                dates.append(published_date[0].text)
    content = zip(titles,links,dates,descs,writers)
    return content
    

def parsing(sid1, sid2):
    url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1='+sid1+'&sid2='+sid2
    req_header={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    res = requests.get(url, headers=req_header)
    if res.ok:
        # Response 객체에서 텍스트 추출
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li')
        desc = soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li dl dd span.lede')
        writer = soup.select('div#main_content div.list_body.newsflash_body ul.type06_headline li dl dd span.writing')
    
        titles = []
        links = []
        dates = []
        descs=[]
        writers=[]
        for data in zip(title,desc, writer):
            titles.append(data[0].find_all('dt', class_= not "photo")[0].text.strip())
            links.append(data[0].find_all('dt', class_= not "photo")[0].find('a')['href'])
            descs.append(data[1].text)
            writers.append(data[2].text)
            
            res2 = requests.get(data[0].find_all('dt', class_= not "photo")[0].find('a')['href'],headers=req_header )
            if res2.ok:
                published_date = BeautifulSoup(res2.text, 'html.parser').select('div#main_content div.article_header div.article_info div.sponsor span.t11')
                if len(published_date)>0:
                    dates.append(published_date[0].text)    
        content = zip(titles,links,dates,descs,writers)            
    return content

def selenium_parsing_new100(sports):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    print(sports)
    page = 1
    day = 0
    maxpage = 0
    titles=[]
    links =[]
    dates=[]
    previews=[]
    writers= []


    while len(titles) < 100:
        URL = 'https://sports.news.naver.com/'+sports+'/news/index.nhn?isphoto=N&date='+check_today(day)+'&page='+str(page)
        driver.get(URL)
        time.sleep(2)

        title = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > a > span')
        link = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > a')
        date = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > div > span.time')
        preview = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > p')
        writer = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > div > span.press')


        if page == 1:
            pagelist = driver.find_elements(By.CSS_SELECTOR,'#_pageList > a')
            if pagelist:
                maxpage=pagelist[len(pagelist)-1].get_attribute('innerHTML')
            else:
                day+=1
                page=0
        if page == maxpage:
            day+=1
            maxPage=0
            page=0
        page+=1
        
        for data in zip(title,preview,writer,date,link):
            titles.append(data[0].get_attribute('innerHTML'))
            previews.append(data[1].get_attribute('innerHTML'))
            writers.append(data[2].get_attribute('innerHTML'))
            dates.append(extract_date(data[3].get_attribute('innerHTML')))
            links.append(data[4].get_attribute('href'))

    contents = zip(titles,links,dates,previews,writers)
    return contents



def selenium_parsing(sports):
    URL = "https://sports.news.naver.com/"+sports+"/news/index.nhn?isphoto=N"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get(URL)
    time.sleep(3)

    title = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > a > span')
    link = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > a')
    date = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > div > span.time')
    preview =driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > p')
    writer = driver.find_elements(By.CSS_SELECTOR,'#_newsList > ul > li > div > div > span.press')
    
    titles = []
    links = []
    dates =[]
    previews = []
    writers = []
    for element in zip(title,link,date,preview,writer):
        titles.append(element[0].get_attribute('innerHTML'))
        links.append(element[1].get_attribute('href'))
        dates.append(extract_date(element[2].get_attribute('innerHTML')))
        previews.append(element[3].get_attribute('innerHTML'))
        writers.append(element[4].get_attribute('innerHTML'))
    contents = zip(titles,links,dates,previews,writers)
    return contents


