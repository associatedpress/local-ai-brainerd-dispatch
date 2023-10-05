# The JSON API format for report submission is designed to communicate with the Lede AI API service. This will need to be redeveloped for other automated writing services.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from threading import Thread
import pika
import os
import datetime
from pytz import timezone
from dbmappers.report import Report
from dbmappers.casedetail import CaseDetail
from dbmappers.category import Category
from dbmappers.priority import Priority
from dbmappers.state import State
from dbmappers.publication import Publication
from dbmappers.agency import Agency
from dbmappers.user import User
from dbmappers.general_setting import GeneralSetting
from config import Config
import json
import requests


class ReportService:
    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME

    def fetch_published_reports(self, user_id, record_count):

        engine = create_engine(self.SQL_Alchemy_URI)
        print("SQL_Alchemy_URI  - " + self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        if record_count != None:
            casedetails_ids = [row.case_id for row in session.query(Report.case_id)
                    .filter_by(report_sent_to_vender=True)
                    .order_by(desc(Report.report_id))
                    .limit(record_count)
                    .all()]
        else:
            casedetails_ids = [row.case_id for row in session.query(Report.case_id).filter_by(report_sent_to_vender=True).all()]
        casedetails = session.query(CaseDetail).filter(CaseDetail.case_id.in_(casedetails_ids)).all()
        for casedetail in casedetails:
            print(casedetail.case_id)

        casedetails_json = []
        for casedetail in casedetails:
            categoryname = None
            category = session.query(Category).filter_by(category_id=casedetail.category_id).first()
            if category != None:
                categoryname = category.category_name

            user = 1
            publication_id = 1

            priority_level = None
            priority = session.query(Priority).filter_by(category_id=casedetail.category_id, publication_id = publication_id).first()
            if priority != None:
                priority_level = priority.priority

            state_name = None
            state = session.query(State).filter_by(state_id = casedetail.state_id).first()
            if state != None:
                state_name = state.usps_state_abbrrevation

            agency_name = None
            agency_details = session.query(Agency).filter_by(agency_id=casedetail.agency_id).first()
            if agency_details != None:
                agency_name = agency_details.agency_name

            case_date = None
            if casedetail.reported_dt != None:
                case_date = str(casedetail.reported_dt)

            report_detail = session.query(Report).filter_by(case_id=casedetail.case_id).first()
            report_sent_date = None
            if report_detail != None:
                if report_detail.report_sent_dt != None:
                    report_sent_date = str(report_detail.report_sent_dt)

                report_sent_user_id = report_detail.report_sent_by_userid
                report_sent_user = session.query(User).filter_by(user_id=report_sent_user_id).first()
                report_sent_user_name = report_sent_user.user_firstname + " " + report_sent_user.user_lastname
                reported_publicationid = report_detail.publication_id
                reported_publication = session.query(Publication).filter_by(publication_id=reported_publicationid).first()
                reported_publication_name = reported_publication.publication_name

            casedetail_json = {
                'cid': casedetail.case_id,
                'case_description': casedetail.case_desc,
                'category': categoryname,
                'reported_dt': case_date,
                'agencyid': agency_name,
                'addressline1': casedetail.address_line1,
                'city': casedetail.city,
                'state': state_name,
                'zipcode': casedetail.zipcode,
                'priority': priority_level,
                'publication': reported_publication_name,
                'report_sent_dt': report_sent_date,
                'user': report_sent_user_name
            }
            casedetails_json.append(casedetail_json)

        # return the casedetails results in JSON format
        session.close()
        return casedetails_json


    def fetch_unpublished_reports(self, user_id):
        
        engine = create_engine(self.SQL_Alchemy_URI)
        print("SQL_Alchemy_URI  - " + self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        casedetails_ids = [row.case_id for row in session.query(Report.case_id).all()]
        print(casedetails_ids)
        print(set(casedetails_ids))
        case_ids_list = set(casedetails_ids)
        casedetails = session.query(CaseDetail).filter((CaseDetail.is_ignored == False) & (~CaseDetail.case_id.in_(set(case_ids_list)))).all()
        for casedetail in casedetails:
            print(casedetail.case_id)

        casedetails_json = []
        casedetails_agencymap = {}
        for casedetail in casedetails:
            category = session.query(Category).filter_by(category_id=casedetail.category_id).first()
            categoryname = None
            if category != None:
                categoryname = category.category_name

            user = 1
            publication_id = 1#user.pubid

            priority = session.query(Priority).filter_by(category_id=casedetail.category_id, publication_id = publication_id).first()
            priority_level = None
            if priority != None:
                priority_level = priority.priority

            state = session.query(State).filter_by(state_id = casedetail.state_id).first()
            state_name = None
            if state != None:
                state_name = state.usps_state_abbrrevation

            agency_details = session.query(Agency).filter_by(agency_id=casedetail.agency_id).first()
            agency_name = None
            if agency_details != None:
                agency_name = agency_details.agency_name

            case_date = None
            if casedetail.reported_dt != None:
                case_date = str(casedetail.reported_dt)


            casedetail_json = {
                'cid': casedetail.case_id,
                'case_description': casedetail.case_desc,
                'category': categoryname,
                'reported_dt': case_date,
                'agencyid': agency_name,
                'addressline1': casedetail.address_line1,
                'city': casedetail.city,
                'state': state_name,
                'zipcode': casedetail.zipcode,
                'priority': priority_level
            }
            casedetails_json.append(casedetail_json)

        session.close()
        return casedetails_json


    def fetch_ignored_reports(self, user_id):
        
        engine = create_engine(self.SQL_Alchemy_URI)
        print("SQL_Alchemy_URI  - " + self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        casedetails_ids = [row.case_id for row in session.query(Report.case_id).all()]
        print(casedetails_ids)
        print(set(casedetails_ids))
        case_ids_list = set(casedetails_ids)
        casedetails = session.query(CaseDetail).filter((CaseDetail.is_ignored == True) & (~CaseDetail.case_id.in_(set(case_ids_list)))).all()
        for casedetail in casedetails:
            print(casedetail.case_id)

        casedetails_json = []
        casedetails_agencymap = {}
        for casedetail in casedetails:
            category = session.query(Category).filter_by(category_id=casedetail.category_id).first()
            categoryname = None
            if category != None:
                categoryname = category.category_name

            user = 1
            publication_id = 1

            priority = session.query(Priority).filter_by(category_id=casedetail.category_id, publication_id = publication_id).first()
            priority_level = None
            if priority != None:
                priority_level = priority.priority

            state = session.query(State).filter_by(state_id = casedetail.state_id).first()
            state_name = None
            if state != None:
                state_name = state.usps_state_abbrrevation

            agency_details = session.query(Agency).filter_by(agency_id=casedetail.agency_id).first()
            agency_name = None
            if agency_details != None:
                agency_name = agency_details.agency_name

            case_date = None
            if casedetail.reported_dt != None:
                case_date = str(casedetail.reported_dt)


            casedetail_json = {
                'cid': casedetail.case_id,
                'case_description': casedetail.case_desc,
                'category': categoryname,
                'reported_dt': case_date,
                'agencyid': agency_name,
                'addressline1': casedetail.address_line1,
                'city': casedetail.city,
                'state': state_name,
                'zipcode': casedetail.zipcode,
                'priority': priority_level
            }
            casedetails_json.append(casedetail_json)

        session.close()
        return casedetails_json

    
    def publish_reports_to_vendor(self, caseid_list, user_id):
        print("Publish the un published reports to vendor")
        print(caseid_list)
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        casedetails = session.query(CaseDetail).filter(CaseDetail.case_id.in_(caseid_list)).all()
        max_report_id = session.query(func.max(Report.report_id)).scalar()
        if max_report_id is not None:
            new_report_id = max_report_id + 1
        else:
            new_report_id = 1
        crime_list = []
        report_list = []
        report_id_list = []

        for casedetail in casedetails:
            print(casedetail.case_id)
            report_sent_dt = str(datetime.datetime.now())

            user = 1
            publication_id = 1

            vendor_id = None
            publication_details = session.query(Publication).filter_by(publication_id=publication_id).first()
            if publication_details != None:
                vendor_id = publication_details.vendor_id

            agency_details = session.query(Agency).filter_by(agency_id=casedetail.agency_id).first()
            agency_name = None
            if agency_details != None:
                agency_name = agency_details.agency_name

            category_details = session.query(Category).filter_by(category_id=casedetail.category_id).first()
            category_name = None
            if category_details != None:
                category_name = category_details.category_name

            priority_level = None
            priority = session.query(Priority).filter_by(category_id=casedetail.category_id, publication_id = publication_id).first()
            if priority != None:
                priority_level = priority.priority

            state = session.query(State).filter_by(state_id = casedetail.state_id).first()
            usps_state_abbrrevation = None
            if state != None:
                usps_state_abbrrevation = state.usps_state_abbrrevation

            lat = None
            long = None
            if casedetail.latitude != None:
                lat = float(casedetail.latitude)
            if casedetail.longitude != None:
                long = float(casedetail.longitude)
            
            reported_dt = None
            if casedetail.reported_dt != None:
                reported_dt = str(casedetail.reported_dt)

            casedetail_json = {
                'upload_date': report_sent_dt,
                'publication_id': vendor_id,
                'report_id': new_report_id,
                'police_department': agency_name,
                'category': category_name,
                "priority": priority_level,
                "crime_datetime": reported_dt,
                "crime_location": [{
                    "addressline1": casedetail.address_line1,
                    "city": casedetail.city,
                    "state": usps_state_abbrrevation,
                    "zipcode": casedetail.zipcode,
                    "latitude": lat,
                    "longitude": long
                }],
                'persons': [{
                    "names": casedetail.names_involved,
                    "crime_reported": casedetail.case_desc
                }],
            }
            new_report = Report(
                report_id = new_report_id,
                report_dt=report_sent_dt,
                report_created_by_userid=casedetail.upload_userid,
                publication_id=publication_id,
                case_id=casedetail.case_id,
                report_sent_to_vender=True,
                report_sent_dt=report_sent_dt,
                report_sent_by_userid=user_id
            )
            report_list.append(new_report)
            crime_list.append(casedetail_json)
            report_id_list.append(new_report_id)
            new_report_id += 1

        json_output = {"crimelist" : crime_list}
        print(json_output)
        

        vendor = session.query(GeneralSetting).filter_by(gs_name= 'VENDOR_URI').first()
        print("Posting to vendor with Vendor URL " + vendor.gs_value)

        # Send the POST request with the payload
        response = requests.post(vendor.gs_value, json=json_output)
        print(response)

        # Check the response status code
        if response.status_code == 200:
            print("POST request successful!")
            print("Updating the report table")
            for report in report_list:
                print("Adding report with report id " + str(report.report_id))
                session.merge(report)
                session.commit()
        else:
            print("POST request failed.")

        session.close()
        return crime_list
    



    def add_cases_to_ignore_list(self, caseid_list, user_id):
        print("Marking the list of cases as ignored")
        print(caseid_list)
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()

        for case_id in caseid_list:
            case_detail = session.query(CaseDetail).filter_by(case_id=case_id).first()
            case_detail.is_ignored = True
            # Commit the changes to the database
            session.commit()

        session.close()




    def restore_cases_from_ignore_list(self, caseid_list, user_id):
        print("Restoring the case from ignore list")
        print(caseid_list)
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()

        for case_id in caseid_list:
            case_detail = session.query(CaseDetail).filter_by(case_id=case_id).first()
            case_detail.is_ignored = False
            # Commit the changes to the database
            session.commit()
        session.close()


        
