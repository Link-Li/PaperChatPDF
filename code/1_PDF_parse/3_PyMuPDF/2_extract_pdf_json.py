# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/20 19:53
@Author      : noahzhenli
@Email       : 
@Description : 
"""

import re
import json
import sys, pathlib, fitz


def update_add_dict_value(up_dict, key, value):
    if up_dict.get(key, None) is None:
        up_dict[key] = value
    else:
        up_dict[key] += value


def get_max_dict_value(get_dict):
    max_res = [0, 0]  # [key, num]
    for key, res in get_dict.items():
        if res > max_res[1]:
            max_res = [key, res]
    return max_res


file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/2312.09251.pdf"
# file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/ICON.pdf"
# file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/Multimodal-Intelligence.pdf"

save_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/output_data/2312.09251.json"
# save_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/output_data/ICON.json"

# 正文的字体大小
paper_content_size = 0
# 正文最左边的x轴位置
paper_content_left_bbox = 0
# 正文最右边的x轴位置
paper_content_right_bbox = 400
# 正文最上边的y轴位置
paper_content_top_bbox = 0
# 正文最下面边的x轴位置
paper_content_bottom_bbox = 800

with fitz.open(file_path) as doc:  # open document
    # 读取所有文本的字号，用来确认正文的字号，将大于正文字号的作为标题候选，小于正文字号的删除
    word_size_dict = {}
    # 读取所有的坐标
    left_bbox_dict = {}
    right_bbox_dict = {}
    top_bbox_dict = {}
    bottom_bbox_dict = {}
    # 读取摘要的坐标
    abstract_bbox = []

    # 读取所有文本的开头坐标，来进行区分不同的段落
    # 段落相关的变量

    for page in doc:
        # page_text_json = json.loads(page.get_text("json", sort=True))
        page_text_json = page.get_text("dict", sort=True)
        for block in page_text_json["blocks"]:
            bbox = block["bbox"]
            update_add_dict_value(left_bbox_dict, bbox[0], 1)
            update_add_dict_value(right_bbox_dict, bbox[2], 1)
            update_add_dict_value(top_bbox_dict, bbox[1], 1)
            update_add_dict_value(bottom_bbox_dict, bbox[3], 1)
            if len(block) == 4 and block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"])
                        text = span["text"]
                        update_add_dict_value(word_size_dict, size, len(text.split(" ")))

                        if "abstract" == text.strip().lower() and len(abstract_bbox) == 0:
                            abstract_bbox = span["bbox"]

                        # if word_size_dict.get(size, None) is None:
                        #     word_size_dict[size] = len(text.split(" "))
                        # else:
                        #     word_size_dict[size] += len(text.split(" "))

    # max_num_size = [0, 0]  # [size, num]
    # for size, num in word_size_dict.items():
    #     if num > max_num_size[1]:
    #         max_num_size = [size, num]
    paper_content_size = get_max_dict_value(word_size_dict)[0]
    paper_content_left_bbox = get_max_dict_value(left_bbox_dict)[0] - 10
    paper_content_right_bbox = get_max_dict_value(right_bbox_dict)[0] + 10
    paper_content_top_bbox = get_max_dict_value(top_bbox_dict)[0] - 10
    paper_content_bottom_bbox = get_max_dict_value(bottom_bbox_dict)[0] + 10

    page_text = []
    title_list = []  # 标题候选
    section_dict = {} # 章节标题及对应的内容
    for index, page in enumerate(doc):
        page_text_json = json.loads(page.get_text("json", sort=False))
        image_info = page.get_image_info()
        table_info = page.find_tables().tables
        image_text_set = set()
        table_text_set = set()

        # 读取图片中的文本
        if len(image_info) > 0:
            image_bbox = [image_info[0]["bbox"][0], image_info[0]["bbox"][1],
                          image_info[0]["bbox"][2], image_info[0]["bbox"][3]]
            for img in image_info:
                image_bbox = [min(image_bbox[0], img["bbox"][0]), min(image_bbox[1], img["bbox"][1]),
                              max(image_bbox[2], img["bbox"][2]), max(image_bbox[3], img["bbox"][3])]
            image_text_set = set(page.get_text(clip=image_bbox).split("\n"))

        # 读取表格中的文本
        if len(table_info) > 0:
            tabel_bbox = [table_info[0].bbox[0], table_info[0].bbox[1],
                          table_info[0].bbox[2], table_info[0].bbox[3]]
            for tab in table_info:
                tabel_bbox = [min(tabel_bbox[0], tab.bbox[0]), min(tabel_bbox[1], tab.bbox[1]),
                              max(tabel_bbox[2], tab.bbox[2]), max(tabel_bbox[3], tab.bbox[3])]
            table_text_set = set(page.get_text(clip=tabel_bbox).split("\n"))

        # 获取标题的粗糙信息，存储在title_list中
        if index == 0:
            for block in page_text_json["blocks"]:
                bbox = block["bbox"]
                if len(block) == 4 and block["type"] == 0:
                    line_text = []
                    line_size = 0
                    for line in block["lines"]:
                        span_text = []
                        for span in line["spans"]:
                            size = round(span["size"])
                            text = span["text"]
                            if size > paper_content_size:
                                span_text.append(text)
                                line_size = size
                        span_text = " ".join(span_text).strip()
                        if len(span_text) > 0 and "arxiv" not in span_text.lower()\
                                and "abstract" not in span_text.lower()\
                                and "introduction" not in span_text.lower()\
                                and not span_text.isdigit()\
                                and span_text not in image_text_set\
                                and span_text not in table_text_set:
                            if span_text[-1] == "-":
                                span_text = span_text[:-1]
                            else:
                                span_text += " "
                            line_text.append([line_size, span_text])
                    # line_text = "\n".join(line_text)
                    if len(line_text) > 0:
                        title_list.append([bbox, line_text])

        # 抽取论文主要内容，并对不同段落进行分段落，同时识别小标题，并对小标题下面的内容进行区分
        block_text = []
        for block in page_text_json["blocks"]:
            if len(block) == 4 and block["type"] == 0:
                line_text = []
                for line in block["lines"]:
                    span_text = []
                    for span in line["spans"]:
                        size = round(span["size"])
                        text = span["text"]
                        if index == 0 and span["bbox"][1] < (abstract_bbox[1] - 5):
                            text = ""
                        if size == paper_content_size:
                            span_text.append(text)
                    span_text = " ".join(span_text).strip()
                    if len(span_text) > 0 \
                            and not span_text.isdigit()\
                            and span_text not in image_text_set\
                            and span_text not in table_text_set:
                        if span_text[-1] == "-":
                            span_text = span_text[:-1]
                        else:
                            span_text += " "
                        line_text.append(span_text)
                if len(line_text) > 0:
                    line_text = "\n".join(line_text)
                    block_text.append(line_text)
        block_text = "\n".join(block_text)
        page_text.append(block_text)
    page_text = "\n\n%\n\n".join(page_text)


    # 抽取标题
    extract_title = ""
    title_top_bbox = 10000
    for bbox, title_info in title_list:
        if bbox[1] < title_top_bbox:
            title_top_bbox = bbox[1]
            extract_title = title_info
    extract_title = " ".join([t[1] for t in extract_title]).replace("  ", " ")




    # 去除引用标志，类似[ 34 , 35 , 49 ]
    page_text = re.sub("\[[0-9, ]*\]", "", page_text)
    # page_text = re.sub("\([0-9a-zA-Z., ]*\)", "", page_text)
    # 正向预查询，去除类似( Ekman , 1993 ; Datcu and Rothkrantz , 2008 )
    page_text = re.sub("\((?=.*\d{4})(?=.*[a-zA-Z]).*\)", "", page_text)




    with open(save_path, "w", encoding="utf-8") as f_write:
        f_write.write(extract_title)
        f_write.write("\n\n\n\n\n")
        f_write.write(page_text)




