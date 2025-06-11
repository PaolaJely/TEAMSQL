
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not SECRET_KEY:
    print("⚠️ ERROR: SECRET_KEY no cargada desde .env")
if not OPENAI_API_KEY:
    print("⚠️ ERROR: OPENAI_API_KEY no cargada desde .env")
