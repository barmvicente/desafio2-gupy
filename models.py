from flask import Flask
from datetime import datetime

app = Flask(__name__)
script_dir = path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  path.join(script_dir, 'url_hash.db')
db = SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    url_hash = db.Column(db.String(20), unique=True)
    count = db.Column(db.Integer)

    def __init__(self, url, url_hash):
        self.url = url
        self.url_hash = url_hash

    def __repr__(self):
        return '<Urls %r %r>' % (self.url, self.url_hash)