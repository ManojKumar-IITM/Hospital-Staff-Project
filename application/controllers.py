from flask import Flask,request,render_template,Blueprint,flash,redirect,url_for
from .models import Patients,Admin,Doctors
from .database import db





controllers = Blueprint('controllers', __name__)

# @controllers.route('/',method=['GET','POST'])
# def home():
#     if request.method=='GET':
#         return render_template('index.html')
#     elif request.method=='POST':

@controllers.route('/',methods=['GET','POST'])
def login():
    if request.method =='GET':
      return render_template('login.html')
    
    elif request.method=='POST':
        username= request.form.get('username')
        password= request.form.get('password')
        # return f'hello {username}'

        user = Admin.query.filter_by(username=username).first()
        if user and user.password == password:
            return render_template('Admin.html', username=user.username)

        user = Doctors.query.filter_by(username=username).first()
        if user and user.password == password:
            return render_template('doctor.html', username=user.username)

        user = Patients.query.filter_by(username=username).first()
        if user and user.password == password:
            return render_template('patient.html', username=user.username)

        # Note: do NOT reveal which type failed, for security
        flash('Invalid username or password','danger')
        return render_template('login.html')
        

@controllers.route('/signup' , methods = ["GET","POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method =="POST":
        firstname= request.form.get('firstname')
        lastname=  request.form.get('lastname')
        username=  request.form.get('username')
        password=  request.form.get('password')

        new_patient = Patients(
                             username=username,
                             password=password,
                             first_name=firstname,
                             last_name=lastname
        )
        try:
            db.session.add(new_patient)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('AN error occurred:' + str(e), 'error')
            return render_template('signup.html')


        flash("Signup Succesfull",'succes')
        return redirect(url_for('controllers.login'))
       


