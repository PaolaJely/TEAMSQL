import mysql.connector
from flask import g
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def init_db(app):
    @app.before_request
    def before_request():
        g.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        g.cursor = g.db.cursor(dictionary=True)

    @app.teardown_request
    def teardown_request(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()
