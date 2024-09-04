import os
from flask import current_app

from api.datastore.handler.request_download_files_to_directory import RequestDownloadFilesToDirectory
from dao.table_datastore_directory import TableDatastoreDirectory
from dao.table_datastore_subset import TableDatastoreSubset


class RequestCreateSubset:
    def __init__(self, payload, subset_name):
        self.payload = payload
        self.subset_name = subset_name
        self.directory_db = TableDatastoreDirectory()
        self.subset_db = TableDatastoreSubset()

    def do_process(self):
        try:
            
            current_app.logger.debug(f"{self.__class__.__name__} - {self.payload}")
            # Check path for necessary directories, create if not exist
            ## Contactenate path from payload
            directory = self.create_subset_directory(self.payload['subset_info'], self.payload['dataset_type'])

            subset_payload = {
                "datastore_id": os.environ.get('DATASTORE_ID_AOLME'),
                "name": self.subset_name,
                "path": directory['subset_dir'],
                "type": self.payload['dataset_type'],
                "owner": self.payload['owner'],
                "description": self.payload['description']
            }
    
            #Create a subset reference in database using the subset_info from the payload
            subset = self.subset_db.insert(subset_payload)

            # Create Directories for video, ground truth, trims, annotations
            video_dir = self.create_utility_directories(subset, directory)

            # Use link to download videos and store them in the subset directory78
            return subset
            
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} - ERROR: {e}")
            return f"{self.__class__.__name__}:: ERROR - {e}"
        
    
    def create_subset_directory(self, subset_info, dataset_type):
        datastore_root_dir = os.environ.get('DATASTORE_ROOT')

        subset_info['type'] =  dataset_type 

        order = ['cohort', 'level', 'school', 'group', 'date', 'type']

        subset_path = datastore_root_dir
        date_dir = ""
        for i, key in enumerate(order):
            
            if key == 'date':
                subset_path += "/" + subset_info[key].replace('-', '')
                date_dir = subset_path
            elif key == 'type':
                subset_path += "/" + subset_info[key].lower()
            elif key == 'school':
                subset_path += "/" + key + "-" + subset_info[key].lower()
            else:
                subset_path += "/" + key + "-" + subset_info[key]


            if not os.path.exists(subset_path):
                current_app.logger.debug(f"{self.__class__.__name__} - creating-directory:: {subset_path}")
                os.makedirs(subset_path)
      
            else:
       
                current_app.logger.debug(f"{self.__class__.__name__} - directory-exists:: {subset_path}")

            
        return { "subset_dir": subset_path, "date_dir": date_dir }
    

    def create_utility_directories(self, subset, directories):
        subset_dirs = ['ground-truth', 'trims', 'annotations']
        date_dirs = ['video']

        existing_directories = self.directory_db.get_list_by_subset_id(subset['ds_subset_id'])

        for date_dir in date_dirs:
            path = directories['date_dir'] + "/" + date_dir
            if date_dir == "video":
                    video_dir = path

            if not os.path.exists(path):
                current_app.logger.debug(f"{self.__class__.__name__} - creating-directory:: {path}")
                self.directory_db.insert({
                    "ds_subset_id": subset['ds_subset_id'],
                    "type": date_dir,
                    "path": path,
                    "owner": subset['owner']
                })
                os.makedirs(path)
                
            else:
                current_app.logger.debug(f"{self.__class__.__name__} - directory-exists:: {path}")

                if existing_directories is not None:
                    toggle = False
                    for dir in existing_directories:
                        if path == dir['path']:
                            toggle = True
                            break
                    
                    if not toggle:
                        self.directory_db.insert({
                            "ds_subset_id": subset['ds_subset_id'],
                            "type": date_dir,
                            "path": path,
                            "owner": subset['owner']
                        })

                

            

        for subset_dir in subset_dirs:
            path = directories['subset_dir'] + "/" + subset_dir
            if not os.path.exists(path):
                current_app.logger.debug(f"{self.__class__.__name__} - creating-directory:: {path}")
                os.makedirs(path)
                self.directory_db.insert({
                    "ds_subset_id": subset['ds_subset_id'],
                    "type": subset_dir,
                    "path": path,
                    "owner": subset['owner']
                })
                
            else:
                current_app.logger.debug(f"{self.__class__.__name__} - directory-exists:: {path}")
                if existing_directories is not None:
                    toggle = False
                    for dir in existing_directories:
                        if path == dir['path']:
                            toggle = True
                            break
                    
                    if not toggle:
                        self.directory_db.insert({
                            "ds_subset_id": subset['ds_subset_id'],
                            "type": date_dir,
                            "path": path,
                            "owner": subset['owner']
                        })

        return video_dir



        
    
