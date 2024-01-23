# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/7 15:49
@Author      : noahzhenli
@Email       : 
@Description : 
"""
import json
import re
from datetime import datetime
from pathlib import Path
import uuid
import requests
import subprocess

from flask import app, request, Flask, send_file, make_response
from werkzeug.utils import secure_filename

from create_flask_app import create_app, db
from web_server_config import TestingConfig
from PDFParse.pdf_to_json import parse_pdf_to_txt, parse_pdf_text_to_json
from MySQL.table_class import PdfInfo
import default_prompts


app = create_app()

with app.app_context():
    db.create_all()

def check_file_type(filename, type):
    if '.' in filename and filename.split('.')[-1] == type:
        return True
    else:
        return False


# 测试
@app.route('/', methods=["GET"])
def api_test():
    """
    测试服务器是否就绪

    Returns:
        str (str): Hello World Web Server!
    """
    return "Hello World Web Server!"


@app.route("/get_system_info", methods=["GET"])
def get_system_info():
    """
    返回服务器的cpu利用率，gpu利用率和内存使用量

    :return:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息
        cpu_usage (float): cpu利用率
        mem_usage (float): 内存使用比例
        gpu_usage (float): gpu利用率
    """
    response_msg = {"msg_code": 0, "msg_content": ""}

    command = 'top -bn1 | grep "Cpu(s)" | sed "s/.*, *\\([0-9.]*\\)%* id.*/\\1/" | awk \'{print 100 - $1}\''
    cpu_usage_res = subprocess.run(command, shell=True, capture_output=True)
    if cpu_usage_res.returncode == 0:
        response_msg["cpu_usage"] = float(cpu_usage_res.stdout.decode("utf-8").strip())
    else:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] += f"get cpu info error {cpu_usage_res.stderr.decode('utf-8').strip()}"

    command = "free -m | sed -n '2p' | awk '{printf \"%f\",($3)/$2*100}'"
    mem_usage_res = subprocess.run(command, shell=True, capture_output=True)
    if mem_usage_res.returncode == 0:
        response_msg["mem_usage"] = float(mem_usage_res.stdout.decode("utf-8").strip())
    else:
        response_msg["msg_code"] = 2
        response_msg["msg_content"] += f"get memory info error {mem_usage_res.stderr.decode('utf-8').strip()}"

#         TODO: 获取GPU的利用率，使用nvidia-smi-py类的工具获取

    if response_msg["msg_code"] == 0:
        response_msg["msg_content"] = "success"
    return response_msg



# 解析PDF
@app.route("/pdf/parse_pdf_to_json", methods=["POST"])
def parse_pdf_to_json():
    """
    将传输过来的PDF文件，保存到指定的位置，并更新MySQL存储信息
    同时将PDF解析成json文件进行保存

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息
    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    file = request.files.get("file", None)
    request_json = request.form.to_dict()
    write_mode = request_json["write_mode"]
    if file is None:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = "No file in the request"
        return response_msg
    elif file.filename == '':
        response_msg["msg_code"] = 2
        response_msg["msg_content"] = "No upload file"
        return response_msg

    if file and check_file_type(file.filename, "pdf"):
        date_time = datetime.today().strftime("%Y%m%d%H")
        # date_time = "2024010723"
        file_id = str(uuid.uuid1())
        exist_flag = True  # 后续替换成mysql里面的查询结果
        if exist_flag and write_mode != "overwrite":
            response_msg["msg_code"] = 3
            response_msg["msg_content"] = "file exist and write_mode not set to overwrite, so the file not save"

        # 保存文件
        save_filename = secure_filename(file.filename)
        save_dir = app.config["PDF_SAVE_PATH"] / date_time
        Path.mkdir(save_dir, parents=True, exist_ok=True)
        pdf_save_path = save_dir / f"{file_id}-{save_filename}"
        file.save(pdf_save_path)

        # 将PDF文件解析成txt
        try:
            save_dir = app.config["PDF_TXT_SAVE_PATH"] / date_time
            Path.mkdir(save_dir, parents=True, exist_ok=True)
            pdf_txt_save_path = save_dir / f"{file_id}-{save_filename}.txt"
            parse_pdf_to_txt(pdf_save_path, pdf_txt_save_path)
        except Exception as e:
            response_msg["msg_code"] = 4
            response_msg["msg_content"] = f"parse pdf to txt error: {e}"
            return response_msg

        # 将PDF文件解析成json
        try:
            save_dir = app.config["PDF_JSON_SAVE_PATH"] / date_time
            Path.mkdir(save_dir, parents=True, exist_ok=True)
            pdf_json_save_path = save_dir / f"{file_id}-{save_filename}.json"
            pdf_json = parse_pdf_text_to_json(pdf_txt_save_path, pdf_json_save_path)
        except Exception as e:
            response_msg["msg_code"] = 5
            response_msg["msg_content"] = f"parse pdf txt to json error: {e}"
            return response_msg

        # 将解析之后的结果存入到数据库中
        try:
            title = request_json.get("title", None)
            abstract = request_json.get("abstract", None)
            if title is None:
                title = pdf_json["title"]
            if abstract is None:
                if pdf_json["content"][0][0].lower() == 'abstract':
                    abstract = pdf_json["content"][0][2][0]
                else:
                    abstract = ""
            pdf_info = PdfInfo(title=title, abstract=abstract, pdf_save_path=pdf_save_path, json_save_path=pdf_json_save_path)
            db.session.add(pdf_info)
            db.session.commit()
        except Exception as e:
            response_msg["msg_code"] = 6
            response_msg["msg_content"] = f"save pdf info to mysql error: {e}"
            return response_msg

    return response_msg


