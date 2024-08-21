import math
import os
import pandas as pd
import ffmpeg
from flask import current_app

from api.datastore.abstract_datastore import AbstractDatastore


class RequestCreateTrimVideosGroundTruth(AbstractDatastore):
    def __init__(self, data):
        self.data = data

    def do_process(self):

        current_app.logger.debug(f"{self.__class__.__name__} :: data: {self.data}")

        ground_truth_path = self.data['ground_truth_path']
        video_path = self.data['video_path']
        output_path = self.data['output_path']
        frame_rate = self.data['frame_rate']
        video_id = self.data['video_id']
        ground_truth_id = self.data['ground_truth_id']

        # Read Ground Truth
        ground_truth_df = pd.read_csv(ground_truth_path)

        # Add 3 sec column to dataframe
        ground_truth_df['f0_3sec'] = self.add_3sec_activity_instance(ground_truth_df)

        # Trim Video
        output_path_list = self.trim_video(ground_truth_df, video_path, video_id, ground_truth_id, output_path, frame_rate)


    def add_3sec_activity_instance(self, df: pd.DataFrame):
        three_second_list = []
        for i, row in df.iterrows():
            initial_frame = row['f0']
            frame_duration = row['f']

            three_second_list += [math.floor(initial_frame + frame_duration/2) - 45]

        return three_second_list
    
    def trim_video(self, ground_truth_df: pd.DataFrame, video_path: str, video_id: str, ground_truth_id: str, output_path: str, frame_rate: int):
        try:
            output_path_list = []
            # Loop through dataframe
            for i, row in ground_truth_df.iterrows():
                start_frame = row['f0_3sec']
                end_frame = row['f0_3sec'] + 90

                oname = f"{os.path.splitext(os.path.basename(row['name']))[0]}_{row['person']}_{start_frame}_{end_frame}.mp4"

                # Time stamps from frame numbers
                sts = start_frame / frame_rate
                nframes = end_frame - start_frame

                # Use ffmpeg to trim and crop the video
                input_video = ffmpeg.input(video_path, ss=sts)
                cropped_video = ffmpeg.crop(input_video, x=row['w0'], y=row['h0'], width=row['w'], height=row['h'])
                trimmed_video = ffmpeg.output(cropped_video, os.path.join(output_path, oname), vframes=nframes, vcodec='libx264', crf=0)

                # Run the ffmpeg command
                ffmpeg.run(trimmed_video, overwrite_output=True)

                trim_entry = self.add_trim(video_id, ground_truth_id, output_path)

                output_path_list.append({"trim_id": trim_entry['trim_id'], "output_path": os.path.join(output_path, oname)})

            return output_path_list
        
        except Exception as e:
            return "error"
