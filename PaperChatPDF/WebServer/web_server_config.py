# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/7 19:41
@Author      : noahzhenli
@Email       : 
@Description : 
"""

from pathlib import Path


class Config(object):
    JSON_AS_ASCII = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    ROOT_PATH = Path(__file__).parents[0]
    PDF_SAVE_PATH = ROOT_PATH / "temp/pdf"
    PDF_TXT_SAVE_PATH = ROOT_PATH / "temp/pdf_txt"
    PDF_JSON_SAVE_PATH = ROOT_PATH / "temp/pdf_json"
