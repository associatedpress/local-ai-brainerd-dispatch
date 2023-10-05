from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from threading import Thread
import pika
import os
from datetime import datetime
from pytz import timezone
from services.file_parsing_service import ParseFile
import json
from services.report_service import ReportService
from services.generic_service  import GenericService
from services.category_service import CategoryService
from services.priority_service import PriorityService
from services.login_service import LoginService
from services.agency_service import AgencyService
from dbmappers.general_setting import GeneralSetting
from services.user_service import UserService
import uuid
from services.parser_mapping_service import ParserMappingService


app = Flask(__name__)
CORS(app)
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ app.config['DB_USERNAME'] + ':' + app.config['DB_PASSWORD'] + '@' + app.config['DB_CONFIG'] + '/' + app.config['DATABASE_NAME']

if __name__ == "__main__":
	app.run()

'''
    Initiating database connection with SQLAlchemy
'''
db = SQLAlchemy(app)


'''
    session dictionary
'''
sessions = {}



'''
    Check if the session token sent by client is valid and return the username for the session token
'''
def is_authenticated(session_token):
    print(session_token)
    print(sessions)
    if session_token in sessions:
        print("Logged in as - " + sessions[session_token])
        return sessions[session_token]
    raise Exception("Unauthorized request")


@app.route('/is_authenticated', methods=['GET'])
def is_user_authenticated():
    session_token = request.headers.get('session-token')
    if session_token in sessions:
        return json.dumps({'response': True}), 200
    else:
        return json.dumps({'response': False}), 401



'''
    Rest end points to authenticate the user
'''
@app.route('/login', methods=['POST'])
def do_login():
    login_details = request.get_json(force=True)
    username = login_details['username']
    password = login_details['password']
    login_service = LoginService()
    user = login_service.get_user_info(username)
    passwd = login_service.get_encrypted_password(password)
    print(passwd)
    print(password)
    if(user.user_password == passwd):
        print("Creating session for user " + username)
        session_token = str(uuid.uuid4())
        sessions[session_token] = str(user.user_id)
        print(session_token)
        print(username)
        return json.dumps({'response': {"session_token" : session_token, "username": username}}), 200
    else:
        return json.dumps({'response': "Incorrect Credentials"}), 401
    

'''
    Rest end points to authenticate the user
'''
@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user_maintenance():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    user_service = UserService()
    if request.method == 'GET':
        print("Getting the list of users")
        response = user_service.get_user_list()
        return json.dumps({'response': response}), 200 
    
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            print("Creating user")
            name = data.get('user_name')
            password = data.get('user_password')
            first_name = data.get('user_firstname')
            last_name = data.get('user_lastname')
            print(name)
            print(password)
            print(first_name)
            print(last_name)
            return user_service.add_user(name, password, first_name, last_name)
        else:
            return "Invalid JSON data in the request body", 400
        
    elif request.method == 'DELETE':
        user_id = request.args.get('user_id')
        if user_id:
            print("Deleting user")
            return user_service.delete_user(int(user_id))
        else:
            return "Invalid JSON data in the request body", 400
    


'''
    Rest end points to logout the authenticated user
'''
@app.route('/logout', methods=['POST'])
def do_logout():
    global sessions
    session_token = request.headers.get('session-token')
    print("Deleting session for user " +  sessions[session_token])   
    del sessions[session_token]
    return json.dumps({'response': 'success'}), 200




'''
    Rest API to process the police blotters.
    Here the RestAPI sends the request details to 'upload_blotter_queue' and notifies UI
'''
@app.route('/process_blotters', methods=['POST'])
def submit():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return jsonify({'response': "Unauthorized request"}), 401
    
    if 'file' not in request.files:
        return jsonify({'response': 'No file part in the request'}), 400
    
    file = request.files['file']
    agency_id = request.form.get('agency')
    print('Agency Id :' + str(agency_id))
    
    if file.filename == '':
        return jsonify({'response': 'No file selected'}), 400

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    print("SQL ALchemy URI " + app.config['SQLALCHEMY_DATABASE_URI'] )
    Session = sessionmaker(bind=engine)
    session = Session()
    staging_location = session.query(GeneralSetting).filter_by(gs_name= 'STAGING_LOCATION').first()
    staging_location = staging_location.gs_value
    print("File will be saved to staging location " + staging_location)
    if not os.path.exists(staging_location):
        os.makedirs(staging_location)
    
    file_path = os.path.join(staging_location, file.filename)
    file.save(file_path)
    print(file.filename)
    rjson = {}
    rjson['file_path'] = file_path
    rjson['agency_id'] = agency_id
    rjson['user_id'] = user_id

    parsefile = ParseFile(file_path, agency_id, int(user_id))
    return parsefile.parsefile();


'''
    Rest API to get the list of all the unpublished blotters in the system
'''
@app.route('/updateparsermappings', methods=['POST'])
def updateparsermappings():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Updating the parser mappings based on user verification")
    parser_mapping_service = ParserMappingService()
    parser_id = request.args.get('parser_id')
    agency_id = request.args.get('agency_id')
    update_parser_map = request.json
    print(parser_id)
    print(agency_id)
    print(update_parser_map)
    response = parser_mapping_service.update_parser_mappings(parser_id, agency_id, update_parser_map)
    return json.dumps({'response': response}), 200


