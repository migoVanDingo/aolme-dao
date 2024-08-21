from flask import current_app, jsonify
from api.datastore.abstract_datastore import AbstractDatastore
class RequestCreateDataset(AbstractDatastore):
    def __init__(self, data, dataset_type):
        super().__init__()
        self.data = data
        self.dataset_type = dataset_type


    def do_process(self):
        try:
            #Log payload data
            current_app.logger.debug(f"{self.__class__.__name__} :: data: {self.data}")

 
            data_list = []
    
            for data in self.data:
                # Get list of videos for an item 
                # This is like a set of group videos e.g. C1L1P-20170302-A vids 1-6, or vids for a whole cohort/level C1L1 All groups, all videos
                item_list = self.get_video_list(data)


                # Loop through list and get ground truth for each video item
                for item in item_list:
                    ground_truth = self.get_ground_truth_by_video_and_type(item['video_id'], self.dataset_type)
                    data_list.append({"video": item, "ground_truth": ground_truth})


            #Log response data
            current_app.logger.debug(f"{self.__class__.__name__} :: data_list: {data_list}")

            return jsonify(data_list)


        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: {e}")
            return jsonify("ERROR")