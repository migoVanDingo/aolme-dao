import json

from flask import Blueprint, jsonify, request

from api.processing.handler.request_create_trim_videos_ground_truth import RequestCreateTrimVideosGroundTruth
from api.processing.handler.request_create_trim_videos_region import RequestCreateTrimVideosRegion

processing_api = Blueprint('processing_api', __name__)

@processing_api.route('/trim/ground-truth', methods=['POST'])
def create_trim_videos_ground_truth():
    data = json.loads(request.data)

    api_request = RequestCreateTrimVideosGroundTruth(data)
    response = api_request.do_process()

    if response.data == "error":
        return jsonify("processing_api :: create_trim_videos() :: An error occurred"), 500
    else:
        return jsonify(response), 200



@processing_api.route('/trim/region', methods=['POST'])
def create_trim_videos_region():
    data = json.loads(request.data)

    api_request = RequestCreateTrimVideosRegion(data)
    response = api_request.do_process()

    if response.data == "error":
        return jsonify("processing_api :: create_trim_videos() :: An error occurred"), 500
    else:
        return jsonify(response), 200
