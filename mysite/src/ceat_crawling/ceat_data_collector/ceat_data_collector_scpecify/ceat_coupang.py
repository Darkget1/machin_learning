import os
import sys
import re
import datetime
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from ceat_crawling.ceat_common.ceat_common import *
from ceat_crawling.ceat_data_collector.ceat_scraper import *

class coupang_scenario:
    def __init__(self, collector_data_info, link_max_cnt, step_get_links = False, step_get_comments = False):
        self.search_key = collector_data_info["search_key"]
        self.target_mall_name = collector_data_info["target_mall"]
        self.start_t = collector_data_info["start_t"]
        self.end_t = collector_data_info["end_t"]
        self.step_get_links = step_get_links
        self.step_get_comments = step_get_comments
        self.link_max_cnt = link_max_cnt
        self.scraper = ceat_scraper("https://www.coupang.com/")

    def coupang_open(self):
        self.scraper.crawler.init_crawler()
        self.scraper.crawler.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
        self.scraper.crawler.open_crawler()

    def coupang_close(self):
        self.scraper.crawler.close_crawler()

    def coupang_get_link_click_next_page(self):
        if self.scraper.crawler.click_btn('class', 'btn-next', 'send_key', '다음') is False:
            return False

    def coupang_get_link_file_exists(self, comparison_name):
        load_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        load_filename_list = os.listdir(load_directory)
        load_filename = ""
        filter_key = str(self.target_mall_name) + "_link"

        for filename in load_filename_list:
            if filter_key in filename:
                load_filename = filename

        if load_filename != "":
            return True, os.path.join(load_directory, load_filename)
        else:
            return False, None

    def coupang_get_link_save(self, comparison_name, data):
        # Save link data
        output_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        create_directory(output_directory)
        output_filename = str(self.target_mall_name) + "_link_" + str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(datetime.today().day) + ".xlsx"
        output_path = os.path.join(output_directory, output_filename)
        link_df = pd.DataFrame({"link": data})
        #수정
        print(link_df)
        link_df.to_excel(output_path, index=True)

    def coupang_get_link_load(self, comparison_name):
        ret, load_path = self.coupang_get_link_file_exists(comparison_name)
        if ret is True:
            return pd.read_excel(load_path, engine='openpyxl')["link"]
        else:
            return False

    def coupang_get_link_filter(self, elements, comparison_name,search_key, link_comments_cnt_list):
        link_ad = self.scraper.parser.findAttr(elements, 'span', {'class':'ad-badge-text'})
        link_title = self.scraper.parser.findAttr(elements, 'div', {'class': 'name'}).text
        #ad

        if link_ad is None:
            if comparison_name in link_title and search_key in link_title:
                if self.scraper.parser.findAttr(elements, 'span', {'class': 'rating-total-count'}) is None:
                    print("[Filter] link_comments_cnt : {}".format(None))
                    status_ret = False
                else:
                    link_comments_cnt_str = self.scraper.parser.findAttr(elements, 'span', {'class': 'rating-total-count'}).text
                    if (any(link_comments_cnt_char.isdigit() for link_comments_cnt_char in link_comments_cnt_str) is False) or (link_comments_cnt_str is None):
                        print("link_comments_cnt_char : {}".format(link_comments_cnt_str))
                        status_ret = False
                    else:
                        link_comments_cnt = int(float(re.sub(r'[^0-9]', '', link_comments_cnt_str)))
                        if link_comments_cnt not in link_comments_cnt_list:
                            link_comments_cnt_list.append(link_comments_cnt)
                            print("[Match] link_title : {}, link_comments_cnt : {}".format(link_title, link_comments_cnt))
                            return True
                        else:
                            print("[Filter] link_comments_cnt : {}".format(link_comments_cnt))
                            return False
            else:
                print("[Filter] link_title : {}".format(link_title))
                status_ret = False
        else:
            print("[AD] {}".format(link_title))
            status_ret = False

        return status_ret

    def coupang_get_link(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            ret, load_path = self.coupang_get_link_file_exists(comparison_name)
            if ret is False:
                # coupang url open
                self.coupang_open()

                # coupang url search
                self.scraper.crawler.search_item('id', 'headerSearchKeyword', comparison_name + " " + self.search_key)

                # # click sort btn
                # self.scraper.crawler.click_btn('xpath', '//*[@id="searchSortingOrder"]/ul/li[4]', 'click', '판매량순')

                # parse web_elements
                link_list = list()
                link_cnt = 0
                link_page_cnt = 1
                link_comments_cnt_list = list()

                get_link_status = True
                while get_link_status is True:
                    #수정
                    link_web_elements = self.scraper.crawler.find_elements('class', 'search-product')
                    if link_web_elements is False:
                        print("link_web_elements : {}".format(link_web_elements))
                        return False

                    for elements in link_web_elements:
                        # check add link
                        if self.coupang_get_link_filter(elements, comparison_name,self.search_key, link_comments_cnt_list):
                            print(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))
                            link_list.append(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))
                            link_cnt += 1

                        if link_cnt >= self.link_max_cnt:
                            self.coupang_get_link_save(comparison_name, link_list)
                            get_link_status = False
                            break

                    print("link_page_cnt : {}".format(link_page_cnt))
                    self.scraper.crawler.sleep_random()
                    if self.coupang_get_link_click_next_page() is False:
                        self.coupang_get_link_save(comparison_name, link_list)
                        get_link_status = False
                    else:
                        link_page_cnt += 1

                print("======================================== ")

                # coupang url close
                self.coupang_close()
            else:
                continue

    def coupang_get_comments_click_next_page(self):
        web_element = self.scraper.crawler.find_element('class', 'sdp-review__article__page')
        if web_element is False:
            print("comments_elements : {}".format(web_element))
            return False

        comment_page_cur = int(web_element.get_attribute("data-page"))
        print("comment_page_cur : {}".format(comment_page_cur))

        if (comment_page_cur % 10) == 0:
            comment_page_next_num = 12
        else:
            comment_page_next_num = (comment_page_cur % 10) + 2

        comment_page_next = '//*[@id="btfTab"]/ul[2]/li[3]/div/div[6]/section[4]/div[3]/button[' + str(comment_page_next_num) + ']'
        if self.scraper.crawler.click_btn('xpath', comment_page_next, 'send_key', comment_page_next_num) is False:
            return False

    def coupang_get_comments_get_latest_time(self, left_dt, right_dt):
        if left_dt > right_dt:
            return True
        else:
            return False

    def coupang_get_comments_save(self, comparison_name, filename, data):
        # save comments data
        output_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        create_directory(output_directory)
        output_filename = filename
        output_path = os.path.join(output_directory, output_filename)
        data.to_excel(output_path, index=False)
        print("coupang_get_commoents_save : {}".format(filename))

    def coupang_get_comments_url_check(self, comparison_name, url_index, start_dt, end_dt):
        load_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        load_filename_list = os.listdir(load_directory)
        load_comments_url_index_list = list()
        filter_key = str(self.target_mall_name)
        start_dt_ret = ""
        end_dt_ret = ""
        status_ret = ""

        for load_filename in load_filename_list:
            if (filter_key in load_filename) and ("link" not in load_filename):
                load_comments_url_index_list.append(int(load_filename.split("_")[1]))

        # url check
        if not load_comments_url_index_list:
            start_dt_ret = start_dt
            end_dt_ret = end_dt
            status_ret = True
        else:
            load_comments_url_index_list_max = max(load_comments_url_index_list)
            if url_index < load_comments_url_index_list_max:
                start_dt_ret = start_dt
                end_dt_ret = end_dt
                status_ret = False
                print("[Skip URL] url_index : {}, load_comments_url_index_list_max : {}".format(url_index, load_comments_url_index_list_max))
            elif url_index > load_comments_url_index_list_max:
                start_dt_ret = start_dt
                end_dt_ret = end_dt
                status_ret = True
                print("[New URL]")
            else:
                filter_key += "_{}".format(load_comments_url_index_list_max)
                for load_filename in load_filename_list:
                    if filter_key in load_filename:

                        load_filename_info = load_filename.split("_")[2].split(".")
                        load_filename_time_info = str(load_filename_info[0]) + "." + str(load_filename_info[1]) + ".01"
                        load_filename_dt = datetime.strptime(load_filename_time_info, "%Y.%m.%d")

                        if load_filename_dt.year <= start_dt.year:
                            if load_filename_dt.month < start_dt.month:
                                start_dt_ret = start_dt
                                end_dt_ret = end_dt
                                status_ret = False
                                print("[Skip URL] url_index : {}, load_comments_url_index_list_max : {}".format(url_index, load_comments_url_index_list_max))
                            elif load_filename_dt.month == start_dt.month:
                                start_dt_ret = load_filename_dt
                                end_dt_ret = (load_filename_dt + relativedelta(months=1)) - relativedelta(days=1)
                                status_ret = True
                                print("Del load_filename load_filename_dt.month == start_dt.month : {}".format(load_filename))
                                os.remove(os.path.join(load_directory, load_filename))
                            else:
                                if load_filename_dt.month <= end_dt.month:
                                    start_dt_ret = start_dt
                                    end_dt_ret = (load_filename_dt + relativedelta(months=1)) - relativedelta(days=1)
                                    status_ret = True
                                    print("Del load_filename load_filename_dt.month <= end_dt.month : {}".format(load_filename))
                                    os.remove(os.path.join(load_directory, load_filename))
                                else:
                                    start_dt_ret = start_dt
                                    end_dt_ret = end_dt
                                    status_ret = True
                        else:
                            start_dt_ret = start_dt
                            end_dt_ret = end_dt
                            status_ret = True
                            print("TBD")
                        break
                    else:
                        start_dt_ret = start_dt
                        end_dt_ret = end_dt
                        status_ret = True

        print("{} ~ {} [{}]".format(start_dt_ret, end_dt_ret, status_ret))
        return start_dt_ret, end_dt_ret, status_ret

    def coupang_get_comments_pattern_match(self, name, date, seller, score, headline, review):
        ret = False
        pattern_len = 5
        name_len = len(name)
        date_len = len(date)

        if (name_len >= (pattern_len * 2)) and (date_len >= (pattern_len * 2)):
            name_prev = name[((pattern_len * 2) * -1):(pattern_len * -1)]
            name_next = name[(pattern_len * -1):]
            date_prev = date[((pattern_len * 2) * -1):(pattern_len * -1)]
            date_next = date[(pattern_len * -1):]

            if (name_prev == name_next) and (date_prev == date_next):
                name.pop(-1)
                date.pop(-1)
                seller.pop(-1)
                score.pop(-1)
                headline.pop(-1)
                review.pop(-1)
                ret = True

        return ret

    def coupang_get_comments(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            # get url_list
            url_list = self.coupang_get_link_load(comparison_name)
            if url_list is False:
                print("url_list : {}".format(url_list))
                continue

            for url_index, url in zip(url_list.index, url_list):
                #교체 네이버에서 충족할필요있음
                start_t = self.start_t.replace('-', '.')
                end_t = self.end_t.replace('-', '.')
                start_dt = datetime.strptime(start_t, "%Y.%m.%d")
                end_dt = datetime.strptime(end_t, "%Y.%m.%d")


                print("[{}] {}".format(url_index, url))

                # check url_check
                start_dt, end_dt, skip_url = self.coupang_get_comments_url_check(comparison_name, url_index, start_dt, end_dt)
                if skip_url is False:
                    continue

                # url open
                self.scraper.crawler.init_crawler()
                self.scraper.crawler.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
                self.scraper.crawler.open_crawler(url)

                get_comments_status = True
                comment_cnt_tot_web_elements = self.scraper.crawler.find_element('class', 'count')
                if comment_cnt_tot_web_elements is False:
                    print("comment_cnt_tot_web_elements : {}".format(comment_cnt_tot_web_elements))
                    continue

                comment_cnt_tot_str = comment_cnt_tot_web_elements.text
                if (any(comment_cnt_tot_char.isdigit() for comment_cnt_tot_char in comment_cnt_tot_str) is False) or (comment_cnt_tot_str is None):
                    print("comment_cnt_tot_str : {}".format(comment_cnt_tot_str))
                    continue

                comment_cnt_tot = int(float(re.sub(r'[^0-9]', '', comment_cnt_tot_str)))
                comment_cnt_cur = 0
                comment_time_cur = 0
                comment_time_tmp = None

                # review click
                self.scraper.crawler.click_btn('css_selector', '#btfTab > ul.tab-titles > li:nth-child(2)', 'click', '상품평')

                # sorting click
                self.scraper.crawler.click_btn('class', 'sdp-review__article__order__sort__newest-btn', 'click', '최신순')

                # init comments data
                data = pd.DataFrame()
                date = list()
                name = list()
                seller = list()
                score = list()
                headline = list()
                review = list()

                while get_comments_status is True:
                    # get comments
                    comments = self.scraper.crawler.find_elements('class', 'sdp-review__article__list')
                    if comments is False:
                        print("comments : {}".format(comments))
                        break

                    # parse coments
                    for comment in comments:
                        # increase comment_cnt_cur
                        comment_cnt_cur += 1
                        print("comment_cnt_cur : {}, comment_cnt_tot : {}".format(comment_cnt_cur, comment_cnt_tot))

                        comment_time_cur = datetime.strptime(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text, "%Y.%m.%d")

                        if (self.coupang_get_comments_get_latest_time(comment_time_cur, end_dt)):
                            # url crawling skip
                            print("[Skip][날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                            print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class': 'sdp-review__article__list__info__user__name'}).text))
                            continue
                        else:
                            # url crawling finish
                            if (comment_cnt_cur >= comment_cnt_tot) or (self.coupang_get_comments_get_latest_time(start_dt, comment_time_cur) or self.coupang_get_comments_pattern_match(name, date, seller, score, headline, review)):
                                data['date'] = date
                                data['name'] = name
                                data['seller'] = seller
                                data['score'] = score
                                data['headline'] = headline
                                data['review'] = review

                                get_comments_status = False
                                if comment_time_tmp is None:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(
                                        comment_time_cur.strftime("%Y.%m")) + ".xlsx"
                                else:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(
                                        comment_time_tmp.strftime("%Y.%m")) + ".xlsx"

                                print(comment_time_cur)
                                self.coupang_get_comments_save(comparison_name, filename, data)
                                break
                            else:
                                # init comment_time_tmp
                                if comment_time_tmp is None:
                                    comment_time_tmp = comment_time_cur

                                if (comment_time_tmp.year >= comment_time_cur.year) and (comment_time_tmp.month > comment_time_cur.month):
                                    print("[날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                                    print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class': 'sdp-review__article__list__info__user__name'}).text))

                                    data['date'] = date
                                    data['name'] = name
                                    data['seller'] = seller
                                    data['score'] = score
                                    data['headline'] = headline
                                    data['review'] = review

                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"
                                    self.coupang_get_comments_save(comparison_name, filename, data)

                                    data = pd.DataFrame()
                                    date = list()
                                    name = list()
                                    seller = list()
                                    score = list()
                                    headline = list()
                                    review = list()

                                    comment_time_tmp = comment_time_cur

                            # print("========================================")
                            # print("[날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                            # print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text))
                            # print("[평점] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating']))
                            # print("[판매] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__seller_name'}).text))

                        date.append(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text)
                        seller.append(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__seller_name'}).text)
                        name.append(self.scraper.parser.findAttr(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text)
                        score.append(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating'])
                        # print("[제목]", end=' ')
                        headline_attr = self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__headline'})
                        if headline_attr is None:
                            # print(None)
                            headline.append("")
                        else:
                            # print(headline_attr.text.strip())
                            headline.append(headline_attr.text.strip())
                        # print("[리뷰]", end=' ')
                        review_attr = self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__review__content'})
                        if review_attr is None:
                            # print(None)
                            review.append("")
                        else:
                            # print(review_attr.text.strip())
                            review.append(review_attr.text.strip())

                        # print("========================================")

                    # click next comments page
                    if get_comments_status is True:
                        self.scraper.crawler.sleep_random()
                        if self.coupang_get_comments_click_next_page() is False:
                            data['date'] = date
                            data['name'] = name
                            data['seller'] = seller
                            data['score'] = score
                            data['headline'] = headline
                            data['review'] = review

                            get_comments_status = False
                            if comment_time_tmp is None:
                                filename = str(self.target_mall_name) + "_"  + str(url_index) + "_" + str(comment_time_cur.strftime("%Y.%m")) + ".xlsx"
                            else:
                                filename = str(self.target_mall_name) + "_"  + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"

                            self.coupang_get_comments_save(comparison_name, filename, data)

                # url close
                self.scraper.crawler.close_crawler()
                self.scraper.crawler.sleep_random()

    def scenario_run(self, comparison_name_list):
        # get link
        self.coupang_get_link(comparison_name_list)

        # get comments
        self.coupang_get_comments(comparison_name_list)

    def coupang_get_link_to_DB(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            ret, load_path = self.coupang_get_link_file_exists(comparison_name)
            if ret is False:
                # coupang url open
                self.coupang_open()

                # coupang url search
                self.scraper.crawler.search_item('id', 'headerSearchKeyword', comparison_name + " " + self.search_key)

                # # click sort btn
                # self.scraper.crawler.click_btn('xpath', '//*[@id="searchSortingOrder"]/ul/li[4]', 'click', '판매량순')

                # parse web_elements
                link_list = list()
                link_cnt = 0
                link_page_cnt = 1
                link_comments_cnt_list = list()

                get_link_status = True
                while get_link_status is True:
                    #수정
                    link_web_elements = self.scraper.crawler.find_elements('class', 'search-product')
                    if link_web_elements is False:
                        # print("link_web_elements : {}".format(link_web_elements))
                        return False

                    for elements in link_web_elements:
                        # check add link
                        if self.coupang_get_link_filter(elements, comparison_name,self.search_key, link_comments_cnt_list):
                            # print(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))
                            # link_list.append(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))

                            # To Do (YANG): Send URL to DB!!!!!!!!!!!!!!!!
                            print(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))
                            link_cnt += 1

                        if link_cnt >= self.link_max_cnt:
                            # self.coupang_get_link_save(comparison_name, link_list)
                            get_link_status = False
                            break

                    # print("link_page_cnt : {}".format(link_page_cnt))
                    self.scraper.crawler.sleep_random()
                    if self.coupang_get_link_click_next_page() is False:
                        # self.coupang_get_link_save(comparison_name, link_list)
                        get_link_status = False
                    else:
                        link_page_cnt += 1

                print("======================================== ")

                # coupang url close
                self.coupang_close()
            else:
                continue

    def coupang_get_comments_to_DB(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            # get url_list
            url_list = self.coupang_get_link_load(comparison_name)
            if url_list is False:
                print("url_list : {}".format(url_list))
                continue

            for url_index, url in zip(url_list.index, url_list):
                #교체 네이버에서 충족할필요있음
                start_t = self.start_t.replace('-', '.')
                end_t = self.end_t.replace('-', '.')
                start_dt = datetime.strptime(start_t, "%Y.%m.%d")
                end_dt = datetime.strptime(end_t, "%Y.%m.%d")


                print("[{}] {}".format(url_index, url))

                # check url_check
                start_dt, end_dt, skip_url = self.coupang_get_comments_url_check(comparison_name, url_index, start_dt, end_dt)
                if skip_url is False:
                    continue

                # url open
                self.scraper.crawler.init_crawler()
                self.scraper.crawler.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
                self.scraper.crawler.open_crawler(url)

                get_comments_status = True
                comment_cnt_tot_web_elements = self.scraper.crawler.find_element('class', 'count')
                if comment_cnt_tot_web_elements is False:
                    print("comment_cnt_tot_web_elements : {}".format(comment_cnt_tot_web_elements))
                    continue

                comment_cnt_tot_str = comment_cnt_tot_web_elements.text
                if (any(comment_cnt_tot_char.isdigit() for comment_cnt_tot_char in comment_cnt_tot_str) is False) or (comment_cnt_tot_str is None):
                    print("comment_cnt_tot_str : {}".format(comment_cnt_tot_str))
                    continue

                comment_cnt_tot = int(float(re.sub(r'[^0-9]', '', comment_cnt_tot_str)))
                comment_cnt_cur = 0
                comment_time_cur = 0
                comment_time_tmp = None

                # review click
                self.scraper.crawler.click_btn('css_selector', '#btfTab > ul.tab-titles > li:nth-child(2)', 'click', '상품평')

                # sorting click
                self.scraper.crawler.click_btn('class', 'sdp-review__article__order__sort__newest-btn', 'click', '최신순')

                # init comments data
                data = pd.DataFrame()
                date = list()
                name = list()
                seller = list()
                score = list()
                headline = list()
                review = list()

                while get_comments_status is True:
                    # get comments
                    comments = self.scraper.crawler.find_elements('class', 'sdp-review__article__list')
                    if comments is False:
                        print("comments : {}".format(comments))
                        break

                    # parse coments
                    for comment in comments:
                        # increase comment_cnt_cur
                        comment_cnt_cur += 1
                        print("comment_cnt_cur : {}, comment_cnt_tot : {}".format(comment_cnt_cur, comment_cnt_tot))

                        comment_time_cur = datetime.strptime(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text, "%Y.%m.%d")

                        if (self.coupang_get_comments_get_latest_time(comment_time_cur, end_dt)):
                            # url crawling skip
                            print("[Skip][날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                            print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class': 'sdp-review__article__list__info__user__name'}).text))
                            continue
                        else:
                            # url crawling finish
                            if (comment_cnt_cur >= comment_cnt_tot) or (self.coupang_get_comments_get_latest_time(start_dt, comment_time_cur) or self.coupang_get_comments_pattern_match(name, date, seller, score, headline, review)):
                                data['date'] = date
                                data['name'] = name
                                data['seller'] = seller
                                data['score'] = score
                                data['headline'] = headline
                                data['review'] = review

                                get_comments_status = False
                                if comment_time_tmp is None:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(
                                        comment_time_cur.strftime("%Y.%m")) + ".xlsx"
                                else:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(
                                        comment_time_tmp.strftime("%Y.%m")) + ".xlsx"

                                print(comment_time_cur)
                                self.coupang_get_comments_save(comparison_name, filename, data)
                                break
                            else:
                                # init comment_time_tmp
                                if comment_time_tmp is None:
                                    comment_time_tmp = comment_time_cur

                                if (comment_time_tmp.year >= comment_time_cur.year) and (comment_time_tmp.month > comment_time_cur.month):
                                    print("[날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                                    print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class': 'sdp-review__article__list__info__user__name'}).text))

                                    data['date'] = date
                                    data['name'] = name
                                    data['seller'] = seller
                                    data['score'] = score
                                    data['headline'] = headline
                                    data['review'] = review

                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"
                                    self.coupang_get_comments_save(comparison_name, filename, data)

                                    data = pd.DataFrame()
                                    date = list()
                                    name = list()
                                    seller = list()
                                    score = list()
                                    headline = list()
                                    review = list()

                                    comment_time_tmp = comment_time_cur

                            # To Do (YANG): Send comment(date) to DB!!!!!!!!!!!!!!!!
                            print("[날짜] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text), end="\t")
                            # To Do (YANG): Send comment(name) to DB!!!!!!!!!!!!!!!!
                            print("[이름] {}".format(self.scraper.parser.findAttr(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text))
                            # To Do (YANG): Send comment(score) to DB!!!!!!!!!!!!!!!!
                            print("[평점] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating']))
                            # To Do (YANG): Send comment(seller) to DB!!!!!!!!!!!!!!!!
                            print("[판매] {}".format(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__seller_name'}).text))

                        date.append(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__reg-date'}).text)
                        seller.append(self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__info__product-info__seller_name'}).text)
                        name.append(self.scraper.parser.findAttr(comment, 'span', {'class':'sdp-review__article__list__info__user__name'}).text)
                        score.append(self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__info__product-info__star-orange'})['data-rating'])

                        # print("[제목]", end=' ')
                        headline_attr = self.scraper.parser.findAttr(comment, 'div', {'class': 'sdp-review__article__list__headline'})
                        if headline_attr is None:
                            # print(None)
                            headline.append("")
                        else:
                            # To Do (YANG): Send comment(headline) to DB!!!!!!!!!!!!!!!!
                            print(headline_attr.text.strip())
                            headline.append(headline_attr.text.strip())
                        # print("[리뷰]", end=' ')
                        review_attr = self.scraper.parser.findAttr(comment, 'div', {'class':'sdp-review__article__list__review__content'})
                        if review_attr is None:
                            # print(None)
                            review.append("")
                        else:
                            # To Do (YANG): Send comment(review_attr) to DB!!!!!!!!!!!!!!!!
                            print(review_attr.text.strip())
                            review.append(review_attr.text.strip())

                        # print("========================================")

                    # click next comments page
                    if get_comments_status is True:
                        self.scraper.crawler.sleep_random()
                        if self.coupang_get_comments_click_next_page() is False:
                            data['date'] = date
                            data['name'] = name
                            data['seller'] = seller
                            data['score'] = score
                            data['headline'] = headline
                            data['review'] = review

                            get_comments_status = False
                            if comment_time_tmp is None:
                                filename = str(self.target_mall_name) + "_"  + str(url_index) + "_" + str(comment_time_cur.strftime("%Y.%m")) + ".xlsx"
                            else:
                                filename = str(self.target_mall_name) + "_"  + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"

                            self.coupang_get_comments_save(comparison_name, filename, data)

                # url close
                self.scraper.crawler.close_crawler()
                self.scraper.crawler.sleep_random()