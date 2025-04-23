from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Veritabanı konfigürasyonu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarifler.db'
app.config['SQLALCHEMY_BINDS'] = {
    'turk_tarifleri': 'sqlite:///turk_tarifleri.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)