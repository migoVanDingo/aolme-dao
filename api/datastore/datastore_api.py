import json, random, string
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_cors import CORS

from api.datastore.handler.request_add_subset import RequestAddSubset
from api.datastore.handler.request_create_dataset import RequestCreateDataset
from api.datastore.handler.request_create_subset import RequestCreateSubset
from dao.table_datastore import TableDatastore

datastore_api = Blueprint('datastore_api', __name__)

@datastore_api.route('/create-dataset', methods=['POST', 'OPTIONS'])
def create_dataset():
    data = json.loads(request.data)
    dataset_type = request.args.get('dataset_type')

    api_request = RequestCreateDataset(data, dataset_type)
    response = api_request.do_process()

    if response.data == "error":
        return make_response(response, 500)
    else:
        return make_response(response, 200)
    
@datastore_api.route('/subset', methods=['POST', 'OPTIONS'])
def add_subset():
    data = json.loads(request.data)

    api_request = RequestAddSubset(data)
    response = api_request.do_process()
    return make_response(response, 200)



@datastore_api.route('/get/<id>', methods=['GET'])
def get_item(id):
    pass


@datastore_api.route('/', methods=['POST', 'OPTIONS'])
def create_datastore():
    db = TableDatastore()
    data = json.loads(request.data)
    datastore = db.insert(data)
    return make_response(jsonify(datastore), 200)


