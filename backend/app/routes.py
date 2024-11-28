from flask_restful import Resource, Api
from main import app, db
from backend.models.models import Enrollment

api = Api(app)

class EnrollmentAPI(Resource):
    def get(self):
        enrollments = Enrollment.query.all()
        return [{"id": e.id, "student_id": e.student_id, "unit_academic": e.unit_academic,
                 "period": e.period, "status": e.status} for e in enrollments], 200

    def post(self):
        # Aquí puedes agregar lógica para recibir datos JSON y guardarlos
        pass

api.add_resource(EnrollmentAPI, "/api/enrollments")