# 获取PDF解析之后的json数据
@app.route("/pdf/get_pdf_json", methods=["GET"])
def get_pdf_json():
    """
    返回解析成json之后的pdf内容，返回结果用json表示，存储在headers的msg_code中

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息

    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    request_json = request.get_json()
    pdf_id = request_json["pdf_id"]
    # 查数据库看文件是否存在，并获取文件的保存位置
    pdf_info = PdfInfo.query.filter_by(id=int(pdf_id)).first()
    if pdf_info:
        file_path = pdf_info.json_save_path
    else:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"id: {pdf_id}, file not found"
        response = make_response("file not found", 200)
        response.headers['msg_code'] = json.dumps(response_msg)
        return response

    response = make_response(send_file(file_path, as_attachment=True))
    response.headers['msg_code'] = json.dumps(response_msg)
    return response


# 对论文的摘要进行关键词提取
@app.route("/pdf/extract_abstract_core_keywords", methods=["GET"])
def extract_abstract_core_keywords():
    """
    抽取论文摘要的关键词，关键词用于索引论文

    Args:
        pdf_id (int): pdf的id号码

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息
        input (str): 输入模型的abstract
        keywords (str): 返回提取的关键词，每个关键词用chr(2)分割
        response (str): 模型生成的原始结果

    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    request_json = request.get_json()
    pdf_id = request_json["pdf_id"]
    # 查数据库看文件是否存在，并获取文件的json数据
    pdf_info = PdfInfo.query.filter_by(id=int(pdf_id)).first()
    abstract = ""
    if pdf_info:
        abstract = pdf_info.abstract
    else:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"id: {pdf_id}, file not found"
        response = make_response("file not found", 200)
        response.headers['msg_code'] = json.dumps(response_msg)
        return response

    if len(abstract) == 0:
        response_msg["msg_code"] = 2
        response_msg["msg_content"] = f"id: {pdf_id}, pdf not have abstract"
        response_msg["keywords"] = ""

    llm_api = app.config["LLM_URL"]
    message_list = [
        {"role": "user", "content": default_prompts.extract_abstract_core_keywords_prompt.format(prompt=abstract)}
    ]
    headers = {"Content-Type": "application/json"}
    data_json = {
        "message_list": message_list,
        "temperature": app.config["TEMPERATURE"],
        "top_k": app.config["TOP_K"],
        "top_p": app.config["TOP_P"],
        "repeat_penalty": app.config["REPETITION_PENALTY"],
        "n_predict": 4096,
        "stop": ["<|im_end|>"]
    }
    generate_info = requests.post(url=llm_api, data=json.dumps(data_json), headers=headers)
    generate_info = json.loads(generate_info.text)
    if generate_info["msg_code"] != 0:
        response_msg["msg_code"] = 3
        response_msg["msg_content"] = f"调用LLM接口失败：{generate_info['msg_content']}"

    response = generate_info["response"]
    def parse_response(response):
        res_list = response.split("\n")
        pattern = r'^\d+\.'
        kw_list = []
        for res in res_list:
            res = res.strip()
            if re.match(pattern, res):
                kw = re.sub(pattern, '', res).strip()
                kw_list.append(kw)
        parse_res = chr(2).join(kw_list)
        return parse_res

    abstract_core_keywords = parse_response(response)
    pdf_info.abstract_core_keywords = abstract_core_keywords
    pdf_info.abstract_llm_generates = response

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        response_msg["msg_code"] = 4
        response_msg["msg_content"] = f"将数据结果存储到mysql数据库出错：{e}"

    response_msg["keywords"] = abstract_core_keywords
    response_msg["response"] = response
    response_msg["input"] = abstract

    return response_msg


