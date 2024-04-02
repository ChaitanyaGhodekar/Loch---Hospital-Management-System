from db import db


class DepartmentModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    services = db.Column(db.Text, nullable=False)

    doctors = db.relationship("DoctorModel", back_populates="department", lazy="dynamic")
