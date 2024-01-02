# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/20 19:53
@Author      : noahzhenli
@Email       : 
@Description : 
"""

import os
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


# 获取正文的开头和结尾x轴坐标
# 获取正文的开头和结尾x轴坐标
def get_content_begin_end_bbox(bbox_list):
    global width, height, axis_error, max_num_line_length
    paper_content_begin_bbox, paper_content_end_bbox = [], []
    begin_bbox_dict = {}
    end_bbox_dict = {}
    line_length_dict = {}
    for bbox in bbox_list:
        update_add_dict_value(begin_bbox_dict, round(bbox[0]), 1)
        update_add_dict_value(end_bbox_dict, round(bbox[2]), 1)
        update_add_dict_value(line_length_dict, round(bbox[2] - bbox[0]), 1)
    begin_bbox_sort = sorted(begin_bbox_dict.items(), key=lambda x: x[1], reverse=True)
    end_bbox_sort = sorted(end_bbox_dict.items(), key=lambda x: x[1], reverse=True)
    line_length_sort = sorted(line_length_dict.items(), key=lambda x: x[1], reverse=True)
    max_num_line_length = line_length_sort[0][0]
    if max_num_line_length / width < 0.5:
        paper_content_begin_bbox = [begin_bbox_sort[0][0]-axis_error, begin_bbox_sort[1][0]-axis_error]
        paper_content_end_bbox = [end_bbox_sort[0][0]+axis_error, end_bbox_sort[1][0]+axis_error]
    else:
        paper_content_begin_bbox = [begin_bbox_sort[0][0]-axis_error]
        paper_content_end_bbox = [end_bbox_sort[0][0]+axis_error]

    # if (begin_bbox_sort[0][1] / len(bbox_list) - begin_bbox_sort[1][1] / len(bbox_list) < 0.05) and (end_bbox_sort[0][1] / len(bbox_list) - end_bbox_sort[1][1] / len(bbox_list) < 0.05):
    #     paper_content_begin_bbox = [begin_bbox_sort[0][0], begin_bbox_sort[1][0]]
    #     paper_content_end_bbox = [end_bbox_sort[0][0], end_bbox_sort[1][0]]
    # else:
    #     paper_content_begin_bbox = [begin_bbox_sort[0][0]]
    #     paper_content_end_bbox = [end_bbox_sort[0][0]]
    paper_content_begin_bbox.sort()
    paper_content_end_bbox.sort()
    return paper_content_begin_bbox, paper_content_end_bbox



root_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))

# file_path = root_path + "/dataset/pdf_data/2312.09251.pdf"
file_path = root_path + "/dataset/pdf_data/ICON.pdf"
# file_path = root_path + "/dataset/pdf_data/Self-Alignment.pdf"
# file_path = root_path + "/dataset/pdf_data/Multimodal-Intelligence.pdf"

# save_path = root_path + "/dataset/output_data/2312.09251.json"
save_path = root_path + "/dataset/output_data/ICON.json"
# save_path = root_path + "/dataset/output_data/Self-Alignment.json"
# save_path = root_path + "/dataset/output_data/Multimodal-Intelligence.json"

# 防止误检测的泛化位置偏差
axis_error = 2
# 正文一行的长度
max_num_line_length = 0
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
# 正文开头x轴位置，可能有1-2个
paper_content_begin_bbox = []
# 正文结尾x轴位置，可能有1-2个
paper_content_end_bbox = []
# 文档的大小
width, height = 0, 0
# 将所有的图片和文本的说明都存储起来，然后放到最后进行解析
block_table_img_list = []
block_table_img_id_set = set()

with fitz.open(file_path) as doc:  # open document
    # 读取所有文本的字号，用来确认正文的字号，将大于正文字号的作为标题候选，小于正文字号的删除
    word_size_dict = {}
    # 读取图片或者表格的文本字号
    table_img_content_size_dict = {}
    # 读取所有的坐标
    left_bbox_dict = {}
    right_bbox_dict = {}
    top_bbox_dict = {}
    bottom_bbox_dict = {}
    # 读取摘要的坐标，用于区分正文部分和标题部分
    abstract_bbox = []
    # 读取摘要的字号大小，用来获取其他标题
    abstract_size = 0
    # 获取introduction的字号大小，要求introduction的文本要以数字开头
    introduction_size = 0
    # 标题是否需要大于等于正文字体大小
    title_size_big_than_paper_content_size = False
    # 保存所有的bbox坐标
    bbox_list = []

    # 判断文本开头是否为figure 1或者table 1开头的正则
    match_table_img_patter = re.compile("^(figure|table)(\s?)(\d+)")

    # 读取所有文本的开头坐标，来进行区分不同的段落
    # 段落相关的变量

    for page in doc:
        # page_text_json = json.loads(page.get_text("json", sort=True))
        page_text_json = page.get_text("dict", sort=True)
        width, height = round(page_text_json["width"]), round(page_text_json["height"])
        for block in page_text_json["blocks"]:
            bbox = block["bbox"]
            update_add_dict_value(left_bbox_dict, bbox[0], 1)
            update_add_dict_value(right_bbox_dict, bbox[2], 1)
            update_add_dict_value(top_bbox_dict, bbox[1], 1)
            update_add_dict_value(bottom_bbox_dict, bbox[3], 1)
            if len(block) == 4 and block["type"] == 0:
                for line in block["lines"]:
                    bbox_list.append(line["bbox"])
                    for span in line["spans"]:
                        size = round(span["size"])
                        text = span["text"]
                        update_add_dict_value(word_size_dict, size, len(text.split(" ")))
                        # bbox_list.append(span["bbox"])

                        if "abstract" == text.strip().lower() and len(abstract_bbox) == 0:
                            abstract_bbox = span["bbox"]
                            abstract_size = round(span["size"])

                        if match_table_img_patter.match(text.strip().lower()):
                            update_add_dict_value(table_img_content_size_dict, size, 1)

    paper_content_size = get_max_dict_value(word_size_dict)[0]
    paper_content_left_bbox = get_max_dict_value(left_bbox_dict)[0] - 10
    paper_content_right_bbox = get_max_dict_value(right_bbox_dict)[0] + 10
    paper_content_top_bbox = get_max_dict_value(top_bbox_dict)[0] - 10
    paper_content_bottom_bbox = get_max_dict_value(bottom_bbox_dict)[0] + 10
    paper_content_begin_bbox, paper_content_end_bbox = get_content_begin_end_bbox(bbox_list)
    table_img_content_size = get_max_dict_value(table_img_content_size_dict)[0]
    if abstract_size > paper_content_size:
        title_size_big_than_paper_content_size = True

    page_text = []
    title_list = []  # 标题候选
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
            image_text_set = set([text.strip() for text in image_text_set])

        # 读取表格中的文本
        if len(table_info) > 0:
            tabel_bbox = [table_info[0].bbox[0], table_info[0].bbox[1],
                          table_info[0].bbox[2], table_info[0].bbox[3]]
            for tab in table_info:
                tabel_bbox = [min(tabel_bbox[0], tab.bbox[0]), min(tabel_bbox[1], tab.bbox[1]),
                              max(tabel_bbox[2], tab.bbox[2]), max(tabel_bbox[3], tab.bbox[3])]
            table_text_set = set(page.get_text(clip=tabel_bbox).split("\n"))
            table_text_set = set([text.strip() for text in table_text_set])

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
                            text = span["text"].strip()
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
                            # else:
                            #     span_text += " "
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
                        text = span["text"].strip()
                        font = span["font"].lower()
                        bbox = span["bbox"]

                        # 首页，隔离开标题信息和正文信息
                        if index == 0 and span["bbox"][1] < (abstract_bbox[1] - 5):
                            text = ""

                        # 如果文本长度为0，那么直接跳过
                        if len(text.strip().lower()) == 0:
                            continue

                        # 将表格和图片的说明信息的block存储起来，用于后续解析
                        if id(block) not in block_table_img_id_set \
                                and size == table_img_content_size \
                                and match_table_img_patter.match(text.strip().lower()):
                            block_table_img_list.append(block)
                            block_table_img_id_set.add(id(block))

                        # 判断是标题还是正文
                        if ((size > paper_content_size and title_size_big_than_paper_content_size is True) or (
                                size >= paper_content_size and title_size_big_than_paper_content_size is False)) \
                                and ("medi" in font or 'bold' in font):
                            span_text.append(f"{chr(1)}{size}{chr(1)}{text}{chr(1)}")
                        elif size == paper_content_size:
                            # 判断正文是否都在指定的坐标范围之内
                            paper_content_flag = 0
                            for paper_begin_bbox, paper_end_bbox in zip(paper_content_begin_bbox, paper_content_end_bbox):
                                if round(bbox[0]) >= paper_begin_bbox and round(bbox[2]) <= paper_end_bbox:
                                    paper_content_flag = 1
                                    # 判断是否是一段话的开头
                                    # 但是鉴于有时候line识别的不准，如果开头坐标右移动的太多了，那么就认为不是一段话的开头
                                    if paper_begin_bbox + \
                                            (axis_error + max_num_line_length/(7*len(paper_content_begin_bbox))) \
                                            > round(bbox[0]) > paper_begin_bbox + (axis_error + 2):
                                        text = chr(2) + text
                                    # 判断是否是一段话的结尾
                                    if round(bbox[2]) < paper_end_bbox - (axis_error + 2) and text[-1] == '.':
                                        text += chr(2)
                            if paper_content_flag == 1:
                                span_text.append(text)
                    span_text = " ".join(span_text).strip().replace(f"{chr(2)} ", " ")
                    if len(span_text) > 0 \
                            and not span_text.isdigit()\
                            and span_text not in image_text_set\
                            and span_text not in table_text_set:
                        if span_text[-1] == "-":
                            span_text = span_text[:-1]
                        line_text.append(span_text)
                if len(line_text) > 0:
                    line_text = "\n".join(line_text)
                    block_text.append(line_text)
        block_text = "\n".join(block_text)
        page_text.append(block_text)
    page_text = chr(3).join(page_text)

    # 抽取标题
    extract_title = ""
    title_top_bbox = 10000
    for bbox, title_info in title_list:
        if bbox[1] < title_top_bbox:
            title_top_bbox = bbox[1]
            extract_title = title_info
    extract_title = " ".join([t[1] for t in extract_title]).replace("  ", " ")

    # 这里在后期合并数据的时候再进行去除
    # # 去除引用标志，类似[ 34 , 35 , 49 ]
    # page_text = re.sub("\[[0-9, ]*\]", "", page_text)
    # # 正向预查询，去除类似( Ekman , 1993 ; Datcu and Rothkrantz , 2008 )
    # page_text = re.sub("\((?=.*\d{4})(?=.*[a-zA-Z]).*\)", "", page_text)
    # # 待完成，去除类似[Ouyang et al., 2022, Touvron et al., 2023, Bai et al., 2022a]
    # page_text = re.sub("\[(?=.*\d{4})(?=.*[a-zA-Z]).*\]", "", page_text)

    # 处理表格和图片的说明文本
    tabel_explain_text_list = []
    image_explain_text_list = []
    for block in block_table_img_list:
        if len(block) == 4 and block["type"] == 0:
            line_text = []
            for line in block["lines"]:
                span_text = []
                for span in line["spans"]:
                    size = round(span["size"])
                    text = span["text"].strip()
                    font = span["font"].lower()
                    bbox = span["bbox"]

                    # 首页，隔离开标题信息和正文信息
                    if index == 0 and span["bbox"][1] < (abstract_bbox[1] - 5):
                        text = ""

                    # 如果文本长度为0，那么直接跳过
                    if len(text.strip().lower()) == 0:
                        continue

                    # 将表格和图片的说明信息的block存储起来，用于后续解析
                    if id(block) not in block_table_img_id_set \
                            and size == table_img_content_size \
                            and match_table_img_patter.match(text.strip().lower()):
                        block_table_img_list.append(block)
                        block_table_img_id_set.add(id(block))

                    # 判断是标题还是正文
                    if ((size > paper_content_size and title_size_big_than_paper_content_size is True) or (
                            size >= paper_content_size and title_size_big_than_paper_content_size is False)) \
                            and ("medi" in font or 'bold' in font):
                        span_text.append(f"{chr(1)}{size}{chr(1)}{text}{chr(1)}")
                    elif size == paper_content_size:
                        # 判断正文是否都在指定的坐标范围之内
                        paper_content_flag = 0
                        for paper_begin_bbox, paper_end_bbox in zip(paper_content_begin_bbox, paper_content_end_bbox):
                            if round(bbox[0]) >= paper_begin_bbox and round(bbox[2]) <= paper_end_bbox:
                                paper_content_flag = 1
                                # 判断是否是一段话的开头
                                # 但是鉴于有时候line识别的不准，如果开头坐标右移动的太多了，那么就认为不是一段话的开头
                                if paper_begin_bbox + \
                                        (axis_error + max_num_line_length / (7 * len(paper_content_begin_bbox))) \
                                        > round(bbox[0]) > paper_begin_bbox + (axis_error + 2):
                                    text = chr(2) + text
                                # 判断是否是一段话的结尾
                                if round(bbox[2]) < paper_end_bbox - (axis_error + 2) and text[-1] == '.':
                                    text += chr(2)
                        if paper_content_flag == 1:
                            span_text.append(text)
                span_text = " ".join(span_text).strip().replace(f"{chr(2)} ", " ")
                if len(span_text) > 0 \
                        and not span_text.isdigit() \
                        and span_text not in image_text_set \
                        and span_text not in table_text_set:
                    if span_text[-1] == "-":
                        span_text = span_text[:-1]
                    line_text.append(span_text)
            if len(line_text) > 0:
                line_text = "\n".join(line_text)
                block_text.append(line_text)


    with open(save_path, "w", encoding="utf-8") as f_write:
        f_write.write(extract_title)
        f_write.write("\n\n\n\n\n")
        f_write.write(page_text)

