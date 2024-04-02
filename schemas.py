from marshmallow import Schema, fields


class PlainDepartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    services = fields.Str(required=True)


class PlainDoctorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    specialization = fields.Str(required=True)
    contact_info = fields.Str(required=True)


class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    gender =fields.Str(required=True)
    contact_info = fields.Str(required=True)


class PlainAppointmentRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    date_time = fields.DateTime(required = True)
    #TODO - add constraints on values


class PlainMedicalHistorySchema(Schema):
    id = fields.Int(dump_only=True)
    diagnoses = fields.Str(required=True)
    allergies = fields.Str(required=True)
    medications = fields.Str(required=True)


class DepartmentSchema(PlainDepartmentSchema):
    doctors = fields.List(fields.Nested(PlainDoctorSchema()), dump_only=True)


class DoctorAppointmentRecordSchema(PlainAppointmentRecordSchema):
    patient = fields.Nested(PlainPatientSchema(), dump_only=True)


class DoctorSchema(PlainDoctorSchema):
    department_id = fields.Int(load_only=True)
    department = fields.Nested(PlainDepartmentSchema(), dump_only=True)
    appointment_records = fields.List(fields.Nested(DoctorAppointmentRecordSchema()), dump_only=True)


class PatientAppointmentRecordSchema(PlainAppointmentRecordSchema):
    medical_history = fields.Nested(PlainMedicalHistorySchema(), dump_only=True)
    doctor = fields.Nested(PlainDoctorSchema(), dump_only=True)


class PatientSchema(PlainPatientSchema):
    appointment_records = fields.List(fields.Nested(PatientAppointmentRecordSchema()), dump_only=True)


class AppointmentRecordSchema(PlainAppointmentRecordSchema):
    patient_id = fields.Int(load_only=True)
    patient = fields.Nested(PlainPatientSchema(), dump_only=True)
    doctor_id = fields.Int(required=True, load_only=True)
    doctor = fields.Nested(PlainDoctorSchema(), dump_only=True)
    medical_history = fields.Nested(PlainMedicalHistorySchema(), dump_only=True)


class MedicalHistorySchema(PlainMedicalHistorySchema):
    appointment_id = fields.Int(required=True, load_only=True)
    appointment_record = fields.Nested(AppointmentRecordSchema(), dump_only=True)


class DepartmentUpdateSchema(Schema):
    name = fields.Str()
    services = fields.Str()


class DoctorUpdateSchema(Schema):
    name = fields.Str()
    specialization = fields.Str()
    contact_info = fields.Str()
    department_id = fields.Int()


class PatientUpdateSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    gender =fields.Str()
    contact_info = fields.Str()


class AppointmentRecordUpdateSchema(Schema):
    date_time = fields.DateTime()
    patient_id = fields.Int()
    doctor_id = fields.Int()


class MedicalHistoryUpdateSchema(Schema):
    diagnoses = fields.Str()
    allergies = fields.Str()
    medications = fields.Str()
    appointment_id = fields.Int()