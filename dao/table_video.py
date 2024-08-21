from dao.abstract_dao import AbstractDao
from flask import current_app


class TableVideo(AbstractDao):
    def __init__(self):
        from app import db
        self.db = db

    def get_list(self, params):
        params_list = params.items()
        query = "SELECT * FROM `groups` WHERE "
        query_conditions = []
        query_params = []

        for index, (key, value) in enumerate(params_list):
            if isinstance(value, int):
                query_conditions.append(f"{key} = %s")
            else:
                query_conditions.append(f"{key} = %s")
            query_params.append(value)

        query += " AND ".join(query_conditions)

        cursor = self.db.connection.cursor()
        cursor.execute(query, query_params)
        videos = cursor.fetchall()
        cursor.close()
        return videos

    def get_by_id(self, id):
        pass

    def add(self, payload):
        pass

    def update(self, payload):
        pass

    def delete(self, id):
        pass
