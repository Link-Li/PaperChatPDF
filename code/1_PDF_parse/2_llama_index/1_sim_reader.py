# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/17 20:29
@Author      : noahzhenli
@Email       : 
@Description : 
"""


from llama_index import SimpleDirectoryReader

# documents = SimpleDirectoryReader("/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/").load_data()



from llama_index import download_loader

PDFReader = download_loader("PDFReader")

loader = PDFReader()
documents = loader.load_data(file="/data_cbs/zhenli/code/PaperChatPDF/dataset/pdf_data/2312.09251.pdf")

a = 1