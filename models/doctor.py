from db import db


class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    specialization = db.Column(db.String(80), nullable=False)
    contact_info = db.Column(db.String(10), nullable=False)

    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id")
    ) 
    department = db.relationship("DepartmentModel", back_populates = "doctors")
    
    appointment_records = db.relationship("AppointmentRecordModel", back_populates="doctor", lazy="dynamic", cascade = "all, delete")