import random
import string
import traceback

from flask import current_app, jsonify


class TableDatastoreSubset:
    def __init__(self):
        from app import db
        self.db = db
        

    def generate_id(self):
        N = 22
        id = 'DSB' + ''.join(random.choices(string.digits, k= N - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=N - 2))
        return id

    def insert(self, payload):
        try:
            subset_id = self.generate_id()
            payload['ds_subset_id'] = subset_id
            payload['is_active'] = 1
            query = "INSERT INTO `datastore_subset` (ds_subset_id, datastore_id, name, path, type, is_active, is_public, created_at, created_by) VALUES (%s, %s, %s, %s, %s, 1, 1, NOW(), %s)"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (payload['ds_subset_id'], payload['datastore_id'], payload['name'], payload['path'],payload['type'], payload['owner']))
            self.db.connection.commit()
            cursor.close()
            return payload
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"

    def get_item(self, subset_id):
        try:
            query = "SELECT datastore_id, ds_subset_id, name, type, is_public, path, created_by FROM datastore_subset WHERE ds_subset_id = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (subset_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"
    
    def get_item_by_name(self, name, type):
        try:
            query = "SELECT datastore_id, ds_subset_id, name, type, is_public, path, created_by FROM datastore_subset WHERE name = %s AND type = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (name, type))
            result = cursor.fetchone()
            cursor.close()
            return result
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"

    def get_list(self, datastore_id):
        try:
            query = "SELECT * FROM datastore_subset WHERE datastore_id = %s AND is_active = 1"
            cursor = self.db.connection.cursor()
            cursor.execute(query, (datastore_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {e}")
            return f"{self.__class__.__name__}::ERROR - {e}"

    def update(self):
        current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {'Not implemented'}")
        return "Not implemented"

    def delete(self):
        current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {'Not implemented'}")
        return "Not implemented"