'''
    Rest API to get the list of all the unpublished blotters in the system
'''
@app.route('/getunpublishedreports', methods=['GET'])
def getunpublishedreports():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Getting all the un published reports")
    report_service = ReportService()
    response = report_service.fetch_unpublished_reports(int(user_id))
    return json.dumps({'response': response}), 200



'''
    Rest API to get the list of all the blotters that are published to vendor for story generation
'''
@app.route('/getpublishedreports', methods=['GET'])
def getpublishedreports():
    record_count = request.args.get('record_count', type=int)
    print(record_count)
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Getting the recently published " + str(record_count) + " reports" )
    report_service = ReportService()
    response = report_service.fetch_published_reports(int(user_id), record_count)

    return json.dumps({'response': response}), 200

    

'''
    Rest API to publish the list of blotters to vendor for story generation 
'''
@app.route('/publishreports', methods=['POST'])
def publishreports():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Publishing the reports")
    caseid_list = request.get_json()['case_ids']
    report_service = ReportService()
    response = report_service.publish_reports_to_vendor(caseid_list, int(user_id))
    return json.dumps({'response': response}), 200



'''
    Rest API to get the list of all the unpublished blotters in the system
'''
@app.route('/getignoredreports', methods=['GET'])
def getignoredreports():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Getting all the ignored reports")
    report_service = ReportService()
    response = report_service.fetch_ignored_reports(int(user_id))
    return json.dumps({'response': response}), 200




'''
    Rest API to add the list of items to ignore list 
'''
@app.route('/ignorecases', methods=['POST'])
def ignorecases():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Making the list of cases as ignored")
    caseid_list = request.get_json()['case_ids']
    report_service = ReportService()
    response = report_service.add_cases_to_ignore_list(caseid_list, int(user_id))
    return json.dumps({'response': response}), 200




'''
    Rest API to restore the cases from ignore list
'''
@app.route('/restorecases', methods=['POST'])
def restore_ignoredcases():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Restoring the list of cases from ignore list")
    caseid_list = request.get_json()['case_ids']
    report_service = ReportService()
    response = report_service.restore_cases_from_ignore_list(caseid_list, int(user_id))
    return json.dumps({'response': response}), 200



'''
    Rest API to get the list of agencies in the system, create a new agency, and delete the agency
'''
@app.route('/agencies', methods=['GET', 'POST', 'DELETE'])
def get_agencies():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    generic_service = AgencyService()
    if request.method == 'GET':
        print("Getting the agencies list")
        response = generic_service.get_agencies_list(int(user_id))
        return json.dumps({'response': response}), 200 
    
    elif request.method == 'POST':
        print("Creating the agency")
        agency_name = request.args.get('name')
        city = request.args.get('city')
        state = request.args.get('state')
        parser = request.args.get('parser')
        print(agency_name)
        print(city)
        print(state)
        print(parser)
        return generic_service.add_agency(user_id, agency_name, city, state, parser)
    
    elif request.method == 'DELETE':
        print("CDeleting the agency")
        agency_id = request.args.get('agency_id')
        return generic_service.delete_agency(agency_id)



'''
    Rest API to get the list of publications belonging to an user in the system
'''
@app.route('/publications', methods=['GET'])
def get_publications():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    print("Getting the publication list")
    generic_service = GenericService()
    response = generic_service.get_publications_list(int(user_id))
    return json.dumps({'response': response}), 200



'''
    Rest API to get the list of categories in the system, create a new category and delete the category
'''
@app.route('/categories', methods=['GET', 'POST', 'DELETE'])
def get_categories():
    session_token = request.headers.get('session-token')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    category_service = CategoryService()
    if request.method == 'GET':
        print("Getting the category list")       
        response = category_service.get_categories_list(int(user_id))
        return json.dumps({'response': response}), 200 
    elif request.method == 'POST':
        category_name = request.args.get('category_name')
        print("Adding a category to the category list")
        #JSON is contstructed in the service method already
        return category_service.add_category(int(user_id), category_name)
    elif request.method == 'DELETE':
        category_id = request.args.get('category_id')
        print("Deleting a category from the category list")
        #JSON is contstructed in the service method already
        return category_service.delete_category(int(user_id), int(category_id))



'''
    Rest API to get the list of categories along with priority, add priority to existing category and delete the priority
'''
@app.route('/category_priority_list', methods=['GET', 'POST', 'DELETE'])
def get_category_priority_list_by_publication():
    session_token = request.headers.get('session-token')
    pubId = request.args.get('pubId')
    try:
        user_id = is_authenticated(session_token)
    except:
        return json.dumps({'response': "Unauthorized request"}), 401
    
    priority_service = PriorityService()
    if request.method == 'GET':
        print("Getting the categories with respective priorities")
        response = priority_service.get_category_priority_list_by_publication(int(user_id), pubId)
        return json.dumps({'response': response}), 200
    
    elif request.method == 'POST':
        print("Adding priority for the new category")
        category_id = request.args.get('category_id')
        publication_id = request.args.get('pub_id')
        priority = request.args.get('priority')
        return priority_service.add_priority_to_category(int(user_id), int(category_id), int(publication_id), int(priority))
    
    elif request.method == 'DELETE':
        print("Deleting the priority for the category")
        priority_id = request.args.get('priority_id')
        return priority_service.delete_priority(int(user_id), int(priority_id))



    


    

