from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from db import db
from models.appointment_record import AppointmentRecordModel
from models.department import DepartmentModel
from models.doctor import DoctorModel
from schemas import DoctorAppointmentRecordSchema, DoctorSchema, DoctorUpdateSchema, PlainAppointmentRecordSchema


blp = Blueprint("Doctors", __name__, description="Operations on doctors")


@blp.route("/doctor")
class DoctorList(MethodView):
    @blp.response(200, DoctorSchema(many=True))
    def get(self):
        return DoctorModel.query.all()

    @blp.arguments(DoctorSchema)
    @blp.response(201, DoctorSchema)
    def post(self, doctor_data):

        # Additional check because SQLITE doesn't enforce Foreign Key Constraints
        department = DepartmentModel.query.get(doctor_data["department_id"])
        if department is None:
            abort(
                404, 
                message= "Department with department id {} does not exists.".format(doctor_data["department_id"])
            )

        doctor = DoctorModel(**doctor_data)

        try:
            db.session.add(doctor)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A doctor with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while entering the doctor record."
            )

        return doctor
    

@blp.route("/doctor/<string:doctor_id>")
class Doctor(MethodView):
    @blp.response(200, DoctorSchema)
    def get(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        return doctor

    def delete(self, doctor_id):
        doctor = DoctorModel.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {"message": "Doctor deleted."}
    
    @blp.arguments(DoctorUpdateSchema)
    @blp.response(200, DoctorSchema)
    def put(self, doctor_data, doctor_id):
        
        if doctor_data.get("department_id"):
            # Additional check because SQLITE doesn't enforce Foreign Key Constraints
            department = DepartmentModel.query.get(doctor_data["department_id"])
            if department is None:
                abort(
                    404, 
                    message= "Department with department id {} does not exists.".format(doctor_data["department_id"])
                )

        doctor = DoctorModel.query.get(doctor_id)
        
        if doctor:
            if doctor_data.get("name"):
                doctor.name = doctor_data["name"]
            if doctor_data.get("specialization"):
                doctor.specialization = doctor_data["specialization"]
            if doctor_data.get("contact_info"):
                doctor.contact_info = doctor_data["contact_info"]
            if doctor_data.get("department_id"):
                doctor.department_id = department.id
        
        else:

            doctor = DoctorModel(id=doctor_id, **doctor_data)

        try:
            db.session.add(doctor)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A doctor with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while updating the doctor record."
            )

        return doctor
    

@blp.route("/doctor/<string:doctor_id>/availability")
class DoctorAvailability(MethodView):
    
    @blp.response(200, PlainAppointmentRecordSchema(many=True))
    def get(self,doctor_id):
        results = AppointmentRecordModel.query.filter(
            AppointmentRecordModel.date_time >= datetime.now() ,
            AppointmentRecordModel.doctor_id == doctor_id,
            AppointmentRecordModel.patient_id == None,       
        ).all()
        return results
    

@blp.route("/doctor/<string:doctor_id>/patients")
class DoctorAvailability(MethodView):
    @blp.response(200, DoctorAppointmentRecordSchema(many=True))
    def get(self,doctor_id):
        results = AppointmentRecordModel.query.filter(
            AppointmentRecordModel.doctor_id == doctor_id,
            AppointmentRecordModel.patient_id != None,     
        ).all()
        return results