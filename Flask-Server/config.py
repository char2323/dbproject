import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-default-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None
    APPKEY = os.environ.get('APPKEY')
    APPSECRET = os.environ.get('APPSECRET')
    ADMIN = (os.environ.get('ADMIN_USERNAME'), os.environ.get('ADMIN_PASSWORD'))
    MAILSERVER = os.environ.get('MAILSERVER')
    MAILKEY = os.environ.get('MAILKEY')
