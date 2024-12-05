from flask import Flask
from services.total_service import gender_service
from services.total_service import total_service
from services.total_service import mode_service
from services.total_service import status_service
from services.total_service import unidad_service
from services.total_service import procedencia_service

from services.csv_service import csv_service

app = Flask(__name__)

# Registrar los Blueprints (modularización de rutas)
app.register_blueprint(gender_service, url_prefix="/data")
app.register_blueprint(total_service, url_prefix="/data")
app.register_blueprint(mode_service, url_prefix="/data")
app.register_blueprint(status_service, url_prefix="/data")
app.register_blueprint(unidad_service, url_prefix="/data")
app.register_blueprint(procedencia_service, url_prefix="/data")

app.register_blueprint(csv_service, url_prefix="/csv")

if __name__ == "__main__":
    app.run(debug=True, port=5010)
