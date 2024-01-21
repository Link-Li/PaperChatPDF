# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/18 17:37
@Author      : noahzhenli
@Email       : 
@Description : 
"""

import os
print (os.getcwd())

from create_flask_app import db


class PdfInfo(db.Model):
    __tablename__ = 'pdf_info'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, info={'comment': 'id'})
    title = db.Column(db.String(255), nullable=False, info={'comment': 'paper的标题'})
    abstract = db.Column(db.Text, nullable=False, info={'comment': 'paper的摘要'})
    abstract_chinese = db.Column(db.Text, nullable=True, info={'comment': 'paper的摘要的中文翻译结果'})
    title_llm_generates = db.Column(db.Text, nullable=True, info={'comment': '根据paper的标题提取的关键词的大模型生成结果'})
    title_core_keywords = db.Column(db.Text, nullable=True, info={'comment': '根据paper的标题提取的关键词'})
    abstract_llm_generates = db.Column(db.Text, nullable=True, info={'comment': '根据paper的摘要提取的关键词的大模型生成结果'})
    abstract_core_keywords = db.Column(db.Text, nullable=True, info={'comment': '根据paper的摘要提取关键词'})
    pdf_save_path = db.Column(db.String(2048), nullable=False, info={'comment': 'paper的pdf的保存位置'})
    json_save_path = db.Column(db.String(2048), nullable=False, info={'comment': 'paper的json解析结果的保存位置'})

    def __repr__(self):
        return '<title %r>' % self.title