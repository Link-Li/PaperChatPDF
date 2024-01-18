# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/18 17:33
@Author      : noahzhenli
@Email       : 
@Description : 
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from web_server_config import TestingConfig

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig())
    db.init_app(app)
    return app