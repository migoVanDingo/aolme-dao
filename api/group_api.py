from flask import Blueprint, request, jsonify, make_response, current_app
from flask_cors import CORS
 

group_api = Blueprint('group_api', __name__)

@group_api.route('/', methods=['GET'])
def get_group():
    from app import db
    query = "SELECT * FROM `groups`"
    cursor = db.connection.cursor()
    cursor.execute(query)
    groups = cursor.fetchall()
    cursor.close()
    current_app.logger.debug(f" Response: {jsonify(groups)}")
    return jsonify(groups)

@group_api.route('/categories', methods=['GET'])
def get_categories():
    from app import db

    result = {}
    queries = [
        {"category": "date", "q":"SELECT DISTINCT date FROM `groups`"},
        {"category": "facilitator", "q":"SELECT DISTINCT facilitator FROM `groups`"},
        {"category": "school", "q":"SELECT DISTINCT school FROM `groups`"},
        {"category": "cohort", "q":"SELECT DISTINCT cohort FROM `groups`"},
        {"category": "level", "q":"SELECT DISTINCT level FROM `groups`"},
    ]

    for query in queries:
        cursor = db.connection.cursor()
        cursor.execute(query['q'])
        c = cursor.fetchall()
        result[query['category']] = c
        cursor.close()
    current_app.logger.debug(f" Response: {jsonify(result)}")
    return jsonify(result)
