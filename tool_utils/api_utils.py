# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :api_utils.py
# @Time      :2024/10/12 10:34
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import requests
from tool_utils.log_utils import RichLogger

rich_logger = RichLogger()


class APIUtils:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.gsc_api_base_url = 'https://aiadmin.erweima.ai/api/gsc/acceptAndParseData'
        # self.gsc_api_base_url = 'https://1004-207-2-120-14.ngrok-free.app/api/gsc/acceptAndParseData'
        self.gsc_time_url = 'https://d8a4-103-134-34-68.ngrok-free.app/api/gsc/getDBMaxGscDate'

    @rich_logger
    def post_gsc_data(self, json_data: str, json_type: str, domain_str: str):
        """
        提供 GSC 数据。
        :param json_data: JSON 数据。
        :param json_type: JSON 数据类型。
        :param domain_str: 域名。
        :return: bool: 是否成功提供数据。
        """
        json = {
            'jsonData': json_data,
            'jsonType': json_type,
            'domain': domain_str.split(':')[-1],
        }
        try:
            response = requests.post(url=self.gsc_api_base_url, headers=self.headers, json=json, timeout=300)
            rich_logger.info(f"GSC Data API Status: {response.status_code}丨{response.text}")
        except Exception as e:
            rich_logger.exception(f"GSC API 接口异常: {e}")

    @rich_logger
    def get_recent_time(self, gscType: str, projectSource: str):
        """
        获取最近时间。
        :param gscType: 原因。
        :param projectSource: 域名。
        :return: str: 最近时间。
        """
        params = {
            'gscType': gscType,
            'projectSource': projectSource,
        }
        try:
            response = requests.get(url=self.gsc_time_url, headers=self.headers, params=params, timeout=300)
            rich_logger.info(f"GSC Time API Status: {response.status_code}丨{response.text}")
            if response.status_code == 200:
                if response.json()['code'] == 200:
                    recent_date = response.json()['data']
                    return recent_date
                else:
                    return None
            else:
                return None
        except Exception as e:
            rich_logger.exception(f"GSC Time API 接口异常: {e}")


if __name__ == '__main__':
    api_utils = APIUtils()
    gscType = 'Not found (404)'
    projectSource = 'aicoloringpages.net'
    date = api_utils.get_recent_time(gscType=gscType, projectSource=projectSource)
    print(type(date))
