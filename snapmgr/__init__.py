# -*- coding: utf-8 -*-

import flask
import flask_restful
import flask_sqlalchemy
from flask_apscheduler import APScheduler


from snapmgr.config import DevelopmentConfig


_api_blueprint = flask.Blueprint('api', __name__)
flask_api = flask_restful.Api(_api_blueprint)

app = flask.Flask('snapmgr')
scheduler = APScheduler()
app.register_blueprint(_api_blueprint, url_prefix='/snapmgr_api')
app.config.from_object(DevelopmentConfig)

db = flask_sqlalchemy.SQLAlchemy(app)


def initdb():
    db.create_all()


from snapmgr.urls import *
