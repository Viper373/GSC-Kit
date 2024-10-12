# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :run_task_get.py
# @Time      :2024/10/11 16:46
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import requests
import warnings
from tool_utils.decorator_utils import RichLogger
from tool_utils.string_utils import StringUtils
from tool_utils.file_utils import ExcelManager

warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')
rich_logger = RichLogger()
string_utils = StringUtils()
excel = ExcelManager()


class RunTaskGet:
    def __init__(self, cookies):
        """
        初始化 RunTaskGet 类。
        :param cookies: cookies 字典。
        """
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
        self.params = {
            'resource_id': 'sc-domain:brev.ai',
        }
        self.start_url = 'https://search.google.com/u/1/search-console/index'
        self.base_url = 'https://search.google.com/u/{}/search-console/index'
        self.domains_url = 'https://search.google.com/u/{}/_/SearchConsoleAggReportUi/data/batchexecute'
        self.domains_data_template = 'f.req=[[["BWF8he","[]",null,"generic"]]]&at={}'
        self.domains_headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://search.google.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://search.google.com/',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-form-factors': '"Desktop"',
            'sec-ch-ua-full-version': '"130.0.2849.13"',
            'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.19", "Microsoft Edge";v="130.0.2849.13", "Not?A_Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'x-same-domain': '1',
        }
        self.domains_params = {
            'rpcids': 'BWF8he',
            'source-path': '/u/2/search-console/index',
            'f.sid': '371691613736909429',
            'bl': 'boq_searchconsoleserver_20241009.02_p0',
            'hl': 'en',
            'soc-app': '1',
            'soc-platform': '1',
            'soc-device': '1',
            '_reqid': '1068404',
            'rt': 'c',
        }

    @rich_logger
    def get_gsc_version_and_at_id(self):
        """
        获取 GSC 版本和 at_id。
        :return: tuple(version, at_id)
        """
        try:
            response = self.session.get(url=self.start_url, headers=self.headers, cookies=self.cookies, allow_redirects=False)
            if response.status_code == 302:
                # 从重定向的Location中提取版本
                location = response.headers.get('Location', '')
                version = string_utils.extract_gsc_version(location)
                rich_logger.info(f"gsc_version: {version}")
                # 构建新的URL并发送GET请求
                new_url = self.base_url.format(version)
                response = self.session.get(url=new_url, headers=self.headers, cookies=self.cookies, params=self.params, allow_redirects=False)
                at_id = string_utils.extract_at_id(response.text)
                rich_logger.info(f"at_id: {at_id}")
                return version, at_id
            else:
                # 如果没有重定向，直接从响应中提取at_id
                at_id = string_utils.extract_at_id(response.text)
                rich_logger.info(f"at_id: {at_id}")
                return None, at_id
        except Exception as e:
            rich_logger.exception(f"获取GSC版本和at_id失败: {e}")
            return None, None

    @rich_logger
    def get_domains(self, version, at_id):
        """
        获取所有域名。
        :param version: GSC 版本
        :param at_id: at_id
        :return: list of domains
        """
        formatted_data = self.domains_data_template.format(at_id)
        formatted_domains_url = self.domains_url.format(version)
        try:
            response = self.session.post(
                url=formatted_domains_url,
                headers=self.domains_headers,
                cookies=self.cookies,
                params=self.domains_params,
                data=formatted_data
            )
            if response.status_code == 200:
                domains = string_utils.extract_domains(response.text)
                rich_logger.info(f"域名列表长度: {len(domains)}")
                return domains
            else:
                rich_logger.error(f"获取域名失败: {response.status_code}")
                return []
        except Exception as e:
            rich_logger.exception(f"获取域名失败: {e}")
            return []
