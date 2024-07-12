from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_mysqldb import MySQL
import logging, json
from api.group_api import group_api


logging.basicConfig(filename='record.log',
                level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'aolme_prod'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'aolme_prod'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 
    app.register_blueprint(group_api, url_prefix='/api/group')

    return app

def init_db(app):
    db = MySQL()
    db.init_app(app)
    return db


app = create_app()
db = init_db(app)

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('success', 200)
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = '*'
        return response