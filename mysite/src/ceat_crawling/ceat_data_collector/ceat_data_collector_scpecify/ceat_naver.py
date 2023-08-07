import os
import sys
import re
import datetime
import time

from dateutil.relativedelta import relativedelta
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from src.ceat_crawling.ceat_common.ceat_common import *
from src.ceat_crawling.ceat_data_collector.ceat_scraper import *

class naver_scenario:
    def __init__(self, collector_data_info, link_max_cnt, step_get_links = False, step_get_comments = False):
        self.search_key = collector_data_info["search_key"]
        self.target_mall_name = collector_data_info["target_mall"]
        self.start_t = collector_data_info["start_t"]
        self.end_t = collector_data_info["end_t"]
        self.step_get_links = step_get_links
        self.step_get_comments = step_get_comments
        self.link_max_cnt = link_max_cnt
        self.scraper = ceat_scraper("https://shopping.naver.com/home/p/index.naver")

    def naver_open(self):
        self.scraper.crawler.init_crawler()
        self.scraper.crawler.open_crawler()

    def naver_close(self):
        self.scraper.crawler.close_crawler()

    def naver_get_link_same_framework_check(self):
        ret = False
        filter_key_list = ["brand.naver", "smartstore.naver"]

        for filter_key in filter_key_list:
            if filter_key in self.scraper.crawler.get_cur_url():
                ret = True
                print("{}".format(filter_key))

        return ret

    def naver_get_link_click_next_page(self):
        web_elements = self.scraper.crawler.find_elements('class', 'UWN4IvaQza')
        if web_elements is False:
            print("link_elements : {}".format(web_elements))
            return False

        # web_elements_len = len(web_elements)
        for element in web_elements:
            if element.get_attribute('aria-current') == "true":
                link_page_next_num = int(element.text) + 2
                link_page_next = '//*[@id="CategoryProducts"]/div[3]/a[' + str(link_page_next_num) + "]"
                if self.scraper.crawler.click_btn('xpath', link_page_next, 'click', link_page_next_num - 1) is False:
                    return False
                else:
                    return True

        return False

    def naver_get_link_file_exists(self, comparison_name):
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

    def naver_get_link_save(self, comparison_name, data):
        # Save link data
        output_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        create_directory(output_directory)
        output_filename = str(self.target_mall_name) + "_link_" + str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(datetime.today().day) + ".xlsx"
        output_path = os.path.join(output_directory, output_filename)
        link_df = pd.DataFrame({"link": data})
        link_df.to_excel(output_path, index=True)

    def naver_get_link_load(self, comparison_name):
        ret, load_path = self.naver_get_link_file_exists(comparison_name)
        if ret is True:
            return pd.read_excel(load_path, engine='openpyxl')["link"]
        else:
            return False

    def naver_get_link_filter(self, elements, link_comments_cnt_list):
        link_comments_cnt_str = None

        for link_comments_cnt_element_bs in self.scraper.parser.findAttrs(elements, 'span'):
            if "리뷰" in link_comments_cnt_element_bs.text:
                link_comments_cnt_str = link_comments_cnt_element_bs.text
                break

        if link_comments_cnt_str is None:
            print("[Filter] link_comments_cnt_str : {}".format(link_comments_cnt_str))
            status_ret = False
        else:
            if (any(link_comments_cnt_char.isdigit() for link_comments_cnt_char in link_comments_cnt_str) is False) or (link_comments_cnt_str is None):
                print("link_comments_cnt_char : {}".format(link_comments_cnt_str))
                status_ret = False
            else:
                link_comments_cnt = int(float(re.sub(r'[^0-9]', '', link_comments_cnt_str)))
                if link_comments_cnt not in link_comments_cnt_list:
                    link_comments_cnt_list.append(link_comments_cnt)
                    print("[Match] link_comments_cnt : {}".format(link_comments_cnt))
                    status_ret = True
                else:
                    print("[Filter] link_comments_cnt : {}".format(link_comments_cnt))
                    status_ret = False

        return status_ret

    def naver_get_link(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            ret, load_path= self.naver_get_link_file_exists(comparison_name)
            if ret is False:
                # naver url open
                self.naver_open()

                # naver url search
                self.scraper.crawler.search_item('class', '_searchInput_search_text_3CUDs', comparison_name + " " + self.search_key)

                # scoll down
                self.scraper.crawler.scroll()

                link_web_elements = self.scraper.crawler.find_elements('class', 'adProduct_item__1zC9h')
                if link_web_elements is False:
                    print("link_web_elements : {}".format(link_web_elements))
                    return False
                else:
                    for elements in link_web_elements:
                        item_info = self.scraper.parser.findAttr(elements, 'a', {'class':'adProduct_mall__zeLIC'})
                        if item_info is None:
                            continue
                        else:
                            if comparison_name in item_info.text:
                                # open tab
                                self.scraper.crawler.open_tab(item_info['href'])
                                print("Open tab : {}".format(item_info['href']))

                                # check naver framework
                                if self.naver_get_link_same_framework_check() is True:

                                    # click main page
                                    self.scraper.crawler.click_btn('class', '_2yPVRArtDH', 'click', '메인 page 이동')

                                    # search total item
                                    for element in self.scraper.crawler.find_elements('class', '_3HQCww4jR6'):
                                        if "전체상품" in element.text:
                                            # click total item
                                            self.scraper.parser.click_btn(element, 'click', "전체상품")
                                            self.scraper.crawler.sleep_random()

                                            # parse web_elements
                                            link_list = list()
                                            link_cnt = 0
                                            link_page_cnt = 1
                                            link_comments_cnt_list = list()

                                            get_link_status = True
                                            while get_link_status is True:
                                                # scoll down
                                                self.scraper.crawler.scroll()

                                                # get item list
                                                link_web_page_element = self.scraper.crawler.find_element('xpath', '//*[@id="CategoryProducts"]/ul')
                                                link_web_elements = self.scraper.parser.find_elements(link_web_page_element, 'tag', 'li')
                                                for elements in link_web_elements:
                                                    if self.naver_get_link_filter(elements, link_comments_cnt_list):
                                                        link_list.append(self.scraper.parser.find_element(elements, 'tag', 'a').get_attribute('href'))
                                                        link_cnt += 1

                                                print("link_page_cnt : {}".format(link_page_cnt))
                                                # click next link page
                                                if self.naver_get_link_click_next_page() is False:
                                                    self.naver_get_link_save(comparison_name, link_list)
                                                    get_link_status = False
                                                else:
                                                    link_page_cnt += 1

                                # close tab
                                self.scraper.crawler.close_tab()
                                break

                print("======================================== ")

                # naver url close
                self.naver_close()

    def naver_get_comments_click_next_page(self):
        cur_url = self.scraper.crawler.get_cur_url()

        web_element = self.scraper.crawler.find_element('class', '_1HJarNZHiI')
        if web_element is False:
            print("web_element btn_box : {}".format(web_element))
            return False

        web_element = self.scraper.parser.find_elements(web_element, 'tag', 'a')
        if web_element is False:
            print("web_element btn_list : {}".format(web_element))
            return False

        if "brand.naver" in cur_url:
            for element in web_element:
                if element.get_attribute("aria-current") == "true":
                    comment_page_cur = int(float(element.text))
                    print("comment_page_cur : {}".format(comment_page_cur))

            if (comment_page_cur % 10) == 0:
                comment_page_next_num = 12
            else:
                comment_page_next_num = (comment_page_cur % 10) + 2

            comment_page_next = '//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[' + str(comment_page_next_num) + ']'
            if self.scraper.crawler.click_btn('xpath', comment_page_next, 'send_key', comment_page_next_num) is False:
                return False
        elif "smartstore.naver" in cur_url:
            comment_page_next = '//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[' + str(len(web_element)) + ']'
            if self.scraper.crawler.click_btn('xpath', comment_page_next, 'send_key', "다음") is False:
                return False
        else:
            return False

    def naver_get_comments_get_latest_time(self, left_dt, right_dt):
        if left_dt > right_dt:
            return True
        else:
            return False

    def naver_get_comments_save(self, comparison_name, filename, data):
        # save comments data
        output_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name)
        create_directory(output_directory)
        output_filename = filename
        output_path = os.path.join(output_directory, output_filename)
        data.to_excel(output_path, index=False)
        print("naver_get_commoents_save : {}".format(filename))

    def naver_get_comments_url_check(self, comparison_name, url_index, start_dt, end_dt):
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

    def naver_get_comments_pattern_match(self, name, date, seller, score, headline, review):
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

    def naver_get_comments(self, comparison_name_list):
        for comparison_name in comparison_name_list:
            # get url_list
            url_list = self.naver_get_link_load(comparison_name)
            if url_list is False:
                print("url_list : {}".format(url_list))
                continue

            for url_index, url in zip(url_list.index, url_list):
                start_dt = datetime.strptime(self.start_t, "%Y.%m.%d")
                end_dt = datetime.strptime(self.end_t, "%Y.%m.%d")

                print("[{}] {}".format(url_index, url))

                # check url_check
                start_dt, end_dt, skip_url = self.naver_get_comments_url_check(comparison_name, url_index, start_dt, end_dt)
                if skip_url is False:
                    continue

                # url open
                self.scraper.crawler.init_crawler()
                self.scraper.crawler.open_crawler(url)

                get_comments_status = True
                comment_cnt_tot_web_elements = self.scraper.crawler.find_element('class', '_2pgHN-ntx6')
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
                self.scraper.crawler.click_btn('xpath', '//*[@id="content"]/div/div[3]/div[3]/ul/li[2]/a', 'click', '리뷰')

                # sorting click
                self.scraper.crawler.click_btn('xpath', '//*[@id="REVIEW"]/div/div[3]/div[1]/div[1]/ul/li[2]/a', 'click', '최신순')

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
                    comments = self.scraper.crawler.find_elements('class', '_2389dRohZq')
                    if comments is False:
                        print("comments : {}".format(comments))
                        break

                    # parse coments
                    for comment in comments:
                        # increase comment_cnt_cur
                        comment_cnt_cur += 1
                        print("comment_cnt_cur : {}, comment_cnt_tot : {}".format(comment_cnt_cur, comment_cnt_tot))

                        comment_time_cur = datetime.strptime(self.scraper.parser.select(comment, "div._2FmJXrTVEX > span._3QDEeS6NLn")[0].text, "%y.%m.%d.")

                        if (self.naver_get_comments_get_latest_time(comment_time_cur, end_dt)):
                            # url crawling skip
                            print("[Skip][날짜] {}".format(self.scraper.parser.select(comment, "div._2FmJXrTVEX > span._3QDEeS6NLn")[0].text), end="\t")
                            print("[이름] {}".format(self.scraper.parser.select(comment, "strong._3QDEeS6NLn")[0].text))
                            continue
                        else:
                            # url crawling finish
                            if (comment_cnt_cur >= comment_cnt_tot) or (self.naver_get_comments_get_latest_time(start_dt, comment_time_cur) or self.naver_get_comments_pattern_match(name, date, seller, score, headline, review)):
                                data['date'] = date
                                data['name'] = name
                                data['seller'] = seller
                                data['score'] = score
                                data['headline'] = headline
                                data['review'] = review

                                get_comments_status = False
                                if comment_time_tmp is None:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(comment_time_cur.strftime("%Y.%m")) + ".xlsx"
                                else:
                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"

                                print(comment_time_cur)
                                self.naver_get_comments_save(comparison_name, filename, data)
                                break
                            else:
                                # init comment_time_tmp
                                if comment_time_tmp is None:
                                    comment_time_tmp = comment_time_cur

                                if (comment_time_tmp.year >= comment_time_cur.year) and (comment_time_tmp.month > comment_time_cur.month):
                                    print("[날짜] {}".format(self.scraper.parser.select(comment, "div._2FmJXrTVEX > span._3QDEeS6NLn")[0].text), end="\t")
                                    print("[이름] {}".format(self.scraper.parser.select(comment, "strong._3QDEeS6NLn")[0].text))

                                    data['date'] = date
                                    data['name'] = name
                                    data['seller'] = seller
                                    data['score'] = score
                                    data['headline'] = headline
                                    data['review'] = review

                                    filename = str(self.target_mall_name) + "_" + str(url_index) + "_" + str(comment_time_tmp.strftime("%Y.%m")) + ".xlsx"
                                    self.naver_get_comments_save(comparison_name, filename, data)

                                    data = pd.DataFrame()
                                    date = list()
                                    name = list()
                                    seller = list()
                                    score = list()
                                    headline = list()
                                    review = list()

                                    comment_time_tmp = comment_time_cur

                            # print("========================================")
                            # print("[날짜] {}".format(self.scraper.parser.select(comment, "div._2FmJXrTVEX > span._3QDEeS6NLn")[0].text), end="\t")
                            # print("[이름] {}".format(self.scraper.parser.select(comment, "strong._3QDEeS6NLn")[0].text))
                            # print("[평점] {}".format(self.scraper.parser.select(comment, "em._15NU42F3kT")[0].text))
                            # print("[판매] {}".format(comparison_name))

                        date.append(self.scraper.parser.select(comment, "div._2FmJXrTVEX > span._3QDEeS6NLn")[0].text)
                        seller.append(comparison_name)
                        name.append(self.scraper.parser.select(comment, "strong._3QDEeS6NLn")[0].text)
                        score.append(self.scraper.parser.select(comment, "em._15NU42F3kT")[0].text)
                        # print("[제목]", end=' ')
                        headline_attr = None
                        if headline_attr is None:
                            # print(None)
                            headline.append("")
                        else:
                            # print(headline_attr.text.strip())
                            headline.append(headline_attr.text.strip())
                        # print("[리뷰]", end=' ')
                        review_attr = self.scraper.parser.select(comment, "div.YEtwtZFLDz > span._3QDEeS6NLn")[0].text
                        if review_attr is None:
                            # print(None)
                            review.append("")
                        else:
                            # print(review_attr)
                            review.append(review_attr)

                        # print("========================================")

                    # click next comments page
                    if get_comments_status is True:
                        self.scraper.crawler.sleep_random()
                        if self.naver_get_comments_click_next_page() is False:
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

                            self.naver_get_comments_save(comparison_name, filename, data)

                # url close
                self.scraper.crawler.close_crawler()
                self.scraper.crawler.sleep_random()

    def scenario_run(self, comparison_name_list):
        # get link
        self.naver_get_link(comparison_name_list)

        # get comments
        self.naver_get_comments(comparison_name_list)
