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
    "NID": "518=uld8-XHWxYNneDNdsZ0Xox1N4PNvlWZAUrIwEKslBICN0Bq7HlrYPEAQg61V4v9HkDJJNQI-9nv_bQnbORdQseD1jrlSOmeqbWfJ3WqRhWYzgaFuXXrqAClur0n71kNT55FHd5uJmr6w2HcjE-hzRyuJjZCCEge-jL1c_CfibFiuvEXANd5okgnGR0b7CF-t7UPZ3fTImX9eysuJ4tuvEvBCmYmSoWRJBemSPEbXlJ7Ny7iQnPJpMV3gyKhgM3eO5UB9KxDka-hBzC6z02KBL7nFXM4fV_XwdFrCUcaziAjVJgw0B7OA9KgU-3uCijWFqeC7QOAd8ghpgbKZgicQjub-dS0sLBM-6DHfZft-rvtMKrDX-GuvUtpP9nxRreRj_Ugeoc9pPvIl4RQEygg9EAamSqF7nwYgEfGuEnBIrcXeA0s3bxgrqj8lT8okKSP2UE3wIME1YMK8Hy0WFKPDtO0N2DcU_vBH62a8yd2lJjFr-bp0pNDPdT4MEjXL65IZpauMxrU2jcjqznx-wWrz9b2NsrlefVpMSNxcYD1Gp6mBieiNV0rpKfglC5ISzti57vENf5emrrMHZZ7fqPgNkN6d95vy159PKVXeDCGBhH6iffcYi2srTggwPFHDf_mi3aUJoD9H_gqhi4cbeeHWdclmHVpt_JhCS_LE9hZzMT4_XQZBaINEMwUn29RC7hcjrD_JeAXTmU7pakVfUgCsvnYmlWq-qvKVZ18W3xOoUDxD5ylbogMc_9YKppCBYNDClrJlQGFmnzJ5dUCuzn7aJsZAkkfYQ4C4lHzqcM6nj9jJwDYC9sX3kLm1-aIpEygyJm_Eu52hBZs4AWH_c7nNu6FiErCwAbdGZ1r68t-s_ygOv67_UmiWQjRTpm31CiwRPbnJg89G9quJOX7MyF2ZcjBaiZZoYs8hLNIUTrFviWm91PKu5nfQcUtLjXqJsI5Z97Ybx7cJYO3XhsPoRmyjR9BJQ4ZBX6U_SG0vf5qGfA8DPqEbRjYfGV3sOrgVFasJUjfP1Ru2YnGCXkqGrNF3xFw5EI0x-ykcOP1rBUSmfba1t5abUiVl7rcXnRopk3UjInBIGq2ZD4X8ckGEJNk",
    "__Secure-1PSIDTS": "sidts-CjIBQlrA-A9T3zkOls4x2Ybl47x8hTWUsyFe2KTfjT7hyDGUe-cEY2rON25SBi2vuVC6CBAA",
    "__Secure-3PSIDTS": "sidts-CjIBQlrA-A9T3zkOls4x2Ybl47x8hTWUsyFe2KTfjT7hyDGUe-cEY2rON25SBi2vuVC6CBAA",
    "SIDCC": "AKEyXzVrtMCa-Eec-37PoRZ_lZ11O6THbjE2-sG3zI_VYgPvKCr8pTjVsA85oEvYNStfKQsudpo",
    "__Secure-1PSIDCC": "AKEyXzV7xP8-SeKQ0M4C2yklT9CdkdFJLGAUzy5shjaeFleJvKKM41yXKl6muDyZ35wBvqJB2A",
    "__Secure-3PSIDCC": "AKEyXzWOUEX-dqRwNr_tDNxdXaPRNHIvVoidIeWx2DsHUzI2WsZ1L16DE20THTX1ajGjBrFy0QA",
    "_ga_QX2LK1FZEG": "GS1.1.1728637910.8.0.1728637910.0.0.0"
}
run_task_indexing = RunTaskIndexing(cookies)
run_task_performance = RunTaskPerformance(cookies)

if __name__ == '__main__':
    run_task_performance.run_performance()
    run_task_indexing.run_indexing()
