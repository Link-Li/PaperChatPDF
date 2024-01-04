# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/3 21:19
@Author      : noahzhenli
@Email       : 
@Description : 将上一步获取的PDF数据进行拼装成格式化的
{
"title": xxx
"section1": {"section2": xxx}
"section1": xxx
}

require：
python >= 3.7
"""

import os


def set_paper_content_section_list_last_key(section_list, old_key, new_key):
    pass

# 获取章节列表的最后一个章节的名称
def get_paper_content_section_list_last_key(section_list):
    pass




if __name__ == '__main__':
    root_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
    file_path = root_path + "/dataset/output_data/ICON.txt"
    save_path = file_path + ".json"
    paper_format_dict = {}

    with open(file_path, "r", encoding="utf-8") as f_read:
        file_content = "".join(f_read.readlines())
        data_split = file_content.strip("").split(chr(5))
        title = data_split[0]
        paper_content = data_split[1]
        image_explain_text = data_split[2]
        tabel_explain_text_list = data_split[3]

        # 用来存储paper正文的内容，
        # [标题：[正文, [标题：正文]]]
        # 最多两级标题，即主标题+小标题
        paper_content_section_list = []
        paper_content = paper_content.replace(chr(3), "\n")
        # 分段落
        paper_content_paragraph = paper_content.replace(f"{chr(2)}{chr(2)}", chr(2)).split(chr(2))

        # 如果paper_content不是abstract开头的，那么加一个默认的标题作为起始标题，名字叫default_section_1
        for index, paragraph in enumerate(paper_content_paragraph):
            if index == 0 and "abstract" not in paragraph.lower():
                if not paragraph.startswith(chr(1)) and len(paper_content_section_list) == 0:
                    paper_content_section_list.append(["default_section_1"])

            if paragraph.startswith(chr(1)):
                section_list = paragraph.strip(chr(1)).split(chr(1))
                section_key = list(paper_content_section_dict.keys())
                if len(section_key) > 0:







        paper_format_dict["title"] = title


        a = 1
