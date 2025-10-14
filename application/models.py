from  .database import db
from datetime import datetime, date, time
from sqlalchemy import Column,Date ,Time




class Members(db.Model):
    __tablename__  = 'Members'
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name= db.Column(db.Text)
    last_name = db.Column(db.Text)
    username  = db.Column(db.Text   , nullable  =False)
    password  = db.Column(db.Text   , nullable  =False)
    role      = db.Column(db.Text   , nullable  =False)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }

class Appointments (db.Model):
    __tablename__ = "Appointments"
    appointment_id = db.Column(db.Integer , primary_key=True, autoincrement=True)  
    patient_id=      db.Column(db.Integer ,db.ForeignKey('Members.id'),nullable=False)
    doctor_id =      db.Column(db.Integer ,db.ForeignKey('Members.id'),nullable=False)
    date  =          db.Column(Date, default=date.today)
    time   =         db.Column(Time, default=lambda: datetime.now().time())
    status =         db.Column(db.Text)
    doctor =         db.relationship(Members,foreign_keys=[doctor_id],backref='doctor_appointments')
    patient =        db.relationship(Members,foreign_keys=[patient_id], backref='patient_appointments')
    department =     db.relationship('Department', primaryjoin='foreign(Appointments.doctor_id)==Department.doctor_id',uselist=False)

    def serialize(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.isoformat() if self.time else None,
            "status": self.status,
            "doctor": self.doctor.serialize() if self.doctor else None,
            "patient": self.patient.serialize() if self.patient else None,
        }

class Treatment (db.Model):
    __tablename__ = "Treatment"
    appointment_id = db.Column(db.Integer , db.ForeignKey('Appointments.appointment_id'), primary_key=True)
    patient_id    =  db.Column(db.Integer,  db.ForeignKey('Members.id'),     primary_key=True)
    diagnosis =      db.Column(db.Text)
    prescription =   db.Column(db.Text)
    notes =          db.Column(db.Text)
    visittype=       db.Column(db.Text)
    testdone =       db.Column(db.Text)
    patient  =       db.relationship('Members',backref='patient_treatment')

    def serialize(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "notes": self.notes,
            "visittype": self.visittype,
            "testdone": self.testdone,
        }


class Department (db.Model):
    __tablename__ = 'Department'
    department_id =  db.Column(db.Integer)
    department_name= db.Column(db.Text,nullable=False)
    description =    db.Column(db.Text)
    doctor_id =      db.Column(db.Integer,  db.ForeignKey('Members.id') ,primary_key=True)
    doctor=          db.relationship('Members',backref='doctor_department')

    def serialize(self):
        return {
            "department_id": self.department_id,
            "department_name": self.department_name,
            "description": self.description,
            "doctor_id": self.doctor_id,
            "doctor": self.doctor.serialize() if self.doctor else None
        }




    
    


    