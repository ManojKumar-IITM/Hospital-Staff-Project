from  .database import db




class Members(db.Model):
    __tablename__  = 'Members'
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name= db.Column(db.Text)
    last_name = db.Column(db.Text)
    username  = db.Column(db.Text   , nullable  =False)
    password  = db.Column(db.Text   , nullable  =False)
    role      = db.Column(db.Text   , nullable  =False)







    
    


    