from flask import current_app, jsonify

from dao.table_ground_truth import TableGroundTruth


class RequestAddGroundTruthAnnotation():
    def __init__(self, data):
        self.data = data

    def do_process(self):
        try:
            #Log payload data
            current_app.logger.debug(f"{self.__class__.__name__} :: data: {self.data}")
            table_ground_truth = TableGroundTruth()
            response = table_ground_truth.add(self.data)

            current_app.logger.debug(f"{self.__class__.__name__} :: response: {response}")

            return jsonify(response)
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: {e}")
            return jsonify("error")