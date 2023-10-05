from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from threading import Thread
import pika
import os
from datetime import datetime
from pytz import timezone
from config import Config
from dbmappers.user import User
import json
import hashlib


class UserService:


    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME
    
    def get_encrypted_password(self, password):
        # Encode the string to bytes
        data = password.encode()

        # Hash the data using SHA-512
        hash_object = hashlib.sha512(data)
        hex_dig = hash_object.hexdigest()

        return hex_dig
        # Print the hash value
        print(hex_dig)


    def get_user_list(self):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        user_list = session.query(User).all()
        user_json_list = []
        for user in user_list:
            user_json = {
                'user_id' : user.user_id,
                'user_name' : user.user_name , 
                'user_password' : user.user_password,
                'user_firstname' : user.user_firstname,
                'user_lastname' : user.user_lastname
            }
            user_json_list.append(user_json)
            print(user_json)
        session.close()
        return user_json_list


    def add_user(self, user_name, user_password, user_firstname, user_lastname):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        max_user_id = session.query(func.max(User.user_id)).scalar()

        if max_user_id is not None:
            new_user_id = max_user_id + 1
        else:
            new_user_id = 1
        encrypted_password = self.get_encrypted_password(user_password)
        new_user = User(
        user_id = new_user_id, 
        user_name = user_name,
        user_password = encrypted_password,
        user_firstname = user_firstname,
        user_lastname = user_lastname
        )
        user_dict = {
            'user_id': new_user_id,
            'user_name': user_name,
            'user_firstname': user_firstname,
            'user_lastname': user_lastname
        }
        session.add(new_user)
        session.commit()
        session.close()
        
        return json.dumps({'response': user_dict}), 200


    def delete_user(self, user_id):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        user_to_delete = session.query(User).filter_by(user_id=user_id).first()
        session.delete(user_to_delete)
        session.commit()
        session.close()
        return json.dumps({'response': 'Deleted the user successfully'}), 200 
