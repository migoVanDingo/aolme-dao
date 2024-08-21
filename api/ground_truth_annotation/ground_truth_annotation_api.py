from flask import Blueprint, request, jsonify, make_response, current_app

from api.ground_truth_annotation.handler.RequestAddGroundTruthAnnotation import RequestAddGroundTruthAnnotation

ground_truth_api = Blueprint('ground_truth_annotation_api', __name__)

@ground_truth_api.route('/ground-truth', methods=['POST'])
def add_ground_truth():
    current_app.logger.debug(f"API: ground_truth_annotation_api :: Request: {request}")

    api_request = RequestAddGroundTruthAnnotation(request.data)
    response = api_request.do_process()

    if response.data == "error":
        return jsonify("An error occurred"), 500
    else:
        return response, 200