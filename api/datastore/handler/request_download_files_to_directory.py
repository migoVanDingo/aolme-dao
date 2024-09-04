import os
from flask import current_app
import requests
from dao.table_datastore_subset_item import TableDatastoreSubsetItem
from dao.table_ground_truth import TableGroundTruth
from dao.table_video import TableVideo
import urllib.request


class RequestDownloadFilesToDirectory:
    def __init__(self, subset, payload):
        self.subset = subset
        self.ds_subset_id = subset['ds_subset_id']
        self.owner = subset['created_by']
        self.payload = payload
        self.ds_subset_item_db = TableDatastoreSubsetItem()
        self.video_db = TableVideo()
        self.gt_db = TableGroundTruth()
        os.environ['no_proxy'] = "*"

    def do_process(self):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} - PARAMS -- subset: {self.subset}  -- payload: {self.payload}")    
            subset_type = self.payload['subset_info']['type']
            del self.payload['subset_info']['group']
            del self.payload['subset_info']['type']

            video_list = self.video_db.get_list(
                self.payload['subset_info'])
            
                    
            if video_list is None:
                current_app.logger.debug(f"{self.__class__.__name__} - No videos found")
            else:
                current_app.logger.debug(
                f"{self.__class__.__name__} - Downloading videos to: {self.payload['directory']} -- video_list: {video_list}")

                for video in video_list:

                    # Check if video exists in directory
                    if not os.path.isfile(os.path.join(self.payload['directory'], video['video_name'])):

                        video_url = video['link']
                        directory = self.payload['directory']
                        self.download_video_series(video_url, directory, video)
                    else:
                        current_app.logger.debug(f"{self.__class__.__name__} - File already exists: {os.path.join(directory, video['video_name'])}")

                    # Check for existing ground truth and add as subset item
                    ground_truth = self.gt_db.get_by_video_and_type(
                        video['video_id'], subset_type.upper())
                    

                    if ground_truth is not None:
                        ground_truth_name = ground_truth['filename']
                        ground_truth_path = ground_truth['path']
                        self.add_to_subset_items(self.ds_subset_id, ground_truth['ground_truth_id'], ground_truth_name, self.owner, ground_truth_path)

                current_app.logger.debug(f"{self.__class__.__name__}:: Download complete")

            return "COMPLETE"

        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"



    def download_video_series(self, video_link, directory, video):
        try:
            
            current_app.logger.debug(f"{self.__class__.__name__} - Downloading... {video_link} to {os.path.join(directory, video['video_name'])}")

            r = requests.get(video_link, stream=True)

            with open(os.path.join(directory, video["video_name"]), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)


            self.add_to_subset_items(self.ds_subset_id, video["video_id"], video["video_name"], self.owner, os.path.join(directory, video["video_name"]))

            current_app.logger.debug(f"{self.__class__.__name__} - Download Complete!! {video_link} to {os.path.join(directory, video['video_name'])}")
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"

    def add_to_subset_items(self, subset_id, item_id, name, owner, path):
        try:

            item = self.ds_subset_item_db.get_item(item_id)
            if item is not None:
                current_app.logger.debug(f"{self.__class__.__name__} - Item Already exists: ds_subset_item_id: {item_id}  --  subset_id: {subset_id}")
                return "Item Already exists: ds_subset_item_id: {item_id}  --  subset_id: {subset_id}"
            
            payload = {
                'ds_subset_id': subset_id,
                'ds_subset_item_id': item_id,
                'name': name,
                'path': path,
                'owner': owner,
                'type': 'video'
            }
            self.ds_subset_item_db.insert(payload)
            current_app.logger.debug(f"{self.__class__.__name__} - Added to subset items: {payload}")
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"
