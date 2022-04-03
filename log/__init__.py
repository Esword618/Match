# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:19
# File : __init__.py.py
# Author : Esword

import os
import time

from loguru import logger

Nowadays = time.strftime("%Y-%m-%d", time.localtime())

logger.add(f"{os.getcwd()}/save/logs/{Nowadays}.log", rotation="5MB", encoding="utf-8", enqueue=True, compression="zip",retention="1 days")
