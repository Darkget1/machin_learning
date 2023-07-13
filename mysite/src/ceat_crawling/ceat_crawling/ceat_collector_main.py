import os
import sys
import pandas as pd


from threading import Thread
from ceat_crawling.ceat_common.ceat_logging import *
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_comparison_list import comparison_list
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_coupang import coupang_scenario
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_naver import naver_scenario

def ceat_collector_data_init():
    print("========================================")
    init_data = dict()
    init_data["target_mall"] = input("Target Mall Name (Coupang or Naver) : ")
    init_data["search_key"] = input("Search Key : ")
    init_data["start_t"] = input("Start Date (YYYY.MM.DD) : ")
    init_data["end_t"] = input("End Date (YYYY.MM.DD) : ")
    print("========================================")
    return init_data

def worker():
    # init collector data
    collector_data_info = ceat_collector_data_init()

    # enable collector logging
    ceat_logging("collector")

    # Get comparison list
    comparison_name_list = comparison_list(collector_data_info, comparison_list_cnt_max=10).scenario_run()

    print("==================== {} worker start ====================".format(collector_data_info["target_mall"]))
    print(collector_data_info)
    print("========================================")

    if collector_data_info["target_mall"] == "Coupang":
        coupang_scenario(collector_data_info, link_max_cnt=2000, step_get_links=True, step_get_comments=True).scenario_run(comparison_name_list)
    elif collector_data_info["target_mall"] == "Naver":
        naver_scenario(collector_data_info, link_max_cnt=2000, step_get_links=True, step_get_comments=True).scenario_run(comparison_name_list)
    else:
        print("Wrong target_mall")

    print("==================== {} worker  end  ====================".format(collector_data_info["target_mall"]))

if __name__ == "__main__":

    # # start collecting
    # worker_list = list()
    # for target_mall_name in target_mall_df.index:
    #     th = Thread(target=worker, args=())
    #     th.start()
    #     worker_list.append(th)
    #
    # for th in worker_list:
    #     th.join()

    th = Thread(target=worker)
    th.start()
    th.join()
