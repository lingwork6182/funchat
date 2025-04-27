# -*- coding:utf-8 -*-
"""
@NAME: basic_config.py
@Auth: dabin
@Date: 2025/4/27
"""
import logging
import os
import shutil
import tempfile

import langchain

#是否显示详细日志
log_verbose = False
langchain.verbose = False

#日期格式
LOG_FORMAT = '%(asctime)s - %(filename)s[lineno]d - %(levelname)s: %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

#日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

#临时文件目录，主要用于对话
BASE_TEMP_DIR = os.path.join(tempfile.gettempdir(), 'funChat_temp')
try:
    shutil.rmtree(BASE_TEMP_DIR)
except Exception:
    pass
os.mkdirs(BASE_TEMP_DIR, exist_ok=True)

