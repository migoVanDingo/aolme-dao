import json, random, string
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_cors import CORS

from api.datastore.handler.request_create_dataset import RequestCreateDataset

datastore_api = Blueprint('datastore_api', __name__)

@datastore_api.route('/create-dataset', methods=['POST', 'OPTIONS'])
def create_dataset():
    data = json.loads(request.data)
    dataset_type = request.args.get('dataset_type')

    api_request = RequestCreateDataset(data, dataset_type)
    response = api_request.do_process()

    if response.data == "error":
        return make_response(jsonify({"error": "An error occurred"}), 500)
    else:
        return make_response(response, 200)



@datastore_api.route('/get/<id>', methods=['GET'])
def get_item(id):
    pass


