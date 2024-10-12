# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :gsc_main.py
# @Time      :2024/10/10 18:44
# @Author    :Zhangjinzhao
# @Software  :PyCharm

from run_task.run_task_indexing import RunTaskIndexing
from run_task.run_task_performance import RunTaskPerformance

cookies = {
    "SEARCH_SAMESITE": "CgQIjpwB",
    "__Secure-ENID": "22.SE=XHRyeOx78dLkgsYyhsP7Si7UAhHXuAzLTtpAjDRkn3XESWcP4LtEUyYaj_5ttefZ6R2YnHvgTa3g7QBwTna6bIYXT7ntwxw9ZzQzNQO2o4cr3GK7Rwu-_7kq67ZQ72YOXwXFuhawwbK-X4LO6Z1coCAFRaWFL_CBPgaEpyxqUSfa4J_IVizj-wmeSg9dplWXkj-qkeixWdRlHMWgR5qPv77fxdEUEDj0WEvG-7dj_UHgQNnb4o0oPhP4PpQ4M2quMN1hq7N3o-Lb01z2gdTmu6N-P0Am-yhNN5TUb_Z8vDElLSPZnahbq1o",
    "AEC": "AVYB7crDsFWU1GGcpYfZL01-d6QXOtFD9RUUMJuxeTBrOkv2a-1zd0xwlQ",
    "OTZ": "7768898_24_24__24_",
    "_ga": "GA1.1.1821709462.1728437902",
    "SID": "g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDBAc6pJJ5LlaLRE0dXQauLQACgYKAeISARASFQHGX2MiAcSmCsVnWeOV_MscQRl6_xoVAUF8yKoqkqBcZ_pY2fAyZ4FaPCNh0076",
    "__Secure-1PSID": "g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDNp91cQoZE0ikEWaJd5NW0AACgYKAQcSARASFQHGX2MidmdYFZnAhoYKSvC1GCCSMhoVAUF8yKqu8nV1hV0KvxT89H4vC8Cu0076",
    "__Secure-3PSID": "g.a000pAjIQkOH-H35e0jDJRcfxuSUWYE4dN4rv32k0aAg8KCE6xuDHCFricdoBtEe2A8K5pjoRwACgYKAdYSARASFQHGX2MiXhvCscmj2LDB-R59kNxAwRoVAUF8yKrPfzBjDffSev1DPMCo4c2a0076",
    "HSID": "A05lE0OylGCUJ6nI1",
    "SSID": "APi45FV-MRDN7vMkB",
    "APISID": "wykiv6L5pNLxZk2B/AkW94piY0a-8bvSVd",
    "SAPISID": "xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT",
    "__Secure-1PAPISID": "xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT",
    "__Secure-3PAPISID": "xDVrp0VxBBWeBD77/A4Ad0UoMoVf-UDcVT",
    "NID": "518=AUVI1ArS52abtZdinujR5yjEdfc6Qo2368uBesI06o3MTq7hB0Q7adFme9rUtW5IIIUhywYYzUIwQB9jzIl7dsq6lMrf6dG34Z_OgZVlcQDL3j6tNBK0zD5dPIqizQzC6bYmmXzt6eHPsKjQlONyXSVG78JwfC-Kl44Z2B13OjBtmqcjDBZXCBjQ7Ghj8Ioyu8HqURmze-b6TwpWE-KDaFZ7xkyAYgJsufA7kZSyrXc89JZzJfCiZDei8ylEnc73P65qwdkPxZSyJSsPcVUzo8y6knLGyHFhBIeP6ZFIKuoRrGIEmytyO4GqdniMi5PgHSmIIgAyATR7ZXMpn23hW-ImJ6zPhmaKb2V3UrIfpmfO3BaeXQLALAeMlwBPy9zyM8Efh0-7kkBpeM5N9ye07pueP-xOqpxbZnhhlb17euYVSzu_DK46TRc6tXcnigb5HQmTenLiXXHBNN0uD63Ydhxvec9XP66BbYXINSTLG4dQuZ1QBBr14biXdoXzWyxUI_HGP9Vr7AqdP6u9ItIk6ASzJisf8nJVu4OatFTHzqCiLpVc7TOGBuX0r0T-eZdyMhCfkiBnmo0qhlLZgCVYxAiT-1bRT2_BUuTL-1byb1hBnHqPODBuAOUvP2xijIMPXrOJADzCtnm0xEWZbxzv8HZ7SUHkYYCfLjYN6Dw85odEGBrlZdO8Jr9orpj_Fr-UmLYFj5m8cWe045OPMvDJ1xAIVBhozsiDWh8rIrSWBFWjKe4q4TT0nKGwCWj0nf5-0RiHO-JD4eXBF3H9qNnrK1ts7VQciPXvqLUX5mgjvVQUaK4L-ul0OgxuPc07Kmjasz8fBOm9luKDEh6oedrsyeTf0vVV26dxTJXny5Y4WQ3BNfLEdQ-7xcNsb7s8nja2mlm6y45gzv3Xd4je0wfTktHK2uHLOIkztPCInv7bKprSqwWL2KqtT7HGZks3fRp0QE93n5FYbBjha-8byKPxSxLbM4JT51csE2o0DxvSAZChTymxvO3ZD7vqkElVHsw2jx3-FeuGg2WBWq0Z4MTN9RyeCtZHcIR-BzevUqaTA0-2zurJjUEgCAkX2YeN7E1EIib7wphgjQwMOIr_ktg",
    "__Secure-1PSIDTS": "sidts-CjIBQlrA-K1QI_ca-oc4qKI9UmGSUs9AO9b9XTCBUQtUG7qILxdTdk0hadot1Wkg7WbqehAA",
    "__Secure-3PSIDTS": "sidts-CjIBQlrA-K1QI_ca-oc4qKI9UmGSUs9AO9b9XTCBUQtUG7qILxdTdk0hadot1Wkg7WbqehAA",
    "SIDCC": "AKEyXzWKMjb6woM1C9p-28cc6WAHuWNDoKBxGID1S73f49ZpepGRSqoQvNG5xuKfc7QLw8tw7Y0",
    "__Secure-1PSIDCC": "AKEyXzXCyEPKLkrghhrUkgGyJ5SfXXDvm2mGXV93aO-Qsx4JNFMKTF2p3ezwTrJvg8BW7ryUDw",
    "__Secure-3PSIDCC": "AKEyXzU9wQ_ZKfhwEvzez91H9WcPLzPKTOFeInZ4Lo02-Au4iXEqfbt1fjWggDTRh_S44kTcpcg",
    "_ga_QX2LK1FZEG": "GS1.1.1728694633.10.1.1728694641.0.0.0"
}
run_task_indexing = RunTaskIndexing(cookies)
run_task_performance = RunTaskPerformance(cookies)

if __name__ == '__main__':
    # run_task_performance.run_performance()
    run_task_indexing.run_indexing()
