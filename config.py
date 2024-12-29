# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('password') or "password"
    SQLALCHEMY_DATABASE_URI = 'postgresql://system_db:password@localhost/system_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
