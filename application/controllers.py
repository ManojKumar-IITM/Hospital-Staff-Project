from flask import Flask,request,render_template,Blueprint,flash,redirect,url_for,session,jsonify
from .models import Members,Appointments,Department,Treatment
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
 
        #storing details in session to access while redirecting
        session['username'] = username
        session['password'] = password


        # return f'hello {username}'
        user = Members.query.filter_by(username=username).first()
        if user and user.password==password:
            if user.role == 'admin':
                session['firstname']= user.first_name
                return redirect(url_for('controllers.admin'))
            elif user.role == 'doctor':
                return redirect(url_for('controllers.doctor'))
            elif user.role== 'patient':
                return redirect(url_for('controllers.patient'))
            else:
                flash('Invalid username or password','danger')
                return render_template('login.html')
        flash("No user with the User_name",'danger')
        return render_template('login.html')
        # Note: do NOT reveal which type failed, for security
        
        
        

@controllers.route('/signup' , methods = ["GET","POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method =="POST":
        firstname= request.form.get('firstname')
        lastname=  request.form.get('lastname')
        username=  request.form.get('username')
        password=  request.form.get('password')

        new_patient = Members(
                             username=username,
                             password=password,
                             first_name=firstname,
                             last_name=lastname,
                             role= 'patient'
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
    
@controllers.route('/Admin', methods=['GET','POST'])
def admin():

    if request.method=='GET':
        #for registered doctor and patient div
        username= session['username']
        first_name= session.get('firstname')
        total_doctors = Members.query.filter_by(role='doctor').count()
        total_patients = Members.query.filter_by(role='patient').count()
        doctors= Members.query.filter_by(role='doctor')
        patients= Members.query.filter_by(role='patient')
        appointments = Appointments.query.filter_by(status='booked').all()



        
        return render_template('admin.html',
                               username=username,
                               first_name=first_name,
                               total_doctors=total_doctors,
                               total_patients=total_patients,
                               doctors=doctors,
                               patients=patients,
                               Appointments=appointments)
    
    elif request.method=="POST":

        doctor_first_name=request.form.get('doctor_first_name')
        doctor_last_name=request.form.get('doctor_last_name')
        doctor_username=request.form.get('username')
        doctor_dob=request.form.get('DOB')
        doctor_department=request.form.get('doctor_department')
        doctor_password=request.form.get('password')

        new_doctor = Members(
                             first_name=doctor_first_name,
                             last_name=doctor_last_name,
                             username= doctor_username,
                             password=doctor_password,
                             role='doctor'
                             
        )

        try: 
            db.session.add(new_doctor)
            db.session.commit()
            flash('Doctor added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('AN error occurred:' + str(e), 'error')
        return redirect(url_for('controllers.admin'))

       
        
    

@controllers.route('/get-patient-history/<int:patientId>/<int:doctorId>' , methods=['GET'])
def get_patient_history(patientId,doctorId):

    patient_history = Treatment.query.filter_by(patient_id=patientId).all()
    patient         = Members.query.filter_by(id=patientId).first()
    doctor          = Members.query.filter_by(id=doctorId).first()
    department      = Department.query.filter_by(doctor_id=doctorId).first()


    return  jsonify({
        'patient_history': [h.serialize() for h in patient_history],
        'patient'        : patient.serialize() if patient else {},
        'doctor'         : doctor.serialize() if doctor else {},
        'department'     : department.serialize() if department else {},
    })





@controllers.route('/Doctor', methods=['GET','POST'])
def doctor():

    if request.method=='GET':
        username= session['username']
        return render_template('doctor.html',username=username)
    

@controllers.route('/Patient', methods=['GET','POST'])
def patient():

    if request.method=='GET':
        username= session['username']
        return render_template('patient.html',username=username)
       


