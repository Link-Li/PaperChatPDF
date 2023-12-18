# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/17 19:52
@Author      : noahzhenli
@Email       : 
@Description : 
"""

from langchain.document_loaders import ArxivLoader

docs = ArxivLoader(query="2312.09251", load_max_docs=2).load()
print(len(docs))


print(docs[0].metadata)

print(docs[0].page_content[:400])