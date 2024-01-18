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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    abstract_chinese = db.Column(db.Text, nullable=True)
    paper_summary = db.Column(db.Text, nullable=True)
    pdf_save_path = db.Column(db.String(2048), nullable=False)
    json_save_path = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return '<title %r>' % self.title