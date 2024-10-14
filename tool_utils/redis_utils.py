# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :redis_utils.py
# @Time      :2024/10/12 11:10
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import redis
from tool_utils.log_utils import RichLogger

rich_logger = RichLogger()


class RedisConfig:
    def __init__(self):
        # # redis连接地址 国外
        self.redis_connect_host = 'r-2zepo0pzaiiicdhv29pd.redis.rds.aliyuncs.com'
        self.redis_connect_port = 6379
        self.redis_connect_user_pwd = 'testdaily:testdaily!1024'

        # redis连接地址 国内
        # self.redis_connect_host = 'r-2zepo0pzaiiicdhv29pd.redis.rds.aliyuncs.com'
        # self.redis_connect_port = 6379
        # self.redis_connect_user_pwd = 'testdaily:testdaily!1024'


class RedisUtils:
    def __init__(self):
        redis_config = RedisConfig()
        self.redis_db_number = 0  # redis数据库编号
        self.gsc_cookies_list_key = 'td:gsc:bot:cookies:list'  # gsc_cookies哈希
        # 实现一个连接池
        redis_pool = redis.ConnectionPool(
            host=redis_config.redis_connect_host,
            port=redis_config.redis_connect_port,
            password=redis_config.redis_connect_user_pwd,
            db=self.redis_db_number,
            decode_responses=True  # 设置为True，表示返回的数据是str类型，而不是bytes类型
        )
        self.redis_conn = redis.StrictRedis(connection_pool=redis_pool)

    def set_gsc_cookies(self, cookies):
        """
        将 cookies 字符串直接推送到 Redis 列表。
        :param cookies: cookies 字符串，例如 "key1=value1; key2=value2; ..."
        """
        if cookies:
            self.redis_conn.lpush(self.gsc_cookies_list_key, cookies)

    def get_gsc_cookies(self):
        """
        从 Redis 列表中弹出最新的 cookies 字符串，并将其解析为字典。
        :return: 包含所有 cookies 的字典，如果列表为空则返回空字典
        """
        try:
            # 弹出最右边的元素（最早推送的）
            cookies_string = self.redis_conn.rpop(self.gsc_cookies_list_key)
            if cookies_string:
                # 将 cookies 字符串解析为字典
                cookies_dict = {}
                for cookie in cookies_string.split(';'):
                    cookie = cookie.strip()
                    if '=' in cookie:
                        key, value = cookie.split('=', 1)
                        cookies_dict[key.strip()] = value.strip()
                return cookies_dict
            else:
                return {}
        except redis.RedisError as e:
            return {e}
        except Exception as e:
            return {e}

    @rich_logger
    def len_gsc_cookies(self):
        """
        获取 Redis 列表中存储的 cookies 数量。
        :return: 整数，表示存储的 cookies 的数量
        """
        try:
            count = self.redis_conn.llen(self.gsc_cookies_list_key)
            if count > 0:
                rich_logger.info(f"Redis 中有 {count} 个 GSC Cookies，开始执行任务。")
                return count
            else:
                rich_logger.warning("Redis 中没有 GSC Cookies，任务结束。")
                return 0
        except redis.RedisError as e:
            return 0


