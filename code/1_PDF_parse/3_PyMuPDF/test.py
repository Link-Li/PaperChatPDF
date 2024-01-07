# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/20 17:08
@Author      : noahzhenli
@Email       : 
@Description : 
"""


# import sys, pathlib, fitz
#
#
# file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/2312.09251.pdf"
# # file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/Multimodal-Intelligence.pdf"
# with fitz.open(file_path) as doc:  # open document
#     # all_text = [page.get_text("blocks", sort=True) for page in doc]
#     #
#     # tables = [page.find_tables() for page in doc]
#     #
#     # tab_text = [tab.extract() for tab in doc[6].find_tables().tables]
#     #
#     text = doc[1].get_text(clip=(67, 88.0, 525.0, 296.0), sort=True)
#     page = doc[1]
#     # 创建一个矩形，
#     # fitz.Rect(x1, y1, x2, y2) 创建矩形的参数分别为左下角和右上角的坐标
#     rect = fitz.Rect([419.8441162109375, 163.2222442626953, 526.967529296875, 210.7807159423828])
#
#     # 在页面上添加矩形
#     # 添加边框使用insert_annot或者insert_rect，
#     # 添加填充矩形使用add_rect, 它不会创建一个注解，而是将矩形作为页面内容的一部分。
#     page.draw_rect(rect, color=fitz.utils.getColor("red"), width=1.5)
#     doc.save("/data_cbs/zhenli/code/PaperChatPDF/dataset/output_data/test.pdf")
#
#     a = 1


# write as a binary file to support non-ASCII characters
# pathlib.Path(file_path + ".txt").write_bytes(text.encode())

a = 1


import pdf_to_json
import os

root_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))

file_path = root_path + "/dataset/pdf_data/2312.09251.pdf"
save_path = root_path + "/dataset/output_data/api_2312.09251.txt"

pdf_to_json.parse_pdf_to_txt(file_path, save_path)

file_path = root_path + "/dataset/output_data/api_2312.09251.txt"
save_path = file_path + ".json"
pdf_to_json.parse_pdf_text_to_json(file_path, save_path)

