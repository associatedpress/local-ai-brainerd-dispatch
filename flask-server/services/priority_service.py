from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.category import Category
from dbmappers.priority import Priority
from config import Config
import json

class PriorityService:

    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME
    

    def get_category_priority_list_by_publication(self, user_id, pub_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        category_list = session.query(Category).all()
        category_priority_json_list = []
        for category in category_list:
            priority = session.query(Priority).filter_by(publication_id = pub_id, category_id = category.category_id).first()
            if priority == None:
                category_priority_json = {
                    'category_id' : category.category_id,
                    'category_name' : category.category_name,
                    'priority_id' : None,
                    'priority': None
                }
            else:
                category_priority_json = {
                    'category_id' : category.category_id,
                    'category_name' : category.category_name,
                    'priority_id' : priority.priority_id,
                    'priority': priority.priority
                }
            category_priority_json_list.append(category_priority_json)
            print(str(category.category_id) + " " + category.category_name)
        session.close()
        return category_priority_json_list

    
    def add_priority_to_category(self, user_id, category_id, pub_id, priority):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        max_priority_id = session.query(func.max(Priority.priority_id)).scalar()
        if max_priority_id is not None:
            new_priority_id = max_priority_id + 1
        else:
            new_priority_id = 1
        new_priority = Priority(
        priority_id = new_priority_id, 
        publication_id = pub_id,
        category_id = category_id,
        priority = priority
        )
        session.add(new_priority)
        session.commit()
        session.close()
        priority_dict = {
            'priority_id': new_priority_id,
            'publication_id': pub_id,
            'category_id': category_id,
            'priority': priority
        }
        return json.dumps({'response': priority_dict}), 200
    

    def delete_priority(self, user_id, priority_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        priority_to_delete = session.query(Priority).filter_by(priority_id=priority_id).first()
        session.delete(priority_to_delete)
        session.commit()
        session.close()
        return json.dumps({'response': 'Deleted the priority successfully'}), 200 
