# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/20 17:08
@Author      : noahzhenli
@Email       : 
@Description : 
"""


import sys, pathlib, fitz


file_path = "/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/2312.09251.pdf"
with fitz.open(file_path) as doc:  # open document
    text = [page.get_text("blocks", sort=True) for page in doc]

    tables = [page.find_tables() for page in doc]

    tab_text = [tab.extract() for tab in doc[6].find_tables().tables]

    text = doc[1].get_text(clip=(355.41043853759766, 165.8285705566406, 370.2895050048828, 299.0965881347656), sort=True)

# write as a binary file to support non-ASCII characters
# pathlib.Path(file_path + ".txt").write_bytes(text.encode())

a  = 1