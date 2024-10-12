# -*- coding: utf-8 -*-
# @Project   :td_gsc_scraper
# @FileName  :decorator_utils.py
# @Time      :2024/10/6 14:59
# @Author    :Zhangjinzhao
# @Software  :PyCharm

import os
import sys
import json
import time
import logging
from datetime import datetime
from rich.logging import RichHandler
from functools import wraps


class JSONFormatter(logging.Formatter):
    """自定义 JSON 格式化器，将日志记录转换为 JSON 格式。"""

    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).strftime("[%Y/%m/%d | %H:%M:%S]"),
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)


class RichLogger:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RichLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger_name: str = "RichLogger", level: str = "INFO"):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self.logger.propagate = False  # 防止日志重复

        if not self.logger.handlers:
            # 创建日志目录
            current_date = datetime.now().strftime("%Y-%m-%d")  # 格式：YYYY-MM-DD
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(project_root, "logs", current_date)
            os.makedirs(logs_dir, exist_ok=True)

            script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            info_log_path = os.path.join(logs_dir, f"{script_name}_info.log")
            error_log_path = os.path.join(logs_dir, f"{script_name}_error.log")
            error_json_log_path = os.path.join(logs_dir, f"{script_name}_error_json.log")

            # 文件处理器（INFO 及 WARNING 级别）
            info_handler = logging.FileHandler(info_log_path, encoding='utf-8')
            info_handler.setLevel(logging.INFO)
            # 添加过滤器，排除 ERROR 及以上级别
            info_handler.addFilter(lambda record: record.levelno < logging.ERROR)
            info_formatter = logging.Formatter(
                "%(asctime)s %(levelname)-8s %(message)s",
                datefmt="[%Y/%m/%d | %H:%M:%S]"
            )
            info_handler.setFormatter(info_formatter)

            # 文件处理器（ERROR 及 CRITICAL 级别）
            error_handler = logging.FileHandler(error_log_path, encoding='utf-8')
            error_handler.setLevel(logging.ERROR)
            error_formatter = logging.Formatter(
                "%(asctime)s %(levelname)-8s %(message)s",
                datefmt="[%Y/%m/%d | %H:%M:%S]"
            )
            error_handler.setFormatter(error_formatter)

            # 文件处理器（ERROR 及 CRITICAL 级别，JSON 格式）
            error_json_handler = logging.FileHandler(error_json_log_path, encoding='utf-8')
            error_json_handler.setLevel(logging.ERROR)
            json_formatter = JSONFormatter()
            error_json_handler.setFormatter(json_formatter)

            # Rich 处理器（控制台）
            rich_handler = RichHandler(rich_tracebacks=True)
            rich_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            rich_formatter = logging.Formatter(
                "{message}",
                style="{",
                datefmt="[%Y/%m/%d | %H:%M:%S]"
            )
            rich_handler.setFormatter(rich_formatter)

            # 添加处理器到日志器
            self.logger.addHandler(info_handler)
            self.logger.addHandler(error_handler)
            self.logger.addHandler(error_json_handler)
            self.logger.addHandler(rich_handler)

    def log_method(self, func):
        """装饰器，用于记录函数执行的日志和耗时"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            # 设置 stacklevel=3 以跳过装饰器和 RichLogger 的调用帧，获取实际调用者
            self.logger.info(f"▶️ 开始 '{func_name}'", stacklevel=3)
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                self.logger.info(f"⏹️ 结束 '{func_name}'| 耗时 {elapsed_time:.4f}s", stacklevel=3)
                return result
            except Exception as e:
                self.logger.exception(f"Exception in '{func_name}': {e}", stacklevel=3)
                raise

        return wrapper

    @staticmethod
    def get_signature(args, kwargs):
        """获取函数签名字符串。"""
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        return ", ".join(args_repr + kwargs_repr)

    def __call__(self, func):
        """使类实例可以用作装饰器"""
        return self.log_method(func)

    # 其他日志方法可以直接通过 self.logger 调用，并设置 stacklevel=2 以获取实际调用者
    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def exception(self, message):
        self.logger.exception(message, stacklevel=2)
