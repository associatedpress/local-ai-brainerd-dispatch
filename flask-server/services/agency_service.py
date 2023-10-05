from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.agency import Agency
from dbmappers.state import State
from config import Config
import json

class AgencyService:

    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME


    def get_agencies_list(self, user_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        agency_list = session.query(Agency).all()
        agency_json_list = []
        for agency in agency_list:
            state = session.query(State).filter_by(state_id = agency.state_id).first()
            usps_state_abbrrevation = None
            if state != None:
                usps_state_abbrrevation = state.usps_state_abbrrevation
            agency_json = {
                'agency_id' : agency.agency_id,
                'agency_name' : agency.agency_name + ", " + agency.city + ", " + state.usps_state_abbrrevation , 
            }
            agency_json_list.append(agency_json)
            print(str(agency.agency_id) + " " + agency.agency_name + "  " + str(agency.parser_id))
        session.close()
        return agency_json_list
    

    def add_agency(self, user_id, agency_name, city, state, parser):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        max_agency_id = session.query(func.max(Agency.agency_id)).scalar()

        if max_agency_id is not None:
            new_agency_id = max_agency_id + 1
        else:
            new_agency_id = 1
        print(state)
        print(city)
        stateObj = session.query(State).filter_by(usps_state_abbrrevation = state).first()
        print(stateObj.state_id)
        new_agency = Agency(
        agency_id = new_agency_id, 
        agency_name = agency_name,
        parser_id = int(parser),
        city = city,
        state_id = int(stateObj.state_id)
        )
        agency_dict = {
            'agency_id': new_agency_id,
            'agency_name': agency_name,
            'parser_id': parser,
            'city': city,
            'state_id': str(stateObj.state_id)
        }
        session.add(new_agency)
        session.commit()
        session.close()
        
        return json.dumps({'response': agency_dict}), 200
    


    def delete_agency(self, agency_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        agency_to_delete = session.query(Agency).filter_by(agency_id=agency_id).first()
        session.delete(agency_to_delete)
        session.commit()
        session.close()
        return json.dumps({'response': 'Deleted the priority successfully'}), 200 
        
