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
# # file_path = root_path / "dataset/pdf_data/2312.09251.pdf"
# file_path = root_path / "dataset/pdf_data/Multimodal-Intelligence.pdf"
# # file_path = root_path / "dataset/pdf_data/test copy.pdf"
# title = "VL-GPT: A Generative Pre-trained Transformer for Vision and Language Understanding and Generation"
# abstract = """In this work, we introduce Vision-Language Generative
# Pre-trained Transformer (VL-GPT), a transformer model
# proficient at concurrently perceiving and generating visual
# and linguistic data. VL-GPT achieves a unified pre-training
# approach for both image and text modalities by employing a
# straightforward auto-regressive objective, thereby enabling
# the model to process image and text as seamlessly as a lan-
# guage model processes text. To accomplish this, we initially
# propose a novel image tokenizer-detokenizer framework for
# visual data, specifically designed to transform raw images
# into a sequence of continuous embeddings and reconstruct
# them accordingly. In combination with the existing text tok-
# enizer and detokenizer, this framework allows for the en-
# coding of interleaved image-text data into a multimodal
# sequence, which can subsequently be fed into the trans-
# former model. Consequently, VL-GPT can perform large-
# scale pre-training on multimodal corpora utilizing a uni-
# fied auto-regressive objective (i.e., next-token prediction).
# Upon completion of pre-training, VL-GPT exhibits remark-
# able zero-shot and few-shot performance across a diverse
# range of vision and language understanding and genera-
# tion tasks, including image captioning, visual question an-
# swering, text-to-image generation, and more. Additionally,
# the pre-trained model retrains in-context learning capabil-
# ities when provided with multimodal prompts. We further
# conduct instruction tuning on our VL-GPT, highlighting its
# exceptional potential for multimodal assistance.""".replace("\n", " ")
#
# # data_json = {"write_mode": "overwrite", "title": title, "abstract": abstract}
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
url = "http://127.0.0.1:8001/pdf/get_pdf_json"
data_json = {"pdf_id": "4"}
response = requests.get(url, data=data_json)
print(json.loads(response.headers["msg_code"]))
a = json.loads(response.text)
print(response.text[:100])
print(response.content.decode("utf-8")[:100])
a = 1




# 测试存储pdf的关键词
# url = "http://127.0.0.1:8001/pdf/set_pdf_attribute_info"
# data_json = {"data_id": "123", "file_name": "2312.09251.pdf.json"}
# response = requests.post(url, data=data_json)
# print(response)
# print(json.loads(response.text))
