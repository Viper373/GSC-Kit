# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :run_task_performance.py
# @Time      :2024/10/11 16:41
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import json
import requests
from run_task.run_task_get import RunTaskGet
from tool_utils.log_utils import RichLogger
from tool_utils.string_utils import StringUtils
from tool_utils.file_utils import ExcelManager, CustomJSONEncoder
from tool_utils.api_utils import APIUtils

rich_logger = RichLogger()
string_utils = StringUtils()
excel = ExcelManager()
api_utils = APIUtils()


class RunTaskPerformance:
    def __init__(self, cookies: dict):
        """
        初始化 RunTaskPerformance 类。
        :param cookies: 请求头中的 Cookies。
        """
        self.get = RunTaskGet(cookies)
        self.session = requests.Session()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-form-factors': '"Desktop"',
            'sec-ch-ua-full-version': '"129.0.6668.100"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.100", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-browser-channel': 'stable',
            'x-browser-copyright': 'Copyright 2024 Google LLC. All rights reserved.',
            'x-browser-validation': 'IrKrQbZgwzfhwxeKC1pprn3FhX8=',
            'x-browser-year': '2024',
            'x-client-data': 'CKe1yQEIkrbJAQiitskBCKmdygEIoYPLAQiWocsBCPKiywEIm/7MAQiFoM0BCKyezgEI/qXOAQi/ts4BCKK7zgEI2sLOAQjKxM4BCL7HzgEIp8jOAQivyM4BGPbJzQEYnLHOAQ==',
            'x-same-domain': '1',
        }
        self.cookies = cookies

    # def download_and_save_excel(self, domain_str: str, at_id: str):
    #     params = {
    #         'resource_id': f"{domain_str}",
    #         'num_of_days': '7',
    #         'request_type': '4',
    #         'at': f"{at_id}",
    #     }
    #     try:
    #         response = self.session.get('https://search.google.com/u/1/search-console/export/san', headers=self.headers, cookies=self.cookies, params=params)
    #         excel_name = string_utils.extract_excel_name(response, domain_str)
    #         excel.write_performance_excel(response, domain_str, excel_name)
    #     except Exception:
    #         return
    @rich_logger
    def performance_content_to_json(self, domain_str: str, at_id: str):
        """
        将Excel文件的二进制数据转换为json格式。
        :param domain_str: 域名字符串。
        :param at_id: at_id字符串。
        :return: json格式的Excel文件数据。
        """
        params = {
            'resource_id': f"{domain_str}",
            'num_of_days': '7',
            'request_type': '4',
            'at': f"{at_id}",
        }
        domain_str = domain_str.split(':')[-1]
        try:
            response = self.session.get('https://search.google.com/u/1/search-console/export/san', headers=self.headers, cookies=self.cookies, params=params)
            if response.status_code == 200:
                excel_json = excel.sheet_content_to_json(response)
                rich_logger.info(f"{domain_str} Excel文件转换为JSON成功")
                excel_json = json.dumps(excel_json, ensure_ascii=False, cls=CustomJSONEncoder, default=str)
                return excel_json
            else:
                rich_logger.error(f"{domain_str} Excel文件转换为JSON失败: {response.text}")
                return
        except Exception as e:
            rich_logger.exception(f"{domain_str} Excel文件转换为JSON失败: {e}")
            return

    @rich_logger
    def run_performance(self):
        """
        执行整个GSC-Performance爬取流程。
        """
        # 获取版本和at_id
        version, at_id = self.get.get_gsc_version_and_at_id()

        if not at_id:
            rich_logger.exception("未能获取到at_id，请更新cookies，终止程序。")
            return

        # 获取所有域名
        domains = self.get.get_domains(version=version, at_id=at_id)

        if not domains:
            rich_logger.exception("未找到任何域名，终止程序。")
            return

        # 遍历每个域名
        for domain_str in domains:
            # self.download_and_save_excel(domain_str, at_id)
            performance_json = self.performance_content_to_json(domain_str, at_id)
            if performance_json:
                api_utils.post_gsc_data(json_data=performance_json, json_type="performance")
            else:
                continue
