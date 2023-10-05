from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.agency import Agency
from dbmappers.state import State
from dbmappers.userpublication import UserPublication
from dbmappers.publication import Publication
from config import Config

class GenericService:

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
    

    def get_publications_list(self, user_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        publication_ids = [row.publication_id for row in session.query(UserPublication.publication_id).all()]
        print("Publication Ids ")
        print(publication_ids)
        publication_list = session.query(Publication).filter(Publication.publication_id.in_(publication_ids)).all()
        publication_json_list = []
        for publication in publication_list:
            state = session.query(State).filter_by(state_id = publication.state_id).first()
            usps_state_abbrrevation = None
            if state != None:
                usps_state_abbrrevation = state.usps_state_abbrrevation
            publication_json = {
                'publication_id' : publication.publication_id,
                'publication_name' : publication.publication_name,
                'city' : publication.city,
                'state_usps_abbrrevation' : usps_state_abbrrevation,
                'vendor_id' : publication.vendor_id
            }
            publication_json_list.append(publication_json)
            print(str(publication.publication_id) + " " + publication.publication_name)
        session.close()
        return publication_json_list
    
