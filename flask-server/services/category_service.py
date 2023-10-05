from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dbmappers.category import Category
from config import Config
import json

class CategoryService:

    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME


    def get_categories_list(self, user_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        category_list = session.query(Category).all()
        category_json_list = []
        for category in category_list:
            category_json = {
                'category_id' : category.category_id,
                'category_name' : category.category_name
            }
            category_json_list.append(category_json)
            print(str(category.category_id) + " " + category.category_name)
        session.close()
        return category_json_list
    
    def add_category(self, user_id, category_name):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        category = session.query(Category).filter(Category.category_name.ilike('%'+category_name.strip()+'%')).first()
        if category != None:
            session.close
            return json.dumps({'response': 'Category already exists'}), 409
        max_category_id = session.query(func.max(Category.category_id)).scalar()
        if max_category_id is not None:
            new_category_id = max_category_id + 1
        else:
            new_category_id = 1
        new_category = Category(
        category_id = new_category_id, 
        category_name = category_name
        )
        session.add(new_category)
        session.commit()
        session.close()
        category_dict = {
            'category_id': new_category_id,
            'category_name': category_name
        }
        return json.dumps({'response': category_dict}), 200
    
    def delete_category(self, user_id, category_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        category_to_delete = session.query(Category).filter_by(category_id=category_id).first()
        session.delete(category_to_delete)
        session.commit()
        session.close()
        return json.dumps({'response': 'Deleted the category successfully'}), 200 
    

   