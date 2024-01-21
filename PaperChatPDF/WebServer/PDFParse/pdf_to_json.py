# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/7 17:54
@Author      : noahzhenli
@Email       :

@Description :
用于解析PDF信息，并保存成json格式，主要函数如下
```
parse_pdf_to_txt(file_path, save_path)
parse_pdf_text_to_json(file_path, save_path)
```
"""



import os
import re
import json
import sys, pathlib, fitz

# 防止误检测的泛化位置偏差
axis_error = 2
# 文档的大小
width, height = 0, 0
# 正文一行的长度
max_num_line_length = 0


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


def parse_pdf_to_txt(file_path, save_path):
    """
    将PDF的内容解析出来，主要是将PDF中的标题，小标题以及对应的正文内容、图片和表格的说明文本，并将解析结果保存到txt。

    保存格式：chr(5).join([论文标题, PDF主要内容, 图片说明文本, 表格说明文本])

    PDF主要内容格式：小标题用`{chr(6)}{chr(1)}{size}{chr(1)}{text}{chr(1)}{chr(6)}`格式保存，保存内容的字体大小和标题内容。
                  具体的内容，其中的段落位置用chr(2)分割，然后不同页的PDF用chr(3)分割

    图片和表格说明文本：根据`match_table_img_patter`的正则规则，识别是否是图片或者表格的说明文本，识别出来之后，每个用chr(4)分割。

    Args:
        file_path (str): 需要解析的PDF的路径
        save_path (str): 保存解析好的PDF的数据的路径

    Returns:

    """
    global width, height, axis_error, max_num_line_length
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
                                span_text.append(f"{chr(6)}{chr(1)}{size}{chr(1)}{text}{chr(1)}{chr(6)}")
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
                            # if span_text[-1] == "-":
                            #     span_text = span_text[:-1]
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

        # 处理表格和图片的说明文本
        tabel_explain_text_list = []
        image_explain_text_list = []
        for block in block_table_img_list:
            # no表示还没遇到figure或者table开头的文本
            # figure 或者 table 表示遇到了figure或者table卡头的文本，那么之后的文本都默认是图片或者表格的说明内容
            match_table_img_patter_flag = "no"
            if len(block) == 4 and block["type"] == 0:
                line_text = []
                for line in block["lines"]:
                    span_text = []
                    for span in line["spans"]:
                        size = round(span["size"])
                        text = span["text"].strip()
                        font = span["font"].lower()
                        bbox = span["bbox"]

                        # 如果文本长度为0，那么直接跳过
                        if len(text.strip().lower()) == 0:
                            continue

                        # 判断是不是figure或者table开头，否则跳过
                        # 遇到过一次figure或者table开头之后，之后的文本就不在跳过
                        if (not match_table_img_patter.match(text.strip().lower()))  \
                                and match_table_img_patter_flag == 'no':
                            continue
                        elif match_table_img_patter_flag == 'no':
                            if "figure" in text.strip().lower():
                                match_table_img_patter_flag = "figure"
                            elif "table" in text.strip().lower():
                                match_table_img_patter_flag = "table"

                        span_text.append(text)
                    span_text = " ".join(span_text).strip().replace(f"{chr(2)} ", " ")
                    if len(span_text) > 0 \
                            and not span_text.isdigit():
                        if span_text[-1] == "-":
                            span_text = span_text[:-1]
                        line_text.append(span_text)
                if len(line_text) > 0:
                    line_text = "\n".join(line_text)
                    if match_table_img_patter_flag == "figure":
                        image_explain_text_list.append(line_text)
                    elif match_table_img_patter_flag == "table":
                        tabel_explain_text_list.append(line_text)

        with open(save_path, "w", encoding="utf-8") as f_write:
            f_write.write(extract_title)
            f_write.write(chr(5))
            f_write.write(page_text)
            f_write.write(chr(5))
            f_write.write(chr(4).join(image_explain_text_list))
            f_write.write(chr(5))
            f_write.write(chr(4).join(tabel_explain_text_list))


def filter_cite(content):
    # 这里在后期合并数据的时候再进行去除
    # # 去除引用标志，类似[ 34 , 35 , 49 ]
    content = re.sub("\[[0-9, ]*\]", "", content)
    # # 正向预查询，去除类似( Ekman , 1993 ; Datcu and Rothkrantz , 2008 )
    content = re.sub("\((?=.*\d{4})(?=.*[a-zA-Z]).*\)", "", content)
    # # 去除类似[Ouyang et al., 2022, Touvron et al., 2023, Bai et al., 2022a]
    content = re.sub("\[(?=.*\d{4})(?=.*[a-zA-Z]).*\]", "", content)
    return content


def combine_line_to_paragraph(paper_content_section):
    paragraph_list = []
    paragraph = []
    for line in paper_content_section[-1]:
        if isinstance(line, str):
            if len(paragraph) == 0:
                if len(line) > 0:
                    paragraph = [line]
                else:
                    continue
            elif paragraph[-1][-1] != ".":
                if len(line) > 0:
                    if paragraph[-1][-1] == '-':
                        paragraph[-1] = paragraph[-1][:-1] + chr(1)
                    paragraph.append(line)
                else:
                    continue
            elif paragraph[-1][-1] == ".":
                if len(line) > 0:
                    paragraph.append(line)
                # 形成新的段落，进行合并
                elif len(line) == 0:
                    filter_pargraph = filter_cite(" ".join(paragraph).replace(f"{chr(1)} ", ""))
                    paragraph_list.append(filter_pargraph)
                    paragraph = ""
                    continue
    return paragraph_list


def get_title_font_size(paper_content):
    paper_content_list = paper_content.split(chr(6))
    title_list = []
    for content in paper_content_list:
        title_list.extend(re.findall("\x01[\S\s]+\x01[\S\s]+\x01", content))
    # title_list = re.findall("\x06\x01[\S\s]+\x01[\S\s]+\x01\x06", paper_content)
    font_size_dict = {}
    for title_info in title_list:
        font_size, title = title_info.strip(chr(1)).split(chr(1))
        update_add_dict_value(font_size_dict, font_size, 1)
    font_size_list = sorted(font_size_dict.items(), key=lambda k: (k[0], k[1]), reverse=True)
    for font_size in font_size_list:
        if font_size[1] > 3:
            return int(font_size[0])

    # 如果没有标题，返回一个0值
    return 0


def insert_paper_content_section_list_content(section_list, content):
    last_section_1 = section_list[-1]
    last_section_2 = last_section_1[-1]
    # 如果最后一个内容结构是[section, font_size, content]
    if len(last_section_2) > 0 and isinstance(last_section_2[-1], list):
        section_list[-1][-1][-1][-1].append(content)
    # 如果最后一个内容的结构
    else:
        section_list[-1][-1].append(content)


def set_paper_content_section_list_last_key(section_list, old_key, new_key, font_size):
    if len(section_list) > 0:
        last_section_1 = section_list[-1]
        font_size_1 = last_section_1[1]
        last_section_2 = last_section_1[-1]
        if len(last_section_2) > 0 and isinstance(last_section_2[-1], list):
            font_size_2 = last_section_2[-1][1]
        else:
            font_size_2 = 0
    else:
        last_section_1 = []
        font_size_1 = font_size
        last_section_2 = []
    # 如果有old key，那么说明是将老的标题替换成新的标题
    if old_key:
        # 插入二级标题
        if len(last_section_2) > 0 and isinstance(last_section_2[-1], list) and last_section_2[0] == old_key:
            last_section_2[-1][0] = new_key
            section_list[-1][-1][-1] = last_section_2
        # 插入一级标题
        elif len(last_section_1) > 0 and last_section_1[0] == old_key:
            last_section_1[0] = new_key
            section_list[-1] = last_section_1
        # 抛出异常
        else:
            raise Exception("更新section，和尾部的section无法对应")
    # 没有老的标题，那么就考虑将新的标题插入到section_list中，这里需要考虑是作为一级标题插入，还是作为二级标题插入
    else:
        new_section = [new_key, font_size, []]
        # 作为一级标题插入
        if font_size == font_size_1:
            section_list.append(new_section)
        # 作为二级标题插入
        else:
            section_list[-1][-1].append(new_section)


# 获取章节列表的最后一个章节的名称
def get_paper_content_section_list_last_section(section_list):
    # 防止第一次是abstract的时候，section_list为空
    if len(section_list) > 0:
        last_section_1 = section_list[-1]
        last_section_2 = last_section_1[-1]
        # 可以进行合并的标题，必须满足样式是[section, font_size, []]，并且最后的内容是空的
        # 因为PDF识别的时候，有时候会把一个标题识别成多行
        if len(last_section_2) > 0 and isinstance(last_section_2[-1], list) and len(last_section_2[-1][-1]) == 0:
            return last_section_2[-1]
        elif len(last_section_1) > 0 and isinstance(last_section_1[-1], list) and len(last_section_1[-1]) == 0:
            return last_section_1
        else:
            return None
    return None


def parse_pdf_text_to_json(file_path, save_path):
    """
    将parse_pdf_to_txt解析得到的PDF信息，进行合并得到json数据。

    存储结构如下：
    ```
    {
        "title": "",
        "content": "",
        [
            [section_1, size_1,
                [content, content,
                    [section_2, size_2, [content, content, ...]],
                    [section_2, size_2, [content, content, ...]]
                ]
            ],
            [section_1, size_1,
                [content, content,
                    [section_2, size_2, [content, content, ...]],
                    [section_2, size_2, [content, content, ...]]
                ]
            ],
        ]
    }
    ```


    Args:
        file_path:
        save_path:

    Returns:
        paper_format_dict (dict): 解析之后的PDF的数据

    """
    paper_format_dict = {}

    with open(file_path, "r", encoding="utf-8") as f_read:
        file_content = "".join(f_read.readlines())
        data_split = file_content.strip("").split(chr(5))
        title = data_split[0]
        paper_content = data_split[1]
        image_explain_text = data_split[2]
        tabel_explain_text = data_split[3]

        # 用来存储paper正文的内容，
        # [标题：[正文, [标题：正文]]]
        # 最多两级标题，即主标题+小标题
        paper_content_section_list = []
        paper_content = paper_content.replace(chr(3), "\n")
        # 分段落, 多加一个\n，用于后续分段落用
        paper_content_paragraph = paper_content.replace(f"{chr(2)}{chr(2)}", f"{chr(2)}")\
            .replace(f"{chr(2)}", f"{chr(2)}\n{chr(2)}").split(chr(2))

        # 抽一下标题的文字大小，选择最大的，且数量大于3的作为一级标题大小，大于这个字体大小的，默认改成这个字体大小，小于这个字体大小的，默认作为小标题
        paper_section_font_size = get_title_font_size(paper_content)

        # 如果paper_content不是abstract开头的，那么加一个默认的标题作为起始标题，名字叫default_section_1
        for index, paragraph in enumerate(paper_content_paragraph):
            paragraph = paragraph.strip()
            for line_index, line in enumerate(paragraph.split("\n")):
                if index == 0 and "abstract" not in line.lower():
                    if not line.startswith(f"{chr(6)}{chr(1)}") and len(paper_content_section_list) == 0:
                        paper_content_section_list.append(["default_section_1", paper_section_font_size, []])

                # 如果发现这一行是标题，需要把标题合并到之前的标题里面，或者创建一个新的标题
                if line.startswith(f"{chr(6)}{chr(1)}"):
                    new_section_info = line.strip(f"{chr(6)}{chr(1)}").split(chr(1))
                    new_font_size = int(new_section_info[0])
                    new_section = new_section_info[1].strip()

                    last_section_info = get_paper_content_section_list_last_section(paper_content_section_list)
                    # 如果最后一个标题信息符合将下一个标题合并进去，那么就考虑将新的标题合并到老的标题里面
                    if last_section_info:
                        old_section = last_section_info[0]
                        old_font_size = last_section_info[1]
                        old_content_list = last_section_info[2]

                        # 因为新标题的字体大小与老标题不一致，那说明新的标题不能合并
                        if (new_font_size != old_font_size) or ("abstract" in old_section.lower()):
                            set_paper_content_section_list_last_key(paper_content_section_list, None, new_section,
                                                                    new_font_size)
                        # 将新的标题作为一个新的list插入到paper_content_section_list中
                        else:
                            new_section = f"{old_section} {new_section}"
                            set_paper_content_section_list_last_key(paper_content_section_list, old_section, new_section, new_font_size)
                    # 不符合插入新的标题的要求，那么就创建一个新的标题list放进去
                    else:
                        set_paper_content_section_list_last_key(paper_content_section_list, None, new_section, new_font_size)
                # 如果不是标题，那么就是正文内容，那么将正文内容插入到[section, font_size, []]中的最后一个内容位置
                else:
                    line = line.strip()
                    insert_paper_content_section_list_content(paper_content_section_list, line)

        # 将行拼接成段落
        # 如果上一行不是句号结尾，那么就把下一行和上一行进行拼接，用空格分割；如果上一行结尾是-，那么就不用空格拼接，去掉-，直接拼接
        # 如果上一行是句号，那么就要看下一行是不是空字符串，如果是，那么可以作为段落的分隔符
        # 如果上一行不是句号，但是下一行是空字符串，那么直接跳过空字符串，继续找下一行的非空字符串
        combine_paper_content_section_list = []
        for paper_content_section in paper_content_section_list:
            new_content_list = []
            first_str_flag = "line"
            for line in paper_content_section[-1]:
                if isinstance(line, str) and first_str_flag == "line":
                    first_str_flag = "line_ing"
                    new_content_list.extend(combine_line_to_paragraph(paper_content_section))
                elif isinstance(line, list):
                    first_str_flag = "list"
                    new_content_list.append([line[0], line[1],
                                             combine_line_to_paragraph(line)])
                else:
                    if first_str_flag == "list":
                        raise Exception("合并line到paragraph的时候出现错误")
            paper_content_section[-1] = new_content_list
            combine_paper_content_section_list.append(paper_content_section)

        # 处理一下图片或者表格的说明文本
        image_explain_list = []
        for image_explain_info in image_explain_text.split(chr(4)):
            image_explain = []
            for info in image_explain_info.split("\n"):
                if len(info) > 0 and info[-1] == '-':
                    info = info[:-1] + f"{chr(1)} "
                image_explain.append(info)
            image_explain_list.append(" ".join(image_explain).replace(f"{chr(1)} ", ""))

        table_explain_list = []
        for table_explain_info in tabel_explain_text.split(chr(4)):
            table_explain = []
            for info in table_explain_info.split("\n"):
                if len(info) > 0 and info[-1] == '-':
                    info = info[:-1] + f"{chr(1)} "
                table_explain.append(info)
            table_explain_list.append(" ".join(table_explain).replace(f"{chr(1)} ", ""))

        paper_format_dict["title"] = title
        paper_format_dict["content"] = paper_content_section_list
        paper_format_dict["image_explain"] = image_explain_list
        paper_format_dict["table_explain"] = table_explain_list
        paper_format_json = json.dumps(paper_format_dict, ensure_ascii=False)
        with open(save_path, "w", encoding="utf-8") as f_write:
            f_write.write(paper_format_json)
    return paper_format_dict

