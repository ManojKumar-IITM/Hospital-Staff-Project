from  .database import db


class Admin(db.Model):
    __tablename__  = 'Admin'
    id       = db.Column(db.Integer, primary_key=True  , autoincrement=True )
    username = db.Column(db.Text   , nullable  =False )
    password = db.Column(db.Text   , nullable  =False )
    email    = db.Column(db.Text   , unique    =True  )


class Patients(db.Model):
    __tablename__  = 'Patients'
    id        = db.Column(db.Integer, primary_key=True   , autoincrement=True )
    first_name= db.Column(db.Text   , nullable  =False )
    last_name = db.Column(db.Text   , nullable  =False )
    username  = db.Column(db.Text   , nullable  =False )
    password  = db.Column(db.Text   , nullable  =False )


class Doctors(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text   , nullable  =False )
    password = db.Column(db.Text   , nullable  =False )
    email    = db.Column(db.Text   , unique    =True  )



    
    


    