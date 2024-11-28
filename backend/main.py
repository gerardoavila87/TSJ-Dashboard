# backend/main.py
from app import create_app, db
from routes.students import students_bp

app = create_app()

# Registrar el Blueprint
app.register_blueprint(students_bp)

# Test endpoint
@app.route("/")
def home():
    return {"message": "API is running"}

if __name__ == "__main__":
    app.run(debug=True)
