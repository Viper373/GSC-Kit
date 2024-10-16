# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :run_task_indexing.py
# @Time      :2024/10/10 18:35
# @Author    :Zhangjinzhao
# @Software  :PyCharm
import json
import time
import requests
from run_task.run_task_get import RunTaskGet
from tool_utils.log_utils import RichLogger
from tool_utils.string_utils import StringUtils
from tool_utils.file_utils import ExcelManager, CustomJSONEncoder
from tool_utils.api_utils import APIUtils
from tool_utils.proxy_utils import ProxyUtils

rich_logger = RichLogger()
string_utils = StringUtils()
excel = ExcelManager()
api_utils = APIUtils()
proxy_utils = ProxyUtils()


class RunTaskIndexing:
    def __init__(self, cookies: dict):
        """
        初始化 GSC_Scraper 类，设置所有必要的 headers、cookies、params 和 URLs。
        :param cookies: 登录后的 cookies
        """
        self.get = RunTaskGet(cookies)
        self.session = requests.session()
        self.cookies = cookies
        self.index_url = 'https://search.google.com/u/{}/_/SearchConsoleAggReportUi/data/batchexecute'
        self.index_headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://search.google.com/',
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
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-client-data': 'CKe1yQEIkrbJAQiitskBCKmdygEIoYPLAQiWocsBCPKiywEIm/7MAQiFoM0BCKyezgEI/qXOAQi/ts4BCKK7zgEI2sLOAQjKxM4BCL7HzgEIp8jOAQivyM4BGPbJzQEYnLHOAQ==',
            'x-same-domain': '1',
        }
        self.index_params = {
            'rpcids': 'nDAfwb,OLiH4d,B2IOAd,xDwXKd',
            'source-path': '/u/1/search-console/index',
            'f.sid': '',
            'bl': '',
            'hl': 'en',
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            '_reqid': '',
            'rt': 'c',
        }
        self.export_url = 'https://search.google.com/u/1/search-console/export/index/drilldown'

    def get_indexes(self, domain_str, at_id, version):
        """
        获取指定域名的所有索引。
        :param domain_str: 域名字符串
        :param at_id: at_id
        :param version: GSC 版本
        :return: list of indexes
        """
        index_data = {
            "f.req": f"[[[\"nDAfwb\",\"[\\\"{domain_str}\\\",35,[[12,null,null,null,null,null,null,null,null,null,null,3],[9,\\\"\\\"],[26,null,null,null,null,null,null,null,null,null,4]]]\",null,\"1\"],[\"nDAfwb\",\"[\\\"{domain_str}\\\",35,[[12,null,null,null,null,null,null,null,null,null,null,3],[9,\\\"\\\"],[26,null,null,null,null,null,null,null,null,null,2]]]\",null,\"2\"],[\"OLiH4d\",\"[\\\"{domain_str}\\\",30,[[12,null,null,null,null,null,null,null,null,null,null,3],[9,\\\"\\\"]]]\",null,\"3\"],[\"B2IOAd\",\"[\\\"{domain_str}\\\",[[4,null,null,null,null,null,[null,null,null,[null,null,null,null,null,null,null,null,[3,\\\"\\\",null,2]]]]]]\",null,\"5\"],[\"czrWJf\",\"[\\\"{domain_str}\\\",7,1]\",null,\"6\"],[\"xDwXKd\",\"[\\\"{domain_str}\\\",7]\",null,\"10\"],[\"mKtLlc\",\"[\\\"{domain_str}\\\"]\",null,\"11\"]]]",
            "at": f"{at_id}",
            "": ""
        }
        formatted_index_url = self.index_url.format(version)
        try:
            response = self.session.post(
                url=formatted_index_url,
                headers=self.index_headers,
                cookies=self.cookies,
                params=self.index_params,
                data=index_data
            )
            if response.status_code == 200:
                index_list = string_utils.extract_index(response.text)
                rich_logger.info(f"{domain_str.split(':')[-1]} 索引列表长度: {len(index_list)}")
                return index_list
            else:
                rich_logger.error(f"{domain_str.split(':')[-1]} 获取索引失败: {response.status_code}丨{response.text}")
                return []
        except Exception as e:
            rich_logger.exception(f"{domain_str.split(':')[-1]} 获取索引失败: {e}")
            return []

    # def download_and_save_excel(self, domain_str: str, index: str, at_id: str):
    #     """
    #     下载并保存Excel文件。
    #     :param domain_str: 域名字符串
    #     :param index: 索引
    #     :param at_id: at_id
    #     """
    #     pages_excel_headers = {
    #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #         'accept-language': 'zh-CN,zh;q=0.9',
    #         'cache-control': 'no-cache',
    #         'pragma': 'no-cache',
    #         'priority': 'u=0, i',
    #         'referer': 'https://search.google.com/',
    #         'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    #         'sec-ch-ua-arch': '"x86"',
    #         'sec-ch-ua-bitness': '"64"',
    #         'sec-ch-ua-form-factors': '"Desktop"',
    #         'sec-ch-ua-full-version': '"129.0.6668.100"',
    #         'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.100", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.100"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-model': '""',
    #         'sec-ch-ua-platform': '"Windows"',
    #         'sec-ch-ua-platform-version': '"19.0.0"',
    #         'sec-ch-ua-wow64': '?0',
    #         'sec-fetch-dest': 'document',
    #         'sec-fetch-mode': 'navigate',
    #         'sec-fetch-site': 'same-origin',
    #         'sec-fetch-user': '?1',
    #         'upgrade-insecure-requests': '1',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    #         'x-browser-channel': 'stable',
    #         'x-browser-copyright': 'Copyright 2024 Google LLC. All rights reserved.',
    #         'x-browser-validation': 'g+9zsjnuPhmKvFM5e6eaEzcB1JY=',
    #         'x-browser-year': '2024',
    #         'x-client-data': 'CKe1yQEIkrbJAQiitskBCKmdygEIoYPLAQiWocsBCPKiywEIm/7MAQiFoM0BCKyezgEI/qXOAQi/ts4BCKK7zgEI2sLOAQjKxM4BCL7HzgEIp8jOAQivyM4BGPbJzQEYnLHOAQ==',
    #     }
    #     pages_excel_params = {
    #         'resource_id': f'{domain_str}',
    #         'item_key': f'{index}',
    #         'request_type': '4',
    #         'at': f'{at_id}'
    #     }
    #     try:
    #         response = self.session.get(
    #             url='https://search.google.com/u/1/search-console/export/index/drilldown',
    #             headers=pages_excel_headers,
    #             cookies=self.cookies,
    #             params=pages_excel_params
    #         )
    #         excel.write_indexing_excel(response, domain_str, index)
    #     except Exception:
    #         return
    @rich_logger
    def indexing_content_to_json(self, domain_str: str, at_id: str, index: str):
        """
        将Excel文件的二进制数据转换为json格式。
        :param domain_str: 域名字符串。
        :param at_id: at_id字符串。
        :param index: 索引字符串。
        :return: json格式的Excel文件数据。
        """
        pages_excel_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://search.google.com/',
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
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
            'x-browser-channel': 'stable',
            'x-browser-copyright': 'Copyright 2024 Google LLC. All rights reserved.',
            'x-browser-validation': 'g+9zsjnuPhmKvFM5e6eaEzcB1JY=',
            'x-browser-year': '2024',
            'x-client-data': 'CKe1yQEIkrbJAQiitskBCKmdygEIoYPLAQiWocsBCPKiywEIm/7MAQiFoM0BCKyezgEI/qXOAQi/ts4BCKK7zgEI2sLOAQjKxM4BCL7HzgEIp8jOAQivyM4BGPbJzQEYnLHOAQ==',
        }
        pages_excel_params = {
            'resource_id': f'{domain_str}',
            'item_key': f'{index}',
            'request_type': '4',
            'at': f'{at_id}'
        }
        try:
            response = self.session.get(
                url=self.export_url,
                headers=pages_excel_headers,
                cookies=self.cookies,
                params=pages_excel_params
            )
            if response.status_code == 200:
                excel_json = excel.sheet_content_to_json(response)
                rich_logger.info(f"{domain_str.split(':')[-1]} {index} Excel文件转换为JSON成功")
                excel_json = json.dumps(excel_json, ensure_ascii=False, cls=CustomJSONEncoder, default=str)
                return excel_json
            elif response.status_code == 400:
                rich_logger.error(
                    f"{domain_str.split(':')[-1]} {index} Excel文件转换为JSON失败[{response.status_code}]: {response.text}")
                return
        except Exception as e:
            rich_logger.exception(f"{domain_str.split(':')[-1]} {index} Excel文件转换为JSON失败: {e}")
            return

    @rich_logger
    def run_indexing(self):
        """
        执行整个GSC-Indexing爬取流程。
        """

        rich_logger.logger.info(f'开始执行任务，获取到cookie:{self.cookies}')

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
            # 获取该域名的所有索引
            index_list = self.get_indexes(domain_str=domain_str, at_id=at_id, version=version)

            if not index_list:
                rich_logger.exception(f"未找到域名 {domain_str} 的任何索引。")
                continue

            # 遍历每个索引并下载Excel文件
            for index in index_list:
                indexing_json = self.indexing_content_to_json(domain_str, at_id, index)
                if indexing_json:
                    reason = string_utils.extract_indexing_reason(indexing_json=indexing_json)
                    recent_date = api_utils.get_recent_time(gscType=reason, projectSource=domain_str.split(":")[-1])
                    if recent_date is not None:
                        # 处理逻辑
                        indexing_json = string_utils.filter_chart_data(json_str=indexing_json, recent_date=recent_date)
                    # 上传API
                    string_utils.set_null_excel_sheet(indexing_json=indexing_json, sheet_name='Table')
                    api_utils.post_gsc_data(json_data=indexing_json, json_type='indexing', domain_str=domain_str)
                    rich_logger.info(f"{domain_str.split(':')[-1]} {index} 数据已成功上传至API。")
                else:
                    rich_logger.error(f"{domain_str.split(':')[-1]} {index} 数据上传至API失败。")
                    continue
                time.sleep(1)
