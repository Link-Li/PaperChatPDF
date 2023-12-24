# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/20 17:08
@Author      : noahzhenli
@Email       : 
@Description : 
"""


import sys, pathlib, fitz


file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/2312.09251.pdf"
# file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/Multimodal-Intelligence.pdf"
with fitz.open(file_path) as doc:  # open document
    # all_text = [page.get_text("blocks", sort=True) for page in doc]
    #
    # tables = [page.find_tables() for page in doc]
    #
    # tab_text = [tab.extract() for tab in doc[6].find_tables().tables]
    #
    text = doc[0].get_text(clip=[124.68500518798828, 103.16062927246094, 470.5433349609375, 139.75802612304688], sort=True)

    for page in doc:
        table = page.find_tables()
        image = page.get_image_info()
        a = 1
    # text = doc[0].get_fonts()


# write as a binary file to support non-ASCII characters
# pathlib.Path(file_path + ".txt").write_bytes(text.encode())

a = 1