# 对论文的摘要进行关键词提取
@app.route("/pdf/extract_title_core_keywords", methods=["GET"])
def extract_title_core_keywords():
    """
    抽取论文摘要的关键词，关键词用于索引论文

    Args:
        pdf_id (int): pdf的id号码

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息
        input (str): 输入模型的title
        keywords (str): 返回提取的关键词，每个关键词用chr(2)分割
        response (str): 模型生成的原始结果

    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    request_json = request.get_json()
    pdf_id = request_json["pdf_id"]
    # 查数据库看文件是否存在，并获取文件的json数据
    pdf_info = PdfInfo.query.filter_by(id=int(pdf_id)).first()
    title = ""
    if pdf_info:
        title = pdf_info.title
    else:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"id: {pdf_id}, file not found"
        response = make_response("file not found", 200)
        response.headers['msg_code'] = json.dumps(response_msg)
        return response

    if len(title) == 0:
        response_msg["msg_code"] = 2
        response_msg["msg_content"] = f"id: {pdf_id}, pdf not have title"
        response_msg["keywords"] = ""

    llm_api = app.config["LLM_URL"]
    message_list = [
        {"role": "user", "content": default_prompts.extract_title_core_keywords_prompt.format(prompt=title)}
    ]
    headers = {"Content-Type": "application/json"}
    data_json = {
        "message_list": message_list,
        "temperature": app.config["TEMPERATURE"],
        "top_k": app.config["TOP_K"],
        "top_p": app.config["TOP_P"],
        "repeat_penalty": app.config["REPETITION_PENALTY"],
        "n_predict": 4096,
        "stop": ["<|im_end|>"]
    }
    generate_info = requests.post(url=llm_api, data=json.dumps(data_json), headers=headers)
    generate_info = json.loads(generate_info.text)
    if generate_info["msg_code"] != 0:
        response_msg["msg_code"] = 3
        response_msg["msg_content"] = f"调用LLM接口失败：{generate_info['msg_content']}"

    response = generate_info["response"]
    def parse_response(response):
        res_list = response.split("\n")
        pattern = r'^\d+\.'
        kw_list = []
        for res in res_list:
            res = res.strip()
            if re.match(pattern, res):
                kw = re.sub(pattern, '', res).strip()
                kw_list.append(kw)
        parse_res = chr(2).join(kw_list)
        return parse_res

    title_core_keywords = parse_response(response)
    pdf_info.title_core_keywords = title_core_keywords
    pdf_info.title_llm_generates = response

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        response_msg["msg_code"] = 4
        response_msg["msg_content"] = f"将数据结果存储到mysql数据库出错：{e}"

    response_msg["keywords"] = title_core_keywords
    response_msg["response"] = response
    response_msg["input"] = title

    return response_msg


# 对论文introduction部分进行总结


# 对给定的内容进行翻译



#






# 存储PDF的一些解析数据，例如关键词，总结，abstract中文翻译等等
@app.route("/pdf/set_pdf_attribute_info", methods=["POST"])
def set_pdf_attribute_info():
    """
    针对给定的pdf的id和文件名，将pdf的总结关键词存储到mysql中，并返回json格式的信息

    Returns:
        msg_code (int): 0表示正常，其他错误，见msg_content
        msg_content (str): 错误信息

    """
    response_msg = {"msg_code": 0, "msg_content": "success"}
    request_json = request.form.to_dict()
    file_id = request_json["data_id"]

    # 暂不实现，后续有需要再实现
    response_msg["msg_content"] = "The functionality of this interface has not been implemented yet. "

    # 如果存储失败，那么返回错误信息
    try:
        pass
    except Exception as e:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"save to mysql fail: {e}"

    return response_msg



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8001, debug=True)
