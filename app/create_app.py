from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from elasticsearch import Elasticsearch

from dotenv import load_dotenv
import os

load_dotenv()

# Crea la instancia de Flask
app = Flask(__name__)

# Configura la conexión a la base de datos -> system.b1yuy0s3rv3r2020.net
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}?charset=utf8'
app.config['FLASK_DEBUG'] = True
CORS(app)
db = SQLAlchemy(app)
es = Elasticsearch(['http://elasticsearch_utils:9200'])

#TODO: Telegram tokens
tokenTestTelegram = os.getenv("TOKEN_TELEGRAM_TEST")

#TODO: Url para apuntar al server depende de su hubicacion
UrlServer = os.getenv("SERVER_URL")