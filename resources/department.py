from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models.department import DepartmentModel
from schemas import DepartmentSchema, DepartmentUpdateSchema


blp = Blueprint("Departments", __name__, description="Operations on departments")


@blp.route("/department")
class DepartmentList(MethodView):
    @blp.response(200, DepartmentSchema(many=True))
    def get(self):
        return DepartmentModel.query.all()

    @blp.arguments(DepartmentSchema)
    @blp.response(201, DepartmentSchema)
    def post(self, department_data):
        department = DepartmentModel(**department_data)

        try:
            db.session.add(department)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A department with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while creating the department record."
            )

        return department
    

@blp.route("/department/<string:department_id>")
class Department(MethodView):
    @blp.response(200, DepartmentSchema)
    def get(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        return department

    def delete(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        db.session.delete(department)
        db.session.commit()
        return {"message": "Department deleted"}, 200

    
    @blp.arguments(DepartmentUpdateSchema)
    @blp.response(200, DepartmentSchema)
    def put(self, department_data, department_id):
        department = DepartmentModel.query.get(department_id)
        if department:
            if department_data.get("name"):
                department.name = department_data["name"]
            if department_data.get("services"):
                department.services = department_data["services"]
        else:
            department = DepartmentModel(id=department_id, **department_data)

        try:
            db.session.add(department)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A department with that name already exists.",
            )
        except SQLAlchemyError as e:
            print(str(e)) #For production log this data
            abort(
                500, 
                message="An error occured while updating the department record."
            )

        return department