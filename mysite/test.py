
from src.ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify import ceat_coupang

from src.ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_comparison_list import comparison_list


def coupang(room_name):
    brand_list = []
    #수집 데이터 리스트
    def ceat_collector_data_init():
        print("========================================")
        init_data = dict()

        init_data["target_mall"] = 'Naver'
        print("Target Mall Name (Coupang or Naver) : ",init_data["target_mall"])
        init_data["search_key"] = '마스크'
        print("Search Key : ",init_data["search_key"])
        init_data["start_t"] = '2023.07.01'
        print('Start Date (YYYY.MM.DD) : ',init_data["start_t"])
        init_data["end_t"] = '2023.07.31'
        print("End Date (YYYY.MM.DD) : ",init_data["end_t"])
        init_data['input_brand'] = ['다나']
        print("Input_brand : ",init_data['input_brand'])
        print("========================================")

        return init_data
    collector_data_info = ceat_collector_data_init()
    comparison_name_list = comparison_list(collector_data_info, comparison_list_cnt_max=10).scenario_run()
    print("==================== {} worker start ====================".format(collector_data_info["target_mall"]))
    print(collector_data_info)
    print("========================================")

    print('브랜드 리스트 :',comparison_name_list)
    ceat_coupang.coupang_scenario(collector_data_info, link_max_cnt=2000, step_get_links=True, step_get_comments=True).coupang_get_link_to_DB(comparison_name_list)

coupang(1)