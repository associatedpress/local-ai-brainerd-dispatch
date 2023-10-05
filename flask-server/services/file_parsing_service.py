
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.casedetail import CaseDetail
from config import Config
import datetime, time
from parsers.brainerd_parser import BrainerdParser
from parsers.casscounty_parser import CassParser
from dbmappers.agency import Agency
from dbmappers.state import State
from dbmappers.user import User
from dbmappers.category import Category
from dbmappers.parserdbcolumnmap import ParserColumnMap
import pandas as pd
import math
import os
import json


class ParseFile:
    def __init__(self, filepath, agencyid, userid):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.agencyid = agencyid
        self.userid = userid
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME

    def parsefile(self):    
        print("SQL_Alchemy_URI  - " + self.SQL_Alchemy_URI)
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Created DB session")
        max_cid = session.query(func.max(CaseDetail.case_id)).scalar()
        if max_cid is not None:
            new_cid = max_cid + 1
        else:
            new_cid = 1
        print(type(max_cid))
        print(max_cid)

        print("file path : " + self.filepath)
        print("agency : " + self.agencyid)

        agency = session.query(Agency).filter_by(agency_id=int(self.agencyid)).first()
        agency_id = agency.agency_id

        parser_col_map_list = None
        if agency.parser_id == 1:
            parser = BrainerdParser()
            parser_col_map_list = session.query(ParserColumnMap).filter_by(parser_id=agency.parser_id).all()
        elif agency.parser_id == 2:
            parser = CassParser()
        # In the future, this mapping will need to be a pull from the database's PARSER table rather than hardcoding a parser ID to a python function.

        
        dataframe = parser.parse(self.filepath)#parser.parse(self.filepath, parser_col_map_list)

        if isinstance(dataframe, pd.DataFrame):
            print("Response is instance of dataframe")
            pass
        else:  
            print(dataframe)             
            return json.dumps({'response': dataframe}), 500

        for index, row in dataframe.iterrows():
            casenum = row['caseno']
            casename = row['case']

            print(casename)
            category = None
            if casename != None:
                category = session.query(Category).filter(Category.category_name.ilike('%'+casename.strip()+'%')).first()
            categoryid = None
            if category != None:
                categoryid = category.category_id
            else:
                if casename != None:
                    print("case name not found -- " + casename)
                #Point this to others type dynamically
                categoryid = 78

            casedesc = row['Desc']
            officers = None
            names = None
            try:
                if row['Officers Involved'] != None and pd.isnull(row['Officers Involved']) == False:
                    officers = row['Officers Involved']
            except Exception:
                pass
            
            try:
                if row['Names Involved'] != None and pd.isnull(row['Names Involved']) == False:
                    names = row['Names Involved']
            except Exception:
                pass  

            lati = None
            longi = None
            try:
                if row['lat'] != None and pd.isnull(row['lat']) == False:
                    lati = row['lat']
            except Exception:
                pass
            
            try:
                if row['long'] != None and pd.isnull(row['long']) == False:
                    longi = row['long']
            except Exception:
                pass         

            reported_dt = None
            my_date = None
            my_time = None
            date_arr0 = None
            date_arr1 = None
            date_arr2 = None

            row_date = None
            row_time = None
            try :
                if row['date'] != None and pd.isnull(row['date']) == False:
                    row_date = row['date']
                    print("date")
                    print(row_date)
            except:
                pass
            
            try :
                if row['time'] != None and pd.isnull(row['time']) == False:
                    row_time = row['time']
                    print("time")
                    print(row_time)
            except:
                pass
            
            if row_date != None :
                date_arr = None
                print(str(row_date))
                if '-' in str(row_date):
                    date_arr = str(row_date).split('-')
                elif '/' in str(row_date):
                    date_arr = str(row_date).split('/')
                try :
                    if date_arr[0] != None:
                        date_arr0 = date_arr[0].strip()
                    if date_arr[1] != None:
                        date_arr1 = date_arr[1].strip()
                    if date_arr[2] != None:
                        date_arr2 = date_arr[2].strip()
                except Exception:
                    pass
                if date_arr0 != None and date_arr1 != None and date_arr2 != None:
                    if str(date_arr0).isnumeric() and str(date_arr1).isnumeric() and str(date_arr2).isnumeric(): 
                        my_date = datetime.date(int(date_arr[2]), int(date_arr[0]), int(date_arr[1]))
            
            time_arr = ['00', '00']
            if row_time != None :
                if str(row_time) != None:
                    if str(row_time)[:2].isnumeric() and str(row_time)[2:4].isnumeric():
                        time_arr = [str(row_time)[:2], str(row_time)[2:4]]
            my_time = datetime.time(int(time_arr[0]), int(time_arr[1]))

            if my_date != None:
                reported_dt = datetime.datetime.combine(my_date, my_time)
            address1 = str(row['address1'])

            state = None
            zipcode = None
            state_abbr = None
            print(row['state'])
            zipcode_con = ""
            if type(row['state']) == str and len(row['state'].strip()) >= 2:
                statename = row['state'].strip()
                for char in statename:
                    if char.isnumeric():
                        zipcode_con += char
                state_abbr = row['state'].strip()[:2]
                state= session.query(State).filter_by(usps_state_abbrrevation=state_abbr).first()
            elif type(row['state']) == str and len(row['state'].strip()) == 2:
                state_abbr = row['state'].strip()
                state= session.query(State).filter_by(usps_state_abbrrevation=state_abbr).first()

            stateid = None
            if state != None:
                stateid  = state.state_id
            city = str(row['city']).strip()

            #Get the zip from parsed text once column updates
            if len(str(row['zipcode']).strip()) > 0:
                zipcode = str(row['zipcode']).strip()
            
            if zipcode != None:
                print("zipcode : " + zipcode)

            userid = self.userid#user.user_id
        
            new_case = CaseDetail(
            case_id = new_cid + index,
            case_number=casenum,
            case_desc=casedesc,
            category_id=categoryid,
            reported_dt=reported_dt,
            names_involved=names,
            officers_involved=officers,
            agency_id=agency_id,
            latitude=lati,
            longitude=longi,
            address_line1=address1,
            city=city,
            zipcode=zipcode,
            state_id=stateid,
            resoource_id = self.filename,
            upload_userid=userid,   
            upload_dt=datetime.datetime.now(),
            is_ignored = False
            )

            session.add(new_case)
            session.commit()
        session.close()
        return json.dumps({'response': 'File parsed successfully'}), 200




