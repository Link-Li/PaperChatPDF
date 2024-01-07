# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/7 15:49
@Author      : noahzhenli
@Email       : 
@Description : 
"""
import json
from datetime import datetime
from pathlib import Path

from flask import app, request, Flask, send_file, make_response
from werkzeug.utils import secure_filename

from web_server_config import TestingConfig
from PDFParse.pdf_to_json import parse_pdf_to_txt, parse_pdf_text_to_json



app = Flask(__name__)
app.config.from_object(TestingConfig())


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


# 解析PDF
@app.route("/pdf/parse_pdf_to_json", methods=["POST"])
def parse_pdf_to_json():
    """
    将传输过来的PDF文件，保存到指定的位置，并更新MySQL存储信息
    同时将PDF解析成json文件进行保存

    Returns:
        response_msg (str):
            返回处理之后的结果。
            "msg_code": 0:正常；其他表示出现错误，错误信息见msg_content。
            "msg_content": 错误信息。
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
        # 保存到mysql里面，并获取文件id
        # date_time = datetime.today().strftime("%Y%m%d%H")
        date_time = "2024010723"
        file_id = "123"
        exist_flag = True  # 后续替换成mysql里面的查询结果
        if exist_flag and write_mode != "overwrite":
            response_msg["msg_code"] = 3
            response_msg["msg_content"] = "file exist and write_mode not set to overwrite, so the file not save"

        # 保存文件
        save_filename = secure_filename(file.filename)
        save_dir = app.config["PDF_SAVE_PATH"] / date_time / f"{file_id}"
        Path.mkdir(save_dir, parents=True, exist_ok=True)
        pdf_save_path = save_dir / f"{save_filename}"
        file.save(pdf_save_path)

        # 将PDF文件解析成txt
        try:
            save_dir = app.config["PDF_TXT_SAVE_PATH"] / date_time / f"{file_id}"
            Path.mkdir(save_dir, parents=True, exist_ok=True)
            pdf_txt_save_path = save_dir / f"{save_filename}.txt"
            parse_pdf_to_txt(pdf_save_path, pdf_txt_save_path)
        except Exception as e:
            response_msg["msg_code"] = 4
            response_msg["msg_content"] = f"parse pdf to txt error: {e}"
            return response_msg

        # 将PDF文件解析成txt
        try:
            save_dir = app.config["PDF_JSON_SAVE_PATH"] / date_time / f"{file_id}"
            Path.mkdir(save_dir, parents=True, exist_ok=True)
            pdf_json_save_path = save_dir / f"{save_filename}.json"
            parse_pdf_text_to_json(pdf_txt_save_path, pdf_json_save_path)
        except Exception as e:
            response_msg["msg_code"] = 5
            response_msg["msg_content"] = f"parse pdf txt to json error: {e}"
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
    request_json = request.form.to_dict()
    file_id = request_json["data_id"]
    file_name = request_json["file_name"]
    # 查数据库看文件是否存在，并获取文件的保存位置
    file_exist_flag = True

    # 后期换成正常mysql的路径
    date_time = "2024010723"
    file_path = app.config["PDF_JSON_SAVE_PATH"] / date_time / f"{file_id}/{file_name}"

    if not file_exist_flag:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"{file_id}-{file_name} file not found"
        response = make_response("file not found", 200)
        response.headers['msg_code'] = json.dumps(response_msg)
        return response_msg

    response = make_response(send_file(file_path, as_attachment=True))
    response.headers['msg_code'] = json.dumps(response_msg)
    return response


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
    file_name = request_json["file_name"]

    # 如果存储失败，那么返回错误信息
    try:
        pass
    except Exception as e:
        response_msg["msg_code"] = 1
        response_msg["msg_content"] = f"save to mysql fail: {e}"

    return response_msg



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8001, debug=True)
