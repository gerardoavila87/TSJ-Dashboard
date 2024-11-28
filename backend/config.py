import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', 'password')}"
        f"@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DATA_DB_NAME', 'school_dashboard')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
