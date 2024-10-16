# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :string_utils.py
# @Time      :2024/10/11 10:45
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import re
import json
import codecs
import hashlib
import requests
from typing import Any
from datetime import datetime
from urllib.parse import urlparse
from tool_utils.log_utils import RichLogger

rich_logger = RichLogger()


class StringUtils:

    @staticmethod
    def md5_encode(str_data: str) -> str:
        """
        对字符串进行MD5加密。
        :param str_data: 需要加密的字符串
        :return: 加密后的字符串
        """
        md5_value = hashlib.md5()
        md5_value.update(str_data.encode('utf-8'))
        return md5_value.hexdigest()

    @staticmethod
    def extract_gsc_version(url: str) -> str:
        """
        从URL中提取GSC版本号。

        :param url: 请求的URL
        :return: 版本号，例如 "1" 或者其他数字字符串。如果未找到，则返回空字符串。
        """
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        # 寻找'u'后面的数字，通常是path_parts[2]
        if len(path_parts) > 2 and path_parts[1] == 'u':
            return path_parts[2]
        return ''

    @staticmethod
    def extract_at_id(text: str) -> str:
        """
        从文本中提取at_id。

        :param text: 请求返回的文本
        :return: at_id字符串。如果未找到，则返回空字符串。
        """
        match = re.search(r'"SNlM0e":"(.*?)"', text)
        if match:
            at_id = match.group(1)
            return at_id
        return ''

    @staticmethod
    def extract_index(text: str) -> list:
        """
        从文本中提取所有以 'CAMY' 开头且长度为8的字符串，去重后返回列表。

        :param text: 请求返回的文本
        :return: 包含所有符合条件的字符串的列表
        """
        # 使用正则表达式匹配所有以 'CAMY' 开头且长度为8的字符串
        matches = re.findall(r'\bCAMY\w{4}\b', text)
        # 使用集合去重
        unique_matches = list(set(matches))
        return unique_matches

    @staticmethod
    def extract_domains(text: str) -> set:
        """
        从文本中提取所有域名，去除重复并返回集合。

        :param text: 请求返回的文本
        :return: 包含所有独特域名的集合，例如 {"sc-domain:brev.ai", "sc-domain:aicoloringpages.net"}
        """
        # 解码文本中的unicode转义字符
        decoded_text = codecs.decode(text, 'unicode_escape')
        # 使用正则表达式匹配所有 'sc-domain:' 后面的域名
        pattern = r'sc-domain:([a-zA-Z0-9.-]+)'
        domains = re.findall(pattern, decoded_text)
        # 加上前缀并去重
        unique_domains = set(f'sc-domain:{domain}' for domain in domains)
        return unique_domains

    @staticmethod
    @rich_logger
    def extract_excel_name(response: requests.Response, domain_str: str) -> bool | Any:
        """
        从响应头中提取Excel文件名。
        :param response: 响应对象
        :param domain_str: 域名字符串
        :return: 文件名字符串
        """
        content_disposition = response.headers.get('Content-Disposition', '')
        match = re.findall('filename="(.+)"', content_disposition)
        if match:
            return match[0]
        else:
            rich_logger.info(f"{domain_str.split(':')[-1]} 未验证，无法提取 Excel 文件名")
            return False

    @staticmethod
    def extract_indexing_reason(indexing_json: str) -> str:
        """
        提取索引原因。
        :param indexing_json: 索引JSON数据
        :return: 索引原因字符串
        """
        indexing_json = json.loads(indexing_json)
        for item in indexing_json.get("Metadata", []):
            if item.get("Property") == "Issue":
                return item.get("Value")
        return "未找到索引原因"

    @staticmethod
    def filter_chart_data(json_str: str, recent_date: str):
        """
        过滤 JSON 数据中的 Chart 字段，只保留日期大于等于 recent_date 的项。

        :param json_str: 传入的 JSON 字符串。
        :param recent_date: 最近日期，格式为 "YYYY-MM-DD"。
        :return: 过滤后的 JSON 数据。
        """
        data = json.loads(json_str)
        recent_date = datetime.strptime(recent_date, "%Y-%m-%d")
        # 过滤 Chart 字段
        filtered_chart = [
            entry for entry in data.get("Chart", [])
            if datetime.strptime(entry["Date"], "%Y-%m-%d") >= recent_date
        ]
        # 更新原数据中的 Chart 字段
        data["Chart"] = filtered_chart
        # 返回过滤后的 JSON 数据
        return json.dumps(data, ensure_ascii=False, indent=2)
