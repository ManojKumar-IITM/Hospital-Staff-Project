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

class Appointments (db.Model):
    __tablename__ = "Appointments"
    appointment_id = db.Column(db.Integer , primary_key=True, autoincrement=True)  
    patient_id= db.Column(db.Integer ,db.ForeignKey('Members.id'),nullable=False)
    doctor_id = db.Column(db.Integer ,db.ForeignKey('Members.id'),nullable=False)
    date  =     db.Column(Date, default=date.today)
    time   =    db.Column(Time, default=lambda: datetime.now().time())
    status =    db.Column(db.Text)
    doctor =    db.relationship(Members,foreign_keys=[doctor_id],backref='doctor_appointments')
    patient =   db.relationship(Members,foreign_keys=[patient_id], backref='patient_appointments')



    
    


    