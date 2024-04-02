from db import db
from sqlalchemy import UniqueConstraint

class AppointmentRecordModel(db.Model):
    __tablename__ = "appointment_records"
    # doctor cannot have multiple appointments for same time
    # Similarly patient cannot have multiple appointments for same time
    __table_args__= (
        UniqueConstraint('doctor_id', "date_time",  name='_doctor_time_uc'),
        UniqueConstraint('patient_id', "date_time",  name='_patient_time_uc'),
    )

    id = db.Column(db.Integer, primary_key=True)
    #TODO enum here
    date_time = db.Column(db.DateTime, nullable=False)
    #AppointmentRecord cannot be created without a doctor assigned to it
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    #AppointmentRecord having no patient id associated is a free slot(appointmment available)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    
    doctor = db.relationship("DoctorModel", back_populates="appointment_records")
    patient = db.relationship("PatientModel", back_populates="appointment_records")

    medical_history = db.relationship("MedicalHistoryModel", back_populates="appointment_record", uselist=False, cascade="all, delete")