import os
import sys
import time
import openpyxl
import pandas as pd


from ceat_crawling.ceat_common import *
from ceat_crawling.ceat_data_collector import *

class comparison_list:

    def __init__(self, collector_data_info, comparison_list_cnt_max):
        self.search_key = collector_data_info["search_key"]
        self.input_brand = collector_data_info["input_brand"]
        self.comparison_list_cnt_max = comparison_list_cnt_max
        self.scraper = ceat_scraper("https://shopping.naver.com/home/p/index.naver")

    def comparison_open(self):
        self.scraper.crawler.init_crawler()
        self.scraper.crawler.open_crawler()

    def comparison_close(self):
        self.scraper.crawler.close_crawler()

    def comparison_load(self):
        load_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key)
        load_filename = "comparison_list.xlsx"
        load_path = os.path.join(load_directory, load_filename)
        return pd.read_excel(load_path, engine='openpyxl')["comparison_list"]

    def comparison_save(self):
        # make directory
        output_directory = os.path.join(get_root_path(), "storage", "collector_data", self.search_key)
        if os.path.exists(output_directory) is False:
            create_directory(output_directory)

        output_filename = "comparison_list.xlsx"
        output_path = os.path.join(output_directory, output_filename)
        if os.path.exists(output_path) is False:
            # comparison url open
            self.comparison_open()

            # comparison url search
            self.scraper.crawler.search_item('xpath', '//*[@id="__next"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/form/div[1]/div/input', self.search_key)

            # get source from web
            web_elements = self.scraper.crawler.find_elements('class', 'filter_finder_col__k6BKF ')
            if web_elements is False:
                print("web_elements : {}".format(web_elements))
                return False

            for elements in web_elements:
                if "브랜드" in self.scraper.parser.findAttr(elements, 'div', {'class': 'filter_finder_tit__x1gjS'}).text:
                    web_elements = elements

            # parse web_elements
            comparison_name_list = list()
            comparison_cnt = 0

            for comparison_name in self.scraper.parser.findAttrs(web_elements, 'span', {'class': 'filter_text_over__iesoO'}):
                comparison_name_list.append(comparison_name.text)
                comparison_cnt += 1

                if comparison_cnt >= self.comparison_list_cnt_max:
                    break

            comparison_name_list = list(set(comparison_name_list + self.input_brand))

            # make for colltector directory by comparison_name
            for comparison_name in comparison_name_list:
                create_directory(os.path.join(get_root_path(), "storage", "collector_data", self.search_key, comparison_name))

            comparison_name_df = pd.DataFrame({"comparison_list": comparison_name_list})
            comparison_name_df.to_excel(output_path, index=False)

            # comparison url close
            self.comparison_close()
        else:
            print("comparison_load()")
            for input_brand_name in self.input_brand:
                create_directory(os.path.join(get_root_path(), "storage", "collector_data", self.search_key, input_brand_name))

            pd.DataFrame({"comparison_list": list(set(self.comparison_load().tolist() + self.input_brand))}).to_excel(output_path, index=False)
            comparison_name_list = list(set(self.comparison_load().tolist() + self.input_brand))

        print("{}".format(comparison_name_list))
        return comparison_name_list

    def scenario_run(self):
        return self.comparison_save()