import random
import string

from flask import current_app
from dao.abstract_dao import AbstractDao


class TableTrims(AbstractDao):
    def __init__(self):
        from app import db
        self.db = db

    def generate_id(self):
        N = 22
        id = 'TRM' + \
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        return id

    def get_list(self, params):
        pass

    def get_by_id(self, id):
        pass

    def add(self, payload):
        try:
            trim_id = self.generate_id()
            payload['trim_id'] = trim_id
            payload['is_active'] = 1
            query = "INSERT INTO `trims` (trim_id, ground_truth_id, video_id, filename, path, type, start_time, end_time, is_active, created_at, created_by) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, 1, NOW(), %s)"

            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['trim_id'], payload['ground_truth_id'], payload['video_id'], payload['filename'], payload['path'], payload['type'], payload['start_time'], payload['end_time'], payload['created_by']))
            self.db.connection.commit()
            cursor.close()

            return payload

        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"ERROR"

    def update(self, payload):
        pass

    def delete(self, id):
        pass

    def get_list_by_video_id(self, video_id):
        pass

    def get_list_by_ground_truth_id(self, ground_truth_id):
        pass

