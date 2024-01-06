# -*- coding: utf-8 -*-
"""
@Time        : 2023/11/30 11:33
@Author      : noahzhenli
@Email       : 
@Description :

gunicorn -c gunicorn_conf.py yi_server:app

"""


import os

# 如果机器没有安装cuda，pytorch安装了cuda-toolkit，要在import onnxruntime之前先import torch
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers.generation.utils import GenerationConfig
from peft import prepare_model_for_kbit_training
from flask import Flask, request
from llama_cpp import Llama


def set_process_gpu():
    # worker_id 从1开始，可以手工映射到对应的显卡
    worker_id = int(os.environ.get('APP_WORKER_ID', 1))
    gpu_index = worker_id - 1
    print('current worker id  {} set the gpu id :{}'.format(worker_id, gpu_index))
    return gpu_index, worker_id


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
os.environ["TOKENIZERS_PARALLELISM"] = "false"
worker_id = 0
batch_size = 1
max_length = 2048
gpu_index, worker_id = set_process_gpu()
torch.set_num_threads(8)


class ModelChat:
    def __init__(self,):
        # 模型加载
        model_file = "/data/zhenli/model_file/yi/01-ai--Yi-34B-Chat/ggml-model-q4_0.gguf"
        self.llm = Llama(model_path=model_file, verbose=True, n_ctx=4096, n_threads=16, n_gpu_layers=40)
        model_path = '/data/zhenli/model_file/yi/01-ai--Yi-34B-Chat'
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)

    def get_chat_res(self, message_list):
        input = self.tokenizer.apply_chat_template(conversation=message_list, tokenize=False,
                                                   add_generation_prompt=True)
        output = self.llm(input, temperature=0.6, top_p=0.8, repeat_penalty=1.1, max_tokens=4096, stop=["<|im_end|>"])
        return output


model_chat = ModelChat()


@app.route('/model_chat', methods=["POST"])
def get_model_chat():
    request_data = request.get_json()
    responese_data = {}
    message_list = request_data["message_list"]

    responese_data["message_list"] = message_list
    responese_data["response"] = model_chat.get_chat_res(message_list)
    return responese_data


@app.route('/', methods=["GET"])
def test():
    return "hello world"

# if __name__ == '__main__':
#     app.run(host='9.134.253.154', port=9020)