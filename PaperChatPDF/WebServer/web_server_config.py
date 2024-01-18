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
    SQLALCHEMY_DATABASE_URI = ""
    def __init__(self):
        # 临时的配置，后续可以删除
        config_dict = {}
        with open("temp/env.txt", "r", encoding="utf-8") as f_read:
            for data_line in f_read.readlines():
                data_split = data_line.strip("\n").split("=")
                config_dict[data_split[0]] = data_split[1]
        mysql_url = config_dict["mysql_url"]
        self.SQLALCHEMY_DATABASE_URI = mysql_url


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    ROOT_PATH = Path(__file__).parents[0]
    PDF_SAVE_PATH = ROOT_PATH / "temp/pdf"
    PDF_TXT_SAVE_PATH = ROOT_PATH / "temp/pdf_txt"
    PDF_JSON_SAVE_PATH = ROOT_PATH / "temp/pdf_json"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
