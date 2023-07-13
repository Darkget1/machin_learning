from ceat_crawling.ceat_collector import ceat_collector_process
import multiprocessing
ceat_collector_worker_list = list()

collector_data_info = dict()
collector_data_info["target_mall"] = 'coupang'
collector_data_info["search_key"] = '코유산균'
collector_data_info["start_t"] = '2023-01-01'
collector_data_info["end_t"] = '2023-06-30'

p = multiprocessing.Process(name="{}".format(collector_data_info['target_mall']), target=ceat_collector_process,
                            args=(collector_data_info,))
p.start()
ceat_collector_worker_list.append(p)
