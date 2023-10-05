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


class LoginService:


    def __init__(self):
        self.SQL_Alchemy_URI = 'mysql+pymysql://'+ Config.DB_USERNAME + ':' + Config.DB_PASSWORD + '@' + Config.DB_CONFIG + '/' + Config.DATABASE_NAME

    def get_user_info(self, username):
        engine = create_engine(self.SQL_Alchemy_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(user_name=username).first()
        session.close()
        return user
    
    def get_encrypted_password(self, password):
        # Encode the string to bytes
        data = password.encode()

        # Hash the data using SHA-512
        hash_object = hashlib.sha512(data)
        hex_dig = hash_object.hexdigest()

        return hex_dig
        # Print the hash value
        print(hex_dig)

