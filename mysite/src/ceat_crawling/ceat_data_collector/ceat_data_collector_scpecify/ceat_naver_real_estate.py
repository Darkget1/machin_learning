import os
import sys

from src.ceat_crawling.ceat_data_collector.ceat_scraper import *
from src.ceat_crawling.ceat_common.ceat_common import *
class naver_scenario_real_estate:
    logger = ''
    naver_url = ""
    naver_scraper = ''

    def __init__(self, version, arch, background, init_data = None):
        self.logger = ceat_logging(__class__.__name__, "collector")
        self.logger.logger.info("[" + str(__class__.__name__) + " init !!!!]")
        self.naver_scraper = ceat_scraper(version, arch, self.naver_url, background, init_data)

    def naver_open(self, url = 'default_url'):
        self.naver_scraper.crawler.open_crawler()

        if url == 'default_url':
            self.naver_scraper.crawler.get_url()
        else:
            self.naver_scraper.crawler.get_url(url)

    def naver_close(self):
        self.naver_scraper.crawler.close_crawler()

    #def scenario_run_get_URL(self, city_totla, str_element1_totla, str_element2_totla):
    def scenario_run_get_URL(self, city):
        self.naver_scraper.parser.add_dataframe('link')
        self.naver_scraper.parser.data_series['link']['시/도'] = ''
        self.naver_scraper.parser.data_series['link']['시/군/구'] = ''
        self.naver_scraper.parser.data_series['link']['읍/면/동'] = ''
        self.naver_scraper.parser.data_series['link']['url'] = ''



        self.logger.logger.info("[ Step 1 : get_URL ]")
        naver_url = "https://new.land.naver.com/search?ms=37.482968,127.0634,16&a=APT:JGC:ABYG&e=RETAIL"
        self.naver_open(naver_url)
        self.naver_scraper.crawler.sleep_random()
        self.naver_scraper.crawler.find_elements('class', 'area', self.naver_scraper.crawler.find_element('class', "filter_region_inner"))[0].click()
        self.naver_scraper.crawler.sleep_random()
        #시/도클릭

        elements = self.naver_scraper.crawler.find_elements('class', "area_item")
        for element in elements:
            if city in element.text:
                element.click()
                break
        self.naver_scraper.crawler.sleep_random()
        #시/군/구 클릭
        str_element1_totla = self.naver_scraper.crawler.find_element('css_selector', ".area_list--district").text.split()

        for str_element1 in str_element1_totla:
            elements = self.naver_scraper.crawler.find_elements('class', "area_item")
            for element in elements:
                if str_element1 in element.text:
                    element.click()
                    break
            self.naver_scraper.crawler.sleep_random()
            # 읍/면/동 클릭
            str_element2_totla = self.naver_scraper.crawler.find_element('css_selector',
                                                                         ".area_list--district").text.split()
            # 읍/면/동 클릭

            for str_element2 in str_element2_totla:


                elements = self.naver_scraper.crawler.find_elements('class', "area_item")

                for element in elements:
                    if str_element2 in element.text:

                        element.click()
                        break





                self.naver_scraper.crawler.sleep_random()
                #맵클릭
                self.naver_scraper.crawler.find_element('class' ,'btn_mapview').click()
                self.naver_scraper.crawler.sleep_random()


                url = self.naver_scraper.crawler.driver.current_url
                self.naver_scraper.parser.add_dataframe("Tmp")
                self.naver_scraper.parser.data_series["Tmp"]['시/도'] = [city]
                self.naver_scraper.parser.data_series["Tmp"]['시/군/구'] = [str_element1]
                self.naver_scraper.parser.data_series["Tmp"]['읍/면/동'] = [str_element2]
                self.naver_scraper.parser.data_series["Tmp"]['url'] = [url]

                self.naver_scraper.parser.data_series['link'] = self.naver_scraper.parser.data_series['link'].append(self.naver_scraper.parser.data_series["Tmp"])

                output_directory = os.path.join(get_root_path(), "output", "collector_data", city,"LINK")
                output_filename = str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(
                    datetime.today().day) + ".xlsx"
                output_path = os.path.join(output_directory, output_filename)
                create_directory(output_directory)
                self.naver_scraper.parser.data_series['link'].to_excel(output_path)
                self.naver_scraper.parser.del_dataframe('Tmp')



                self.naver_scraper.crawler.find_elements('class', 'area',self.naver_scraper.crawler.find_element('class',"filter_region_inner"))[2].click()
                self.naver_scraper.crawler.sleep_random()




            self.naver_scraper.crawler.find_elements('class',"area_select_item ")[1].click()

            self.naver_scraper.crawler.sleep_random()

        # Naver close
        self.naver_close()

    def scenario_run_get_data(self, city, data):
        output_directory = os.path.join(get_root_path(), "output", "collector_data", city)
        create_directory(output_directory)
        output_filename = str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(datetime.today().day) + ".xlsx"
        output_path = os.path.join(output_directory, output_filename)

        #저장 데이터 프레임 생성
        self.naver_scraper.parser.add_dataframe(city)
        self.naver_scraper.parser.data_series[city]['시/구/군'] = ''
        self.naver_scraper.parser.data_series[city]['읍/면/동'] = ''
        self.naver_scraper.parser.data_series[city]['매물이름'] = ''
        self.naver_scraper.parser.data_series[city]['계약종류'] = ''
        self.naver_scraper.parser.data_series[city]['가격'] = ''
        self.naver_scraper.parser.data_series[city]['매물종류'] = ''
        self.naver_scraper.parser.data_series[city]['크기'] = ''
        self.naver_scraper.parser.data_series[city]['층'] = ''
        self.naver_scraper.parser.data_series[city]['방향'] = ''
        self.naver_scraper.parser.data_series[city]['스팩2'] = ''
        self.naver_scraper.parser.data_series[city]['에이전트'] = ''
        self.naver_scraper.parser.data_series[city]['날짜'] = ''


        ### step 1. 부동산 크롤링
        # 크롬 웹브라우저 실행

        for url,str_element1,str_element2 in zip(data['url'],data['시/도'],data['시/군/구']):
            self.naver_open(url)
            self.naver_scraper.crawler.sleep_random()
            self.naver_scraper.crawler.find_elements('class', 'area', self.naver_scraper.crawler.find_element('class',
                                                                                                              "filter_region_inner"))[
                3].click()
            self.naver_scraper.crawler.sleep_random()

            #단지 데이터 가져오기
            complex_item_inners = self.naver_scraper.crawler.find_elements('class', 'complex_title',self.naver_scraper.crawler.find_element('class','area_list--complex'))
            complex_item_inner_name = []
            for complex_item_inner in complex_item_inners:
                complex_item_inner_name.append(complex_item_inner.text)

            #테스트
            # self.naver_scraper.crawler.find_elements('class', 'complex_title',
            #                                                                self.naver_scraper.crawler.find_element(
            #                                                                    'class', 'area_list--complex'))[0].click()
            #self.naver_scraper.crawler.sleep_random()


            self.naver_close()
            # 단지 클릭
            for item_name in complex_item_inner_name:

                self.naver_open(url)
                self.naver_scraper.crawler.sleep_random()
                self.naver_scraper.crawler.find_elements('class', 'area',
                                                         self.naver_scraper.crawler.find_element('class',
                                                                                                 "filter_region_inner"))[
                    3].click()
                self.naver_scraper.crawler.sleep_random()
                #단지클릭
                elements = self.naver_scraper.crawler.find_elements('class', 'complex_title',self.naver_scraper.crawler.find_element('class','area_list--complex'))

                for element in elements:
                    if item_name in element.text:
                        element.click()
                        break

                self.naver_scraper.crawler.sleep_random()
                #데이터 스크레핑
                for item in self.naver_scraper.crawler.find_elements('class', 'item ', self.naver_scraper.crawler.find_element('class', "item_list--article")):

                    # 매물 이름
                    # print("매물 이름", end='\t')
                    # print(self.naver_scraper.crawler.find_element('class', 'text', item).text)
                    str_text = self.naver_scraper.crawler.find_element('class', 'text', item).text

                    # 계약 종류
                    # print("계약 종류", end='\t')
                    # print(self.naver_scraper.crawler.find_elements('class', 'type', item)[0].text)
                    str_type0 = self.naver_scraper.crawler.find_elements('class', 'type', item)[0].text

                    # 가격
                    # print("가격", end='\t')
                    # print(self.naver_scraper.crawler.find_element('class', 'price', item).text)
                    str_price = self.naver_scraper.crawler.find_element('class', 'price', item).text

                    # 매물 종류
                    # print("매물 종류", end='\t')
                    # print(self.naver_scraper.crawler.find_elements('class', 'type', item)[1].text)
                    str_type1 = self.naver_scraper.crawler.find_elements('class', 'type', item)[1].text

                    # 스팩1
                    # print("스팩1", end='\t')
                    # print(self.naver_scraper.crawler.find_elements('class', 'spec', item)[0].text)
                    spec1 = self.naver_scraper.crawler.find_elements('class', 'spec', item)[0].text
                    spec1 = spec1.split(',')
                    str_spec10 = spec1[0]
                    str_spec11 = spec1[1]
                    str_spec12 = spec1[2]
                    # for spec in spec1:
                    #     print(spec)

                    # 스팩2
                    # print("스팩2", end='\t')
                    # print(self.naver_scraper.crawler.find_elements('class', 'spec', item)[1].text)
                    str_spec2 = self.naver_scraper.crawler.find_elements('class', 'spec', item)[1].text

                    # agent
                    # print("agent", end='\t')
                    # print(self.naver_scraper.crawler.find_element('class', 'cp_area_inner', item).text.replace('\n', ' '))
                    str_agent = self.naver_scraper.crawler.find_element('class', 'cp_area_inner', item).text.replace('\n', ' ')

                    # label
                    # print('label', end='\t')
                    # print(self.naver_scraper.crawler.find_element('class', 'label', item).text)
                    str_label = self.naver_scraper.crawler.find_element('class', 'label', item).text

                    self.naver_scraper.parser.add_dataframe("Tmp")
                    self.naver_scraper.parser.data_series["Tmp"]['시/구/군'] = [str_element1]
                    self.naver_scraper.parser.data_series["Tmp"]['읍/면/동'] = [str_element2]
                    self.naver_scraper.parser.data_series["Tmp"]['매물이름'] = [str_text]
                    self.naver_scraper.parser.data_series["Tmp"]['계약종류'] = [str_type0]
                    self.naver_scraper.parser.data_series["Tmp"]['가격'] = [str_price]
                    self.naver_scraper.parser.data_series["Tmp"]['매물종류'] = [str_type1]
                    self.naver_scraper.parser.data_series["Tmp"]['크기'] = [str_spec10]
                    self.naver_scraper.parser.data_series["Tmp"]['층'] = [str_spec11]
                    self.naver_scraper.parser.data_series["Tmp"]['방향'] = [str_spec12]
                    self.naver_scraper.parser.data_series["Tmp"]['스팩2'] = [str_spec2]
                    self.naver_scraper.parser.data_series["Tmp"]['에이전트'] = [str_agent]
                    self.naver_scraper.parser.data_series["Tmp"]['날짜'] = [str_label]
                    self.naver_scraper.parser.data_series[city] = self.naver_scraper.parser.data_series[city].append(self.naver_scraper.parser.data_series["Tmp"])
                    self.naver_scraper.parser.del_dataframe("Tmp")


                    self.naver_scraper.parser.data_series[city].to_excel(output_path, index=False, engine='xlsxwriter')







                self.naver_close()

        self.naver_scraper.parser.del_dataframe(city)



    def scenario_run(self, mode, city):
        self.logger.logger.info("================================================")
        self.logger.logger.info("[ Naver scenario run!!! ]")

        # Get URL list
        if mode == 0 or mode ==1 :
            self.scenario_run_get_URL(city)


        # Get comments
        if mode == 0 or mode == 2:

            read_directory = os.path.join(get_root_path(), "output", "collector_data", city , "LINK")
            read_directory_file_list = os.listdir(read_directory)
            read_directory_file_name = ''
            for name in read_directory_file_list:
                read_directory_file_name = name
            read_path = os.path.join(read_directory, read_directory_file_name)

            self.naver_scraper.parser.add_dataframe('Link')
            self.naver_scraper.parser.data_series['Link'] = self.naver_scraper.parser.read_to_excel(read_path)
            data = self.naver_scraper.parser.data_series['Link']

            self.scenario_run_get_data(city, data)




        self.logger.logger.info("================================================")
