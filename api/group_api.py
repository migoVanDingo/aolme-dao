import json, requests
from datetime import datetime
import pandas as pd
import os
import random
import string
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_cors import CORS
 

group_api = Blueprint('group_api', __name__)

@group_api.route('/', methods=['GET'])
def get_group():
    current_app.logger.debug(f" Request: {request}")
    from app import db
    query = "SELECT * FROM `groups`"
    cursor = db.connection.cursor()
    cursor.execute(query)
    groups = cursor.fetchall()
    cursor.close()
    
    for group in groups:
        group['date'] = group['date'].strftime('%Y-%m-%d')  

    #current_app.logger.debug(f" Response: {groups}")
    return jsonify(groups)

@group_api.route('/entities', methods=['GET'])
def get_entities():
    from app import db
    query = "SELECT cohort, level, school, date, group_name, facilitator, video_id FROM `groups` WHERE quality = 2"
    cursor = db.connection.cursor()
    cursor.execute(query)
    groups = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(groups)

    cohorts = df['cohort'].unique()
    levels = df['level'].unique()
    schools = df['school'].unique()
    dates = df['date'].unique()
    group_names = df['group_name'].unique()
    facilitators = df['facilitator'].unique()

    cohortList = []
    levelList = []
    schoolList = []
    dateList = []
    groupList = []


    entities = []
    # For each cohort, append the levels that exist within it. For each level, append the schools that exist within it. For each school, append the dates that exist within it. For each date, append the group names that exist within it.
    for cohort in cohorts:
        cohortList.append(cohort)
        cohortLevels = df[df['cohort'] == cohort]['level'].unique()
        for level in cohortLevels:
            levelList.append(level)
            levelSchools = df[(df['cohort'] == cohort) & (df['level'] == level)]['school'].unique()
            for school in levelSchools:
                schoolList.append(school)
                schoolDates = df[(df['cohort'] == cohort) & (df['level'] == level) & (df['school'] == school)]['date'].unique()
                for date in schoolDates:
                    dateList.append(date)
                    dateGroups = df[(df['cohort'] == cohort) & (df['level'] == level) & (df['school'] == school) & (df['date'] == date)]['group_name'].unique()
                    for group in dateGroups:
                        groupList.append(group)
                        facilitators = df[(df['cohort'] == cohort) & (df['level'] == level) & (df['school'] == school) & (df['date'] == date) & (df['group_name'] == group)]['facilitator'].unique()
                        for facilitator in facilitators:
                            entities.append({
                                "cohort": cohort,
                                "level": level,
                                "school": school,
                                "date": "{}".format,
                                "group_name": group,
                                "facilitator": facilitator
                            })


    current_app.logger.debug(f" get_entities :: response: {entities}")



    return jsonify(entities)

@group_api.route('/categories', methods=['GET'])
def get_categories():
    from app import db

    result = {}
    queries = [
        {"category": "date", "q":"SELECT DISTINCT date FROM `groups`"},
        {"category": "facilitator", "q":"SELECT DISTINCT facilitator FROM `groups`"},
        {"category": "school", "q":"SELECT DISTINCT school FROM `groups`"},
        {"category": "cohort", "q":"SELECT DISTINCT cohort FROM `groups`"},
        {"category": "level", "q":"SELECT DISTINCT level FROM `groups`"},
    ]

    for query in queries:
        cursor = db.connection.cursor()
        cursor.execute(query['q'])
        c = cursor.fetchall()
        result[query['category']] = c
        cursor.close()
    current_app.logger.debug(f" Response: {jsonify(result)}")
    return jsonify(result)

@group_api.route('/update-video-id', methods=['GET'])
def update_video_id():

    from app import db
    
    #GET ALL GROUPS
    query = "SELECT * FROM `groups`"
    cursor = db.connection.cursor()
    cursor.execute(query)
    groups = cursor.fetchall()
    cursor.close()

    count = 0
    for group in groups:
        N = 22
        video_id = 'VID' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        query = f"UPDATE `groups` SET video_id = '{video_id}' WHERE idx = {group['idx']}"
        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        cursor.close()
        count += 1

    return jsonify({"message": f"Updated {count} records"})

@group_api.route('/ground-truth', methods=['POST', 'OPTIONS'])
def add_group():
    from app import db
    data = json.loads(request.data)
    print(f" Request: {data}")
    current_app.logger.debug(f" Request: {data}")

    #generate ground truth id
    N = 22
    ground_truth_id = 'GTR' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

    #insert ground truth id, video id, filename, path, type, is_active, created_at and created_by
    query = f"INSERT INTO `ground_truth` (ground_truth_id, video_id, filename, path, type, file_type, is_active, created_at, created_by) VALUES ('{ground_truth_id}', '{data['video_id']}', '{data['filename']}', '{data['path']}', '{data['type']}', '{data['file_type']}', 1, NOW(), '{data['created_by']}')"

    cursor = db.connection.cursor()
    cursor.execute(query)
    db.connection.commit()
    cursor.close()
    current_app.logger.debug(f" Response: {jsonify({'message': 'success'})}")
    print(f" Done")
    data['ground_truth_id'] = ground_truth_id
    data['is_active'] = 1
    return jsonify({'message': 'success', 'data': data})


@group_api.route('/ground-truth/update', methods=['GET'])
def ground_truth_path_update():
    ### I rearranged the path of the file system so that dataset type (Typing, Writing, Talking was within the date folder) This endpoint made that change in the database. 


    from app import db
    query = "SELECT * FROM `ground_truth`"
    cursor = db.connection.cursor()
    cursor.execute(query)
    ground_truths = cursor.fetchall()
    cursor.close()

    count = 0
    for ground_truth in ground_truths:
        old_path = ground_truth['path']
        paths = old_path.split('/')
        date = paths.pop()
        dataset_type = paths.pop()

        new_path = ""

        for i, path in enumerate(paths):
            if(i == 0):
                new_path += path
            else:
                new_path += f"/{path}"

        new_path += f"/{date}/{dataset_type}"
        query = f"UPDATE `ground_truth` SET path = '{new_path}' WHERE ground_truth_id = '{ground_truth['ground_truth_id']}'"

        cursor = db.connection.cursor()
        cursor.execute(query)
        db.connection.commit()
        cursor.close()


        if(count % 10 == 0):
            print(f"Updated {count} records")
            print(f"Old path: {old_path} New path: {new_path}")

        count += 1

        

        
    return jsonify({"message": "success"})


@group_api.route('/ground-truth/metadata', methods=['GET'])
def update_metadata():
    from app import db
    query = "SELECT * FROM `groups`"
    cursor = db.connection.cursor()
    cursor.execute(query)
    videos = cursor.fetchall()
    cursor.close()

    root_path = os.environ.get('DATASTORE_ROOT')

    for video in videos:
        link = video['link']
        r = requests.get(link, stream=True)
        

        
        school_dir = os.path.join(root_path, f"cohort-{video['cohort']}", f"level-{video['level']}", f"school-{video['school'].lower()}")

        group_dir = os.path.join(school_dir, f"group-{video['group_name']}")

        date = video['date'].replace('-', '')

        dataset_type = video['dataset_type']

        if not os.path.exists(group_dir):
            os.makedirs(group_dir)

       
        


