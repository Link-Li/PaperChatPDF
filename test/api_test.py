# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/7 20:41
@Author      : noahzhenli
@Email       : 
@Description : 
"""
import json

import requests
from pathlib import Path



# 测试服务是否正常
headers = {"Content-Type": "application/json"}
url = "http://127.0.0.1:8001"
print(requests.get(url, headers=headers))
print(requests.get(url, headers=headers).text)


# 测试上传PDF接口
# root_path = Path.cwd().parents[0]
#
# file_path = root_path / "dataset/pdf_data/2312.09251.pdf"
# # file_path = root_path / "dataset/pdf_data/test copy.pdf"
# a = file_path.name
# data_json = {"write_mode": "overwrite"}
# url = "http://127.0.0.1:8001/pdf/parse_pdf_to_json"
# files = {"file": (file_path.name, open(file_path, "rb"))}
#
# response = requests.post(url, files=files, data=data_json)
#
# files["file"][1].close()
# print(response)
# print(response.text)



# 测试获取PDF的json数据
# url = "http://127.0.0.1:8001/pdf/get_pdf_json"
# data_json = {"data_id": "123", "file_name": "2312.09251.pdf.json"}
# response = requests.get(url, data=data_json)
# print(json.loads(response.headers["msg_code"]))
# a = json.loads(response.text)
# print(response.text[:20])
# print(response.content.decode("utf-8")[:20])
# a = 1




# 测试存储pdf的关键词
url = "http://127.0.0.1:8001/pdf/set_pdf_attribute_info"
data_json = {"data_id": "123", "file_name": "2312.09251.pdf.json"}
response = requests.post(url, data=data_json)
print(response)
print(json.loads(response.text))
