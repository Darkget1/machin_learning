#import
import os
import sys
import time

from src.ceat_crawling.ceat_data_collector.ceat_scraper import *
from src.ceat_crawling.ceat_common.ceat_common import *
from selenium.webdriver.common.by import By
#정의매소드
class price_scenario:
    logger = ''

    price_url = "https://www.coupang.com/"
    price_scraper = ''

    def __init__(self, version, arch, background, init_data = None):
        self.logger = ceat_logging(__class__.__name__, "collector")
        self.logger.logger.info("[" + str(__class__.__name__) + " init !!!!]")
        self.price_scraper = ceat_scraper(version, arch, self.price_url, background, init_data)

    def price_open(self, url = 'default_url'):
        self.price_scraper.crawler.open_crawler()
        self.price_scraper.crawler.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

        if url == 'default_url':
            self.price_scraper.crawler.get_url()
        else:
            self.price_scraper.crawler.get_url(url)

    def price_close(self):
        self.price_scraper.crawler.close_crawler()





#쿠팡 제품 검색&url스크레핑 수정중
    def price_get_URL(self, brand_name, item_name, model_name, url_cnt_max):
        self.logger.logger.info("[ Step 1 : get_URL ]")

        # Coupang open
        self.price_open()

        for brand in brand_name:
            for item in item_name:
                for model in model_name:
                    search_key = "'" + str(brand) + "' '" + str(item) + "' '" + str(model) + "'"

                    url_list = list()
                    url_cur_cnt = 0

                    self.price_scraper.crawler.search_item('id', 'headerSearchKeyword', search_key)
                    self.price_scraper.crawler.click_btn('xpath', '//*[@id="searchSortingOrder"]/ul/li[4]', '판매량순')

                    for url_item in self.price_scraper.crawler.find_elements('class', 'search-train_data'):
                        title = str(url_item.find_element(By.TAG_NAME, 'img').get_attribute('alt'))
                        self.logger.logger.debug(title)
                        title = title.lower().replace(item, ' ' + item).replace(model, ' ' + model).replace(',',
                                                                                                            ' ').split(
                            ' ')
                        if brand in title and item in title and model in title:
                            url_list.append(url_item.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                        else:
                            self.logger.logger.debug('Not exist keyward in title')

                        url_cur_cnt += 1
                        if url_cur_cnt >= url_cnt_max:
                            break

                    # Save URL list file
                    output_directory = os.path.join(get_root_path(), "output", "price_data", item, brand, model,
                                                    "LINK")
                    output_filename = str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(
                        datetime.today().day) + ".xlsx"
                    output_path = os.path.join(output_directory, output_filename)
                    create_directory(output_directory)
                    url_df = pd.DataFrame(url_list)
                    url_df.to_excel(output_path)

        # Coupang close
        self.price_close()


#메인에 있는 url 스크레핑 메인 재목 스크레핑
    def coupang_get_comments(self, brand_name, item_name, model_name):

        for brand in brand_name:
            for item in item_name:
                for model in model_name:
                    # Read and get URL list file
                    read_directory = os.path.join(get_root_path(), "output", "collector_data", item, brand, model, "LINK")
                    read_directory_file_list = os.listdir(read_directory)
                    read_directory_file_name = ''
                    for name in read_directory_file_list:
                        read_directory_file_name = name
                    read_path = os.path.join(read_directory, read_directory_file_name)
                    url_list = self.coupang_scraper.parser.read_to_excel(read_path)
                    url_index = 0

                    if url_list.empty:
                        self.logger.logger.debug(brand + item + model + " is no url data")
                    else:
                        for url in url_list[0]:

                            stop_flag = False

                            # Coupang open
                            self.coupang_open(url)

                            self.coupang_scraper.parser.add_dataframe('comments_data')

                            # coupang의 댓글 최대 갯수는 link 당 3000개
                            comment_cur_get_cnt = 0
                            comment_total_cnt = 0

                            while True:
                                try:
                                    if comment_cnt_max == 0:
                                        self.logger.logger.debug(int(re.sub(r'[^0-9]', '', self.coupang_scraper.crawler.find_element('class', 'count').text)))
                                        comment_total_cnt = int(re.sub(r'[^0-9]', '', self.coupang_scraper.crawler.find_element('class', 'count').text))
                                        if comment_total_cnt >= 3000:
                                            comment_total_cnt = 3000
                                    else:
                                        if comment_cnt_max >= 3000:
                                            comment_total_cnt = 3000
                                        else:
                                            comment_total_cnt = comment_cnt_max

                                    # 댓글 이동
                                    self.coupang_scraper.crawler.click_btn('css_selector', '#btfTab > ul.tab-titles > li:nth-child(2)', '상품평')

                                    # 댓글 정렬
                                    self.coupang_scraper.crawler.click_btn('class', 'sdp-review__article__order__sort__newest-btn', '최신순')

                                    # 댓글 crawling 초기화
                                    comments = self.coupang_scraper.crawler.find_elements('class', 'sdp-review__article__list')
                                except:
                                    self.coupang_close()
                                    self.coupang_open(url)
                                    continue
                                else:
                                    break;

                            date = list()
                            name = list()
                            score = list()
                            headline = list()
                            review = list()
                            total_review = list()

                            page_cycle = 0
                            page_index = 0

                            self.logger.logger.debug("[ING][" + str(comment_total_cnt) + "]")
                            while comment_cur_get_cnt < comment_total_cnt:
                                for page_index in range(3, 13):
                                    if comment_cur_get_cnt >= comment_total_cnt:
                                        break

                                    # 댓글 추출
                                    for comment in comments:
                                        # print("[날짜]", end='\t')
                                        # print(self.coupang_scraper.parser.find(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text)
                                        date_data = self.coupang_scraper.parser.find(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__reg-date'}).text
                                        if date_data <= stop_date:
                                            stop_flag = True
                                            break
                                        else:
                                            date.append(date_data)


                                        # print("[이름]", end='\t')
                                        # print(self.coupang_scraper.parser.find(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text)
                                        name.append(self.coupang_scraper.parser.find(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text)

                                        # print("[평점]", end='\t')
                                        # print(self.coupang_scraper.parser.find(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating'])
                                        score.append(self.coupang_scraper.parser.find(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating'])

                                        # print("[제목]", end='\t')
                                        ret_headline = self.coupang_scraper.parser.find(comment, 'div', {'class':'sdp-review__article__list__headline'})
                                        if ret_headline is None:
                                            # print(None)
                                            headline.append("")
                                        else:
                                            # print(ret_headline.text.strip())
                                            headline.append(ret_headline.text.strip())

                                        # print("[리뷰]", end='\t')
                                        ret_review = self.coupang_scraper.parser.find(comment, 'div', {'class':'sdp-review__article__list__review__content'})
                                        if ret_review is None:
                                            # print(None)
                                            review.append("")
                                        else:
                                            # print(ret_review.text.strip())
                                            review.append(ret_review.text.strip())

                                        comment_cur_get_cnt = comment_cur_get_cnt + 1
                                        log_msg = "[" + str(comment_cur_get_cnt) + "]"
                                        self.logger.logger.debug(log_msg)

                                    # 다음 page click
                                    retry_cnt = 0
                                    while True:
                                        try:
                                            btn_xpath = '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[' + str(page_index) + ']'
                                            if self.coupang_scraper.crawler.click_btn('xpath', btn_xpath, page_index):
                                                comments = self.coupang_scraper.crawler.find_elements('class', 'sdp-review__article__list')
                                            else:
                                                if retry_cnt >= 3:
                                                    break
                                                else:
                                                    retry_cnt = retry_cnt + 1
                                                    continue
                                        except:
                                            # click 실패시 처음부터 다시 위치 찾아가는 동장
                                            try:
                                                self.coupang_close()
                                                self.coupang_open(url)
                                                self.coupang_scraper.crawler.click_btn('css_selector', '#btfTab > ul.tab-titles > li:nth-child(2)', '상품평')
                                                self.coupang_scraper.crawler.click_btn('class', 'sdp-review__article__order__sort__newest-btn', '최신순')
                                                for _ in range(0, page_cycle, 1):
                                                    self.coupang_scraper.crawler.click_btn('xpath', '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[12]', 'Next')
                                                for tmp_page_index in range(3, page_index):
                                                    btn_xpath = '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[' + str(tmp_page_index) + ']'
                                                    self.coupang_scraper.crawler.click_btn('xpath', btn_xpath, page_index)
                                                continue
                                            except:
                                                self.logger.logger.error("Except!!!")
                                                comment_cur_get_cnt = comment_total_cnt
                                                break
                                        else:
                                            break

                                    if retry_cnt >= 3:
                                        comment_cur_get_cnt = comment_total_cnt
                                        break

                                    if stop_flag == True:
                                        break

                                if stop_flag == True:
                                    break

                                page_cycle = page_cycle + 1

                            self.logger.logger.debug("[End][" + str(page_cycle) + "][" + str(page_index) + "][" + str(comment_cur_get_cnt) + "]")

                            self.coupang_scraper.parser.data_series['comments_data']['날짜'] = date
                            self.coupang_scraper.parser.data_series['comments_data']['이름'] = name
                            self.coupang_scraper.parser.data_series['comments_data']['평점'] = score

                            for index_num in range(0, len(self.coupang_scraper.parser.data_series['comments_data'].index)):
                                total_review.append(headline[index_num] + review[index_num])

                            self.coupang_scraper.parser.data_series['comments_data']['리뷰'] = total_review

                            # # Save comments file
                            output_directory = os.path.join(get_root_path(), "output", "collector_data", item, brand, model, "COMMENTS")
                            create_directory(output_directory)
                            output_filename = str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(datetime.today().day)  + "." + str(url_index) + ".xlsx"
                            output_path = os.path.join(output_directory, output_filename)
                            self.coupang_scraper.parser.data_series['comments_data'].to_excel(output_path)
                            self.coupang_scraper.parser.del_dataframe('comments_data')

                            url_index += 1

                            # Coupang close
                            self.coupang_close()


#하단 와우할인가 쿠팡판매가 둘다 스크레핑

#매소드 동장 장치
    def run_scenario(self, mode, item_name, brand_name, model_name,url_cnt_max):

        self.logger.logger.info("================================================")
        self.logger.logger.info("[ Coupang scenario run!!! ]")

        if mode == 0 or mode == 1:
            self.price_get_URL(brand_name, item_name, model_name, url_cnt_max)

        if mode == 0 or mode == 2:
            self.price_get_comments(brand_name, item_name, model_name)

