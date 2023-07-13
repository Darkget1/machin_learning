import os
import sys
import multiprocessing


# from ceat_common.ceat_logging import
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_comparison_list import comparison_list
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_coupang import coupang_scenario
from ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_naver import naver_scenario

from flask import request
from flask_restx import Resource, Namespace, fields

Collector = Namespace(name="CEAT Collector")

collector_model = Collector.model('CEAT collector', {
    'target_mall': fields.String(description='Target Mall Name (Coupang or Naver)', required=True, example="Coupang"),
    'search_key': fields.String(description='Search Key', required=True, example="탈모샴푸"),
    'start_t': fields.String(description='Start Date (YYYY.MM.DD)', required=True, example="2023.01.01"),
    'end_t': fields.String(description='End Date (YYYY.MM.DD)', required=True, example="2023.04.30")
})

ceat_collector_worker_list = list()

def ceat_collector_process(collector_data_info):
#    # enable collector logging
#    ceat_logging("collector")

    # Get comparison list
    comparison_name_list = comparison_list(collector_data_info, comparison_list_cnt_max=10).scenario_run()

    print("==================== {} worker start ====================".format(collector_data_info["target_mall"]))
    print(collector_data_info)
    print("========================================")

    if collector_data_info["target_mall"] == "Coupang" or collector_data_info["target_mall"] == "coupang" :
        coupang_scenario(collector_data_info, link_max_cnt=2000, step_get_links=True, step_get_comments=True).scenario_run(comparison_name_list)
    elif collector_data_info["target_mall"] == "Naver" or collector_data_info["target_mall"] == "naver" :
        naver_scenario(collector_data_info, link_max_cnt=2000, step_get_links=True, step_get_comments=True).scenario_run(comparison_name_list)
    else:
        print("Wrong target_mall")

    print("==================== {} worker  end  ====================".format(collector_data_info["target_mall"]))

@Collector.route('')
class ceat_collector(Resource):

    @Collector.expect(collector_model)
    def post(self):
        """ Collector 댓글 수집 """

        # init collector data
        collector_data_info = dict()
        collector_data_info["target_mall"] = request.json.get('target_mall')
        collector_data_info["search_key"] = request.json.get('search_key')
        collector_data_info["start_t"] = request.json.get('start_t')
        collector_data_info["end_t"] = request.json.get('end_t')

        p = multiprocessing.Process(name="{}".format(collector_data_info['target_mall']), target=ceat_collector_process, args=(collector_data_info,))
        p.start()
        ceat_collector_worker_list.append(p)

        return {"target_mall" : p.name,
                "pid" : p.pid,
                }, 200

@Collector.route('/<string:target_mall>')
class ceat_collector_worker(Resource):

    def get(self, target_mall):
        """ Collector 상태값 확인 (target_mall별) """

        collector_process_data = ""
        for i in range(0, len(ceat_collector_worker_list)):
            if target_mall in ceat_collector_worker_list[i].name:
                collector_process_data = ceat_collector_worker_list[i]
                break

        return {"target_mall" : collector_process_data.name,
                "pid" : collector_process_data.pid,
                "status" : collector_process_data.is_alive()
                }, 200

    def delete(self, target_mall):
        """ Collector 정지 및 삭제 (target_mall별) """

        collector_process_data = ""
        for i in range(0, len(ceat_collector_worker_list)):
            if target_mall in ceat_collector_worker_list[i].name:
                collector_process_data = ceat_collector_worker_list[i]
                break

        collector_process_data.terminate()
        collector_process_data.join()
        return 200
