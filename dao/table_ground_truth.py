import random
import string

from flask import current_app
from dao.abstract_dao import AbstractDao


class TableGroundTruth(AbstractDao):
    def __init__(self):
        from app import db
        self.db = db

    def generate_id(self):
        N = 22
        ground_truth_id = 'GTR' + \
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        return ground_truth_id

    def get_list(self, params):
        pass

    def get_by_id(self, id, type):
        pass

    def get_by_video_and_type(self, video_id, type):
        try:
            query = "SELECT filename, path, ground_truth_id, type  FROM ground_truth WHERE video_id = %s AND type = %s"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (video_id, type))
            ground_truth = cursor.fetchone()
            cursor.close()
            return ground_truth
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}" 
    
    


    def add(self, payload):
        try:
            ground_truth_id = self.generate_id()
            payload['ground_truth_id'] = ground_truth_id
            payload['is_active'] = 1
            query = "INSERT INTO `ground_truth` (ground_truth_id, video_id, filename, path, type, file_type, is_active, created_at, created_by) VALUES (%s, %s, %s, %s, %s, %s, 1, NOW(), %s)"

            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['ground_truth_id'], payload['video_id'], payload['filename'], payload['path'], payload['type'], payload['file_type'], payload['created_by']))
            self.db.connection.commit()
            cursor.close()

            return payload
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR"
        
    

    def update(self, payload):
        pass

    def delete(self, id):
        pass
