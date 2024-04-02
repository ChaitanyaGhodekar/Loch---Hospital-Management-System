from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from db import db
from models.appointment_record import AppointmentRecordModel

from models.doctor import DoctorModel
from models.patient import PatientModel
from schemas import AppointmentRecordSchema, AppointmentRecordUpdateSchema


blp = Blueprint("AppointmentRecords", __name__, description="Operations on appointment records")


@blp.route("/appointment-record")
class AppointmentRecords(MethodView):
    @blp.response(200, AppointmentRecordSchema(many=True))
    def get(self):
        return AppointmentRecordModel.query.all()

    @blp.arguments(AppointmentRecordSchema)
    @blp.response(201, AppointmentRecordSchema)
    def post(self, appointment_record_data):

        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        doctor = DoctorModel.query.get(appointment_record_data["doctor_id"])
        if doctor is None:
            abort(
                404, 
                message= "Doctor with doctor id {} does not exists.".format(appointment_record_data["doctor_id"])
            )
        
        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        if appointment_record_data.get("patient_id"):
            patient = PatientModel.query.get(appointment_record_data["patient_id"])
            if patient is None:
                abort(
                    404, 
                    message= "Patient with patient id {} does not exists.".format(appointment_record_data["patient_id"])
                )

        appointment_record = AppointmentRecordModel(**appointment_record_data)

        try:
            db.session.add(appointment_record)
            db.session.commit()
        except IntegrityError as e:
            abort(
                400,
                message="Appointment Record for the same date & time already exists for either the patient or the doctor"
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while creating the Appointment Record."
            )


        return appointment_record
    

@blp.route("/appointment-record/<string:appointment_record_id>")
class AppointmentRecord(MethodView):
    @blp.response(200, AppointmentRecordSchema)
    def get(self, appointment_record_id):
        appointment_record = AppointmentRecordModel.query.get_or_404(appointment_record_id)
        return appointment_record

    def delete(self, appointment_record_id):
        appointment_record = AppointmentRecordModel.query.get_or_404(appointment_record_id)
        db.session.delete(appointment_record)
        db.session.commit()
        return {"message": "Appointment Record deleted."}
    
    @blp.arguments(AppointmentRecordUpdateSchema)
    @blp.response(200, AppointmentRecordSchema)
    def put(self, appointment_record_data, appointment_record_id):
        
        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        if appointment_record_data.get("doctor_id"):
            doctor = DoctorModel.query.get(appointment_record_data["doctor_id"])
            if doctor is None:
                abort(
                    404, 
                    message= "No doctor corresponding to doctor id {} exists.".format(appointment_record_data["doctor_id"])
                )
        
        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        if appointment_record_data.get("patient_id"):
            patient = PatientModel.query.get(appointment_record_data["patient_id"])
            if patient is None:
                abort(
                    404, 
                    message= "No patient corresponding to patient id {} exists.".format(appointment_record_data["patient_id"])
                )

        appointment_record = AppointmentRecordModel.query.get(appointment_record_id)
        
        if appointment_record:
            if appointment_record_data.get("date_time"):
                appointment_record.date_time = appointment_record_data["date_time"]
            if appointment_record_data.get("doctor_id"):
                appointment_record.doctor_id = doctor.id
            if appointment_record_data.get("patient_id"):
                appointment_record.patient_id = patient.id

        else:
            
            appointment_record = AppointmentRecordModel(id=appointment_record_id, **appointment_record_data)

        try:
            db.session.add(appointment_record)
            db.session.commit()
        except IntegrityError as e:
            abort(
                400,
                message="Appointment Record for the same date & time already exists for either the patient or the doctor"
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while updating the Appointment Record."
            )

        return appointment_record