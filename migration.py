# coding: utf-8
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from os import path

#config
script_dir = path.dirname(__file__)
DATABASE = path.join(script_dir, 'url_hash.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('CONFIG_FLASKR', silent=True)


def conect_db():
    return sqlite3.connect(app.config['DATABASE'])


def create_bd():
    with closing(conect_db()) as db:
        with app.open_resource('esquema.sql') as sql:
            db.cursor().executescript(sql.read())
        db.commit()


if __name__ == '__main__':
    app.run()
