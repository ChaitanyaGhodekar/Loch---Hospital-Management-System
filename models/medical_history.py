from db import db

class MedicalHistoryModel(db.Model):
    __tablename__ = "medicalhistory"

    id = db.Column(db.Integer, primary_key=True)
    diagnoses = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    medications = db.Column(db.Text, nullable=False)
    
    appointment_id = db.Column(
        db.Integer, db.ForeignKey("appointment_records.id"), unique=True, nullable=False
    )
    appointment_record = db.relationship("AppointmentRecordModel", back_populates="medical_history", uselist = False)