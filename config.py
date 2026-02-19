import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'superseceretkeyforchatrooms'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chat_rooms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
