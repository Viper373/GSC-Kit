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

    @rich_logger
    def post_gsc_data(self, json_data: str, json_type: str, domain_str: str) -> bool:
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
            response = requests.post(url=self.gsc_api_base_url, headers=self.headers, json=json)
            if response.status_code == 200:
                return True
            else:
                rich_logger.error(f"GSC API 接口异常: {response.status_code}")
                return False
        except Exception as e:
            rich_logger.exception(f"GSC API 接口异常: {e}")
            return False


if __name__ == '__main__':
    api_utils = APIUtils()
    test_json = '{"test": "test"}'
    type_test = 'indexing'
    test_domain = 'test'
    api_utils.post_gsc_data(test_json, type_test, test_domain)
