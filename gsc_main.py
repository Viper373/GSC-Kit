# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :gsc_main.py
# @Time      :2024/10/10 18:44
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from run_task.run_task_indexing import RunTaskIndexing
from run_task.run_task_performance import RunTaskPerformance
from tool_utils.redis_utils import RedisUtils

redis_utils = RedisUtils()


if __name__ == '__main__':
    gsc_cookies_length = redis_utils.len_gsc_cookies()
    if gsc_cookies_length > 0:
        cookies = redis_utils.get_gsc_cookies()
        run_task_indexing = RunTaskIndexing(cookies)
        run_task_performance = RunTaskPerformance(cookies)
        # run_task_performance.run_performance()
        run_task_indexing.run_indexing()
