from abc import ABC, abstractmethod

from dao.table_ground_truth import TableGroundTruth
from dao.table_trims import TableTrims
from dao.table_video import TableVideo
class AbstractDatastore(ABC):

    def __init__(self):
        super().__init__()
        self.table_video = TableVideo()
        self.table_ground_truth = TableGroundTruth()
        self.table_trims = TableTrims()

    @abstractmethod
    def do_process(self):
        pass

    # ACCESS groups TABLE
    def get_video(self, video_id):
        return self.table_video.get_by_id(video_id)

    def get_video_list(self, params):
        return self.table_video.get_list(params)


    # ACCESS ground_truth TABLE
    def get_ground_truth(self, video_id):
        return self.table_ground_truth.get_by_id(video_id)
    
    def get_ground_truth_by_video_and_type(self, video_id, type):
        return self.table_ground_truth.get_by_video_and_type(video_id, type)

    def get_ground_truth_list(self, params):
        return self.table_ground_truth.get_list(params)
    
    # ACCESS trims TABLE
    def add_trim(self, payload):
        return self.table_trims.add(payload)
    
    def get_trim_list_by_video_id(self, video_id):
        return self.table_trims.get_list_by_video_id(video_id)
    
    def get_trim_list_by_ground_truth_id(self, ground_truth_id):
        return self.table_trims.get_list_by_ground_truth_id(ground_truth_id)