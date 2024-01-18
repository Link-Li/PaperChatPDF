# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/17 20:46
@Author      : noahzhenli
@Email       : 
@Description : 
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


config_dict = {}
with open("env.txt", "r", encoding="utf-8") as f_read:
    for data_line in f_read.readlines():
        data_split = data_line.strip("\n").split("=")
        config_dict[data_split[0]] = data_split[1]
mysql_url = config_dict["mysql_url"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserV2(db.Model):
    __tablename__ = 'userv2'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()

    new_user = UserV2(username='xxx', email='john@example.com')
    db.session.add(new_user)
    new_user = UserV2(username='yyy', email='Tom@example.com')
    db.session.add(new_user)
    db.session.commit()

    # 获取所有用户
    users = UserV2.query.all()
    print(users)

    # 根据用户名查询单个用户
    user = UserV2.query.filter_by(username='john_doe').first()
    print(user)