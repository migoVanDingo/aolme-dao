import random
import string

from flask import current_app, jsonify


class TableDatastoreDirectory:
    def __init__(self):
        from app import db
        self.db = db

    def generate_id(self):
        N = 22
        id = 'DSD' + ''.join(random.choices(string.digits, k= N - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=N - 2))
        return id
    
    def insert(self, payload):
        try:
            directory_id = self.generate_id()
            payload['ds_directory_id'] = directory_id
            payload['is_active'] = 1
            query = "INSERT INTO `datastore_subset_directory` (directory_id, ds_subset_id, type, path, is_active, created_at, created_by) VALUES (%s, %s, %s, %s, 1, NOW(), %s)"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['ds_directory_id'], payload['ds_subset_id'], payload['type'], payload['path'], payload['owner']))
            self.db.connection.commit()
            cursor.close()
            return payload
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    def get_item(self, directory_id):
        try:
            query = "SELECT * FROM datastore_subset_directory WHERE directory_id = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (directory_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    def get_list_by_subset_id(self, subset_id):
        try:
            query = "SELECT directory_id, ds_subset_id, type, path FROM datastore_subset_directory WHERE ds_subset_id = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (subset_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    def update(self, payload):
        try:
            query = "UPDATE `datastore_subset_directory` SET path = %s WHERE directory_id = %s"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['path'], payload['directory_id']))
            self.db.connection.commit()
            cursor.close()
            return payload
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    def delete(self, directory_id):
        try:
            query = "UPDATE `datastore_subset_directory` SET is_active = 0 WHERE directory_id = %s"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (directory_id,))
            self.db.connection.commit()
            cursor.close()
            return f"Deleted {directory_id}"
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
        
    