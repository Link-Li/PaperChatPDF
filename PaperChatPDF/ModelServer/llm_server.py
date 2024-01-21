# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/21 00:11
@Author      : noahzhenli
@Email       : 
@Description : 
"""

import json
from datetime import datetime
from pathlib import Path
import uuid
import subprocess
import requests

from flask import app, request, Flask
from transformers import AutoTokenizer

from llm_server_config import TestingConfig
from prompt_process import yi_prompt_process


def init_tokenizer(app):
    return AutoTokenizer.from_pretrained(app.config["LLM_MODEL"], use_fast=False)


def test_llama_cpp(app):
    try:
        port = app.config["PORT"]
        host = app.config["HOST"]
        headers = {"Content-Type": "application/json"}
        prompt = yi_prompt_process([{"role": "user", "content": "你是谁？"}], llm_tokenizer)
        print("输入：", prompt)
        data_json = {
            "prompt": prompt,
            "n_predict": 4096,
            "stop": ["<|im_end|>"]
        }
        ip_url = f"http://{host}:{port}/completion"
        generate_info = None
        generate_info = requests.post(url=ip_url, json=data_json, headers=headers)
        generate_info = json.loads(generate_info.text)
        response = generate_info["content"]
        print("测试LLama cpp服务是否正常启动：", response)
    except Exception as e:
        print("LLama cpp服务未正常启动")
        print(e)
        print(generate_info)


app = Flask(__name__)
app.config.from_object(TestingConfig())
llm_tokenizer = init_tokenizer(app)
test_llama_cpp(app)


# 测试
@app.route('/', methods=["GET"])
def api_test():
    """
    测试服务器是否就绪

    Returns:
        str (str): Hello World Web Server!
    """
    return "Hello World LLM Server!"


# 解析PDF
@app.route("/llm_chat", methods=["POST"])
def llm_chat():
    """
    使用llm处理数据

    Args:
        message_list (list): 输入的数据 [{'role': 'user', 'content': xxx}, {'role': 'assistant', 'content': xxx}]
        temperature (float): 温度参数 default: 0.8
        top_k (float): top_k default: 40
        top_p (float): top_p default: 0.95
        repeat_penalty (float): 重复惩罚参数 default: 1.1
        n_predict (int): 生成的最长token数量 default: 2048
        stop (list): 停止字符 default:[]

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息
        response (str): 模型处理的结果
        predict_speed (str): 预测速度 token/s
        prompt_speed (str): prompt处理速度 token/s

    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    try:
        request_json = request.get_json()
        message_list = request_json.get("message_list", "")
        temperature = request_json.get("temperature", 0.8)
        top_k = request_json.get("top_k", 40)
        top_p = request_json.get("top_p", 0.95)
        repeat_penalty = request_json.get("repeat_penalty", 1.1)
        n_predict = request_json.get("n_predict", 2048)
        stop = request_json.get("stop", [])

        if len(message_list) == 0:
            response_msg["msg_code"] = 2
            response_msg["msg_content"] = "the length of message_list is 0, check message_list!"
            return response_msg

        prompt = yi_prompt_process(message_list, llm_tokenizer)

        port = app.config["PORT"]
        host = app.config["HOST"]
        headers = {"Content-Type": "application/json"}
        data_json = {
            "prompt": prompt,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "repeat_penalty": repeat_penalty,
            "n_predict": n_predict,
            "stop": stop
        }
        ip_url = f"http://{host}:{port}/completion"
        generate_info = requests.post(url=ip_url, json=data_json, headers=headers).json()
        response = generate_info["content"]
        predict_speed = "%.4f" % generate_info["timings"]["predicted_per_second"]
        prompt_speed = "%.4f" %  generate_info["timings"]["prompt_per_second"]
        response_msg["response"] = response
        response_msg["predict_speed"] = predict_speed
        response_msg["prompt_speed"] = prompt_speed

        return response_msg
    except Exception as e:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = str(e)


print("LLM server 启动完成")

if __name__ == '__main__':
    app.run(host="192.168.31.137", port=9001, debug=True)