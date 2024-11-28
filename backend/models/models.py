from main import db

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    unit_academic = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Active, Dropped, etc.

    def __repr__(self):
        return f"<Enrollment {self.student_id}>"
