from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.parserdbcolumnmap import ParserColumnMap
from config import Config

class ParserMappingService:

    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME


    def update_parser_mappings(self, parser_id, agency_id, update_map):

        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        for item in update_map:
            parse_col_map = session.query(ParserColumnMap).filter_by(parser_id = parser_id, agency_id = agency_id, db_colname = update_map[item]).first()
            parse_col_map.parser_colname = item
            session.commit()
            session.close()
        return "Parser mappings updated successfully"


