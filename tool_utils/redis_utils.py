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
        self.redis_connect_host = 'r-rj9l0g0zs12vuf60mrpd.redis.rds.aliyuncs.com'
        self.redis_connect_port = 6379
        self.redis_connect_user_pwd = 'testdaily:testdaily!1024'

        # redis连接地址 国内
        # self.redis_connect_host = 'r-2zepo0pzaiiicdhv29pd.redis.rds.aliyuncs.com'
        # self.redis_connect_port = 6379
        # self.redis_connect_user_pwd = 'testdaily:testdaily!1024'


class RedisUtils:
    def __init__(self):
        redis_config = RedisConfig()
        self.redis_db_number = 13  # redis数据库编号
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
    cookies_str = 'SEARCH_SAMESITE=CgQIjpwB; __Secure-ENID=22.SE=XHRyeOx78dLkgsYyhsP7Si7UAhHXuAzLTtpAjDRkn3XESWcP4LtEUyYaj_5ttefZ6R2YnHvgTa3g7QBwTna6bIYXT7ntwxw9ZzQzNQO2o4cr3GK7Rwu-_7kq67ZQ72YOXwXFuhawwbK-X4LO6Z1coCAFRaWFL_CBPgaEpyxqUSfa4J_IVizj-wmeSg9dplWXkj-qkeixWdRlHMWgR5qPv77fxdEUEDj0WEvG-7dj_UHgQNnb4o0oPhP4PpQ4M2quMN1hq7N3o-Lb01z2gdTmu6N-P0Am-yhNN5TUb_Z8vDElLSPZnahbq1o; AEC=AVYB7crDsFWU1GGcpYfZL01-d6QXOtFD9RUUMJuxeTBrOkv2a-1zd0xwlQ; OTZ=7768898_24_24__24_; _ga=GA1.1.1821709462.1728437902; SID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDBAc6pJJ5LlaLRE0dXQauLQACgYKAeISARASFQHGX2MiAcSmCsVnWeOV_MscQRl6_xoVAUF8yKoqkqBcZ_pY2fAyZ4FaPCNh0076; __Secure-1PSID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDNp91cQoZE0ikEWaJd5NW0AACgYKAQcSARASFQHGX2MidmdYFZnAhoYKSvC1GCCSMhoVAUF8yKqu8nV1hV0KvxT89H4vC8Cu0076; __Secure-3PSID=g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDHCFricdoBtEe2A8K5pjoRwACgYKAdYSARASFQHGX2MiXhvCscmj2LDB-R59kNxAwRoVAUF8yKrPfzBjDffSev1DPMCo4c2a0076; HSID=A05lE0OylGCUJ6nI1; SSID=APi45FV-MRDN7vMkB; APISID=wykiv6L5pNLxZk2B/AkW94piY0a-8bvSVd; SAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; __Secure-1PAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; __Secure-3PAPISID=xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT; NID=518=QWsLmJC5de1EhKAwGNwC5tZtYDdKzI7LZjv0DQev56E5S9hCJBNn41LrJ4fTScNHfp9agvkBEFnOplfnr_kehh0eW_sQuJSPl_mbG12SbaMC_I8fhzgXnVip98I_vY4KI44rSL3nSwJV_z3nJRsyE1gDbIQSTr8J6fT8Ixmd9g3_yfLy6oMQHByed5z9YWIznFTEyiMgq7wcsAh5ltbcoBpUU93Yd8zxkJgSuOb35sL7plwcu8hsmu3NAf5ouysMKDKfbm6WLCZ7F3l5TVI8f5cryVtXbeoJsOQ1kciYFVzqsEfFuv6zwWBgiNeIDKNaFYB6syOJV3a3cl00eZikB4fm5Er7bCbB-wfRIDNCOLu6QrRa7Up610C-4zaiDJyBbF_qd4eiiRQKCjB3Kjaqqyi_Hb7aZki1YNV1RxD9iMoyePbN98lj_MwSvFV801LMbps477v42Fo37BS8SvrN9KM8keoe5OeFmVvvtDCTB3TTca46L-tLsPOV-nVHp6NHf_qbwiLCz7OtNAE2wh9ubQ-736Gg0v2oMvRVpiU6SOuixMtJjAg3RKSmVhpuNGKvDz_CbBMMf2T0AEap8RZQKKbZBPSL65DVuUgQ2RevY4Wan4CxsHOe-qs2ly3vw9TuCcr0zycAUAk3IiRIamZXJLpghrHbqRnr0qZkYeNZ9fa2ENFFoEwfcHl7i4S_C0_rNSgs-6iBucOqLXXQN1qxYmTUg18RiyEOXRtRQh2jfsNAADVw503VbZ0oQ0TVqFLCiYzCsXBkAITBpve9qS_9xMdVEQh1SRL3z8vAUv8F9G9QiX5iYg9X15b7wepPFyBb2-kKws4MFajsRGXKBataKKmSwd68qga7CM3VDqLkDNP4hlNPQwl40TZzC1VtzJXitMgC-nz9iRZSNx4bDNgiN666ePF1xSsq6Htyfnfw58Vxq8wnDNT9tPBJU5fhqVDHHG6WjTrE0T78bc_APeCfAkaVeAxKNXrvcQdphiuOlidcVYayOZ3P782pNLmVmlx6VCGsrYjTGzxUYDzc04yLx7vd6nlnEeTYEDeIp_KHedbd4t8GzDQ48LjEtDaOQT91FdXjpVz_n_XqCNiWVuc; __Secure-1PSIDTS=sidts-CjIBQlrA-PQNUyYfh2sHbWT5wLSdVZV2uQ6w7zdnQiK4zPLFgrT4G1J_JPVCT4y86VWAjBAA; __Secure-3PSIDTS=sidts-CjIBQlrA-PQNUyYfh2sHbWT5wLSdVZV2uQ6w7zdnQiK4zPLFgrT4G1J_JPVCT4y86VWAjBAA; SIDCC=AKEyXzXncwJUWK9V_WktK5h6VMiCyKeDGgxp4NfbM64VWg0bQalEMaLwSpkFzbH4KFC8JTLf2wQ; __Secure-1PSIDCC=AKEyXzXCGRzGDsbLF7S-hVm1isl2X418a_OH1HK1DEsmvjysF9lriWVk-xXxxWFwn1hmA_wnfw; __Secure-3PSIDCC=AKEyXzUCi-FH0-Wu4ICOxjO9lj9rzJriHeEDOf9xVwyL4CsVf98SQ3-Lqt04yJ60w7ftpbD9RFg; _ga_QX2LK1FZEG=GS1.1.1728703519.11.0.1728703521.0.0.0'

    # 设置 cookies
    redis_utils.set_gsc_cookies(cookies_str)
