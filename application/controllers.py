from flask import Flask,request,render_template,Blueprint
from .models import Patients
from .database import db





controllers = Blueprint('controllers', __name__)

@controllers.route('/',methods=['GET','POST'])
def login():
    if request.method =='GET':
      return render_template('login.html')
    
    elif request.method=='POST':
        username= request.form.get('username')
        password= request.form.get('password')
        # return f'hello {username}'
        if username=="Manoj" and password=="Adminrg@979":
         return render_template('Admin.html', username=username)
        else: 
           return f'who are you?'
        

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

       db.session.add(new_patient)
       db.session.commit()


       
       return render_template("login.html")
       


@controllers.route('/Admin')
def Admin():
    return render_template('Admin.html')


@controllers.route('/Doctor')
def Doctor():
    return render_template('doctor.html')



@controllers.route('/Patient')
def Patient():
    return render_template('patient.html')