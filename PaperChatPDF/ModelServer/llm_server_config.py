# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/21 00:12
@Author      : noahzhenli
@Email       : 
@Description :

scp -r /path/to/local/code lizhen@192.168.31.137:/path/to/remote/destination
"""


from pathlib import Path


class Config(object):
    JSON_AS_ASCII = False
    def __init__(self):
        pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    ROOT_PATH = Path(__file__).parents[0]
    # LLAMA_SERVER = "/home/lizhen/test/code/llama.cpp/server"
    # LLM_MODEL_PATH = "/home/lizhen/test/model_file/01-yi/Yi-34B-Chat/ggml-model-q4_0.gguf"
    # GPU_NGL = 0
    # THREADS = 4
    # CTX_SIZE = 4096  # size of the prompt context
    # SPLIT_MODE = "layer"
    LLM_MODEL = "/home/lizhen/test/model_file/01-yi/Yi-34B-Chat"
    PORT = 9000
    HOST = "192.168.31.137"