if __name__ == '__main__':
    redis_utils = RedisUtils()

    # 示例 cookies 字符串
    cookies_str = 'SEARCH_SAMESITE=CgQIjpwB; __Secure-ENID=22.SE=XHRyeOx78dLkgsYyhsP7Si7UAhHXuAzLTtpAjDRkn3XESWcP4LtEUyYaj_5ttefZ6R2YnHvgTa3g7QBwTna6bIYXT7ntwxw9ZzQzNQO2o4cr3GK7Rwu-_7kq67ZQ72YOXwXFuhawwbK-X4LO6Z1coCAFRaWFL_CBPgaEpyxqUSfa4J_IVizj-wmeSg9dplWXkj-qkeixWdRlHMWgR5qPv77fxdEUEDj0WEvG-7dj_UHgQNnb4o0oPhP4PpQ4M2quMN1hq7N3o-Lb01z2gdTmu6N-P0Am-yhNN5TUb_Z8vDElLSPZnahbq1o; AEC=AVYB7crDsFWU1GGcpYfZL01-d6QXOtFD9RUUMJuxeTBrOkv2a-1zd0xwlQ; OTZ=7768898_24_24__24_; _ga=GA1.1.1821709462.1728437902; SID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDBAc6pJJ5LlaLRE0dXQauLQACgYKAeISARASFQHGX2MiAcSmCsVnWeOV_MscQRl6_xoVAUF8yKoqkqBcZ_pY2fAyZ4FaPCNh0076; __Secure-1PSID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDNp91cQoZE0ikEWaJd5NW0AACgYKAQcSARASFQHGX2MidmdYFZnAhoYKSvC1GCCSMhoVAUF8yKqu8nV1hV0KvxT89H4vC8Cu0076; __Secure-3PSID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDHCFricdoBtEe2A8K5pjoRwACgYKAdYSARASFQHGX2MiXhvCscmj2LDB-R59kNxAwRoVAUF8yKrPfzBjDffSev1DPMCo4c2a0076; HSID=A05lE0OylGCUJ6nI1; SSID=APi45FV-MRDN7vMkB; APISID=wykiv6L5pNLxZk2B/AkW94piY0a-8bvSVd; SAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; __Secure-1PAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; __Secure-3PAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; NID=518=oGECHxuiK79WGMTMeFcUx1j_mePujDM84seIdeub6OkIMYQBsu0QAye9GyzR7OXPPf1RsNvr8gzGjwBCqHWIT1uI7luVLJl2w2_EvlAeT_sXyqURp1W0Dprd7Z7Pfg8lc0n6iTvLDLDgLinzYpQ2MhXZ8nMvnY4qJjqGa0sJI_dJYkt0Nb52zbvWqRvQj75cWo4vGJ4okCk1gqvjR41l-R6hW3yBoG12PRazr_mNRtR6MDjVnAxJcLCGkhZ22q1qcfWOoNK0LW9vIlIjpoH_7Fzyq04mG64KFSNt8VvcENcyXZSc5LDG1g0174b1kqX3hwpBa-MpILKncczpKXiVPRcaKJeDw5H99OAGX-esUpqX6aoKNLY15yvvFPgNkYIyYV2U1uIXgzcEvd06inFAyuEjiaEi9YTSelKSKruKXd42Fe7c4LgPVjIZFQP52_h-q-X9BYa14oEHEjDHdtiTrw69M0NZy6QCXDl66t9sj96i-cEbsjHfTAN1Eq4TiJQj4qJKe8Vu2jFqlAflFqnkPaxUWGlp3ermcyUSpTM0O3zHIoJexYk3kOnPg5Zt-bfKHzwmfGx3PirzX-DtxkexJzYEUchhM4zyl_WBzD4eAU0GjtdF4BBAZVK-kcq5JBXZbm6KJj5owI-0_axpLEeQ7FMTtcyr_TATPFtTj8UiBNZX7YaOET4RL1QdDZ_MJnOJATkQhKv0bkg44TVnyCtehlCdETTc1M61I9TOysDF6RA94KPGGiJegawnHSuT8sAq1tdE8Kpmvkcz4X3qY8UzyOpAu9uUxgjz7FhH2uS6G0uP0L4mrq0YXlw-9tFSNpf08wkoHxrdSel8IG-yCH88Rne2zs8lyW1bSFhckt1dY1OxUkf_66iTpZMfWS6Y-Qp6PAY33C1JmG3xwU4Zc_T85Y0jWlMHEej_9O8dDF5MjhOkAJwy4AeU6MRsrJL3LQLFcDumGqoprZAscxqH1ILL1hYIF6Rb8fmeOMZpklOD_nrLR_rBwQnJzyLLffdZOZC9nsaMSbm8-ELoqzW1W9P18II_2ZBcBIXXW7yeaedTHzP-zg0dEBfqBV4TUDzERjSdimXMUrz4j2Af2YUK4tY; __Secure-1PSIDTS=sidts-CjIBQlrA-LCzWBMRDmqr1DIPsH1nFHYt_nbGWz1hq2O1JefOt0RetDOJM34lsPukZuCzKBAA; __Secure-3PSIDTS=sidts-CjIBQlrA-LCzWBMRDmqr1DIPsH1nFHYt_nbGWz1hq2O1JefOt0RetDOJM34lsPukZuCzKBAA; SIDCC=AKEyXzVmour9G6fgotLrzcjY_ij1A5kiL6YJxD4cAt-id4aUvNKXehhJ50nCvv0bKS7vtrDO24Y; __Secure-1PSIDCC=AKEyXzVd2RdWxY3N1oquXpf7v7zEPD7qcPHK-b6TKVUkKol4FXTBsTXMpqgTRpE_kwOJlOAEzA; __Secure-3PSIDCC=AKEyXzV5VctH-qIJZZ-rF_4oFl2yeap6NV0Zb-WnG6mZz_8AKiP1QLmMhOuf0UpQLlMJafhEUuM; _ga_QX2LK1FZEG=GS1.1.1728868964.14.1.1728875974.0.0.0'

    # 设置 cookies
    redis_utils.set_gsc_cookies(cookies_str)
