from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models.appointment_record import AppointmentRecordModel
from models.medical_history import MedicalHistoryModel
from schemas import MedicalHistorySchema, MedicalHistoryUpdateSchema


blp = Blueprint("MedicalHistory", __name__, description="Operations on medical history")


@blp.route("/medical-history")
class MedicalHistory(MethodView):
    @blp.response(200, MedicalHistorySchema(many=True))
    def get(self):
        return MedicalHistoryModel.query.all()

    @blp.arguments(MedicalHistorySchema)
    @blp.response(201, MedicalHistorySchema)
    def post(self, medical_history_data):
        
        appointment_record =  AppointmentRecordModel.query.get(medical_history_data["appointment_id"])
        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        if appointment_record is None:
            abort(
                404, 
                message= "Appointment Record with appointment id {} does not exists.".format(medical_history_data["appointment_id"])
            )

        # Assumption: Medical History is only recorded on a scheduled appointment by patient
        # Additional check to ensure appointment record has a patient associated to create the medical history for
        if appointment_record.patient is None:
            abort(
                400,
                message="Appoinment Record is not assigned to a patient."
            )


        # Additional check to ensure medical history for a present or past record is being created
        if appointment_record.date_time > datetime.now():
            abort(
                400,
                message="Trying to set medical history for a future appointment."
            )
            
        medical_history = MedicalHistoryModel(**medical_history_data)

        try:
            db.session.add(medical_history)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Medical Histroy for the appointment id already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while creating the Medical History record."
            )

        return medical_history


@blp.route("/medical-history/<string:medical_history_id>")
class MedicalHistory(MethodView):
    @blp.response(200, MedicalHistorySchema)
    def get(self, medical_history_id):
        medical_history = MedicalHistoryModel.query.get_or_404(medical_history_id)
        return medical_history

    def delete(self, medical_history_id):
        medical_history = MedicalHistoryModel.query.get_or_404(medical_history_id)
        db.session.delete(medical_history)
        db.session.commit()
        return {"message": "Medical History deleted."}
    
    @blp.arguments(MedicalHistoryUpdateSchema)
    @blp.response(200, MedicalHistorySchema)
    def put(self, medical_history_data, medical_history_id):
        
        if medical_history_data.get("appointment_id"):
            appointment_record = AppointmentRecordModel.query.get(medical_history_data["appointment_id"])
            # Additional check because SQLITE doesn't enforce Foreign Key Constraints
            if appointment_record is None:
                abort(
                    404, 
                    message= "Appointment Record with appointment id {} does not exists.".format(medical_history_data["appointment_id"])
                )
            
            # Assumption: Medical History is only recorded on a scheduled appointment by patient
            # Additional check to ensure appointment record has a patient associated to create the medical history for
            if appointment_record.patient is None:
                abort(
                    400,
                    message="Appoinment Record is not assigned to a patient."
                )
            
            # Additional check to ensure medical history for a present or past record is being created
            if appointment_record.date_time > datetime.now():
                abort(
                    400,
                    message="Trying to set medical history for a future appointment."
                )
        
        medical_history = MedicalHistoryModel.query.get(medical_history_id)
        
        if medical_history:
            if medical_history_data.get("appointment_id"):
                medical_history.appointment_id = appointment_record.id
            if medical_history_data.get("diagnoses"):
                medical_history.diagnoses = medical_history_data["diagnoses"]
            if medical_history_data.get("allergies"):
                medical_history.allergies = medical_history_data["allergies"]
            if medical_history_data.get("medications"):
                medical_history.medications = medical_history_data["medications"]
                        
        else:
        
            medical_history = MedicalHistoryModel(id=medical_history_id, **medical_history_data)

        try:
            db.session.add(medical_history)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Medical History with that appointment id already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while updating the Medical History record."
            )

        return medical_history