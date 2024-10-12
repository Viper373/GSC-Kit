# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :checks.py
# @Time      :2024/10/12 11:37
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from tool_utils.redis_utils import RedisUtils


class Check:
    def __init__(self):
        self.redis_utils = RedisUtils()

    def check_gsc_cookies(self) -> bool:
        """
        检查redis中是否有gsc的cookies
        :return: gsc的cookies 或 False
        """
        gsc_cookies_length = self.redis_utils.len_gsc_cookies()
        if gsc_cookies_length > 0:
            return True
        return False


if __name__ == '__main__':
    check = Check()
    result = check.check_gsc_cookies()
    print(result)
