from db import db


class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    contact_info = db.Column(db.String(10), nullable=False)
    
    appointment_records = db.relationship("AppointmentRecordModel", back_populates="patient", lazy="dynamic", cascade="all, delete")
