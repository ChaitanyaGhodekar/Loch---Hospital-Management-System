from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models.patient import PatientModel
from schemas import PatientSchema, PatientUpdateSchema


blp = Blueprint("Patients", __name__, description="Operations on patients")


@blp.route("/patient")
class PatientList(MethodView):
    @blp.response(200, PatientSchema(many=True))
    def get(self):
        return PatientModel.query.all()

    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    def post(self, patient_data):
        patient = PatientModel(**patient_data)

        try:
            db.session.add(patient)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A patient with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while entering the patient record."
            )

        return patient


@blp.route("/patient/<string:patient_id>")
class Patient(MethodView):
    @blp.response(200, PatientSchema)
    def get(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        return patient

    def delete(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted."}
    
    @blp.arguments(PatientUpdateSchema)
    @blp.response(200, PatientSchema)
    def put(self, patient_data, patient_id):
        patient = PatientModel.query.get(patient_id)
        if patient:
            if patient_data.get("name"):
                patient.name = patient_data["name"]
            if patient_data.get("age"):
                patient.age = patient_data["age"]
            if patient_data.get("gender"):
                patient.gender = patient_data["gender"]
            if patient_data.get("contact_info"):
                patient.contact_info = patient_data["contact_info"]
        else:
            patient = PatientModel(id=patient_id, **patient_data)

        try:
            db.session.add(patient)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A patient with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while updating the patient record."
            )

        return patient
