import os
import traceback
from flask import current_app, json

from api.datastore.handler.request_create_subset import RequestCreateSubset
from api.datastore.handler.request_download_files_to_directory import RequestDownloadFilesToDirectory
from dao.table_datastore_directory import TableDatastoreDirectory
from dao.table_datastore_subset import TableDatastoreSubset
from dao.table_datastore_subset_item import TableDatastoreSubsetItem


class RequestAddSubset:
    def __init__(self, payload):
        self.payload = payload
        self.db = TableDatastoreSubset()
        self.subset_item_db = TableDatastoreSubsetItem()
        self.subset_directory_db = TableDatastoreDirectory()

    def do_process(self):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} - {self.payload}")

            # Check if subset exists for this group. If so use that subset
            name = self.concat_name(self.payload['subset_info'])
            subset = self.db.get_item_by_name(name, self.payload['dataset_type'])

            if subset is None:
                request_create_subset = RequestCreateSubset(self.payload, name)
                subset = request_create_subset.do_process()


            current_app.logger.debug(f"{self.__class__.__name__} - Subset: {subset}")

            # Get video directory
            video_directory = self.subset_directory_db.get_item_by_type(subset['ds_subset_id'], 'video')
            
            payload_download_files_to_directory = {
                "subset_info": self.payload['subset_info'],
                "directory": video_directory['path'],
            }

            current_app.logger.debug(f"{self.__class__.__name__} - Payload: {payload_download_files_to_directory}")

            #This will check if video files exist in folders, if not it will dowload them
            request_download_files = RequestDownloadFilesToDirectory(subset, payload_download_files_to_directory)
            response_download_files = request_download_files.do_process()

            if response_download_files == "COMPLETE":
                current_app.logger.debug(f"{self.__class__.__name__} - Subset {subset['ds_subset_id']} files ready: {response_download_files}")
            else:
                current_app.logger.debug(f"{self.__class__.__name__} - There was a problem adding the subset, verify files are in the correct directories: {response_download_files}")

               
            # Subset needs to track creation of GT / ROI annotations
            # Gather subset videos and add as subset items

            return "success"
            
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} ::: {traceback.format_exc()} - {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"


    def concat_name(self, subset_info):
        keys = subset_info.keys()

        name = ""
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                name += key + ":" + subset_info[key]
            else:
                name += key + ":" + subset_info[key] + "_"

        return name