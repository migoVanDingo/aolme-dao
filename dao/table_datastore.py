import random
import string

from flask import current_app


class TableDatastore:
    def __init__(self):
        from app import db
        self.db = db

    def generate_id(self):
        N = 22
        id = 'DS' + ''.join(random.choices(string.digits, k= N - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=N - 2))
        return id
    
    def insert(self, payload):
        try:
            datastore_id = self.generate_id()
            payload['datastore_id'] = datastore_id
            payload['is_active'] = 1
            query = "INSERT INTO `datastore` (datastore_id, name, path, entity_id, is_public, is_active, created_at, created_by) VALUES (%s, %s, %s, %s, 1, 1, NOW(), %s)"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['datastore_id'], payload['name'], payload['path'], payload['entity_id'], payload['owner']))
            self.db.connection.commit()
            cursor.close()
            return payload
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    def get_item(self, datastore_id):
        try:
            query = "SELECT * FROM datastore WHERE datastore_id = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (datastore_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"