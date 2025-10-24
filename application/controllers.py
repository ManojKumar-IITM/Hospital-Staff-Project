from flask import Flask,request,render_template,Blueprint,flash,redirect,url_for,session,jsonify
from .models import Members,Appointments,Department,Treatment,Availability
from .database import db
from datetime import datetime,timedelta





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

    username= session['username']
    doctor = Members.query.filter_by(username=username).first()

    if request.method=='GET':
        
        next_7_days = [(datetime.now() + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(7)]
        appointments= Appointments.query.filter_by(doctor_id=doctor.id,status='booked').all()
        all_appointments=Appointments.query.filter_by(doctor_id=doctor.id).all()
        department = Department.query.filter_by(doctor_id=doctor.id).first()



    
    
        return render_template('doctor.html',
                               username=username,
                               days=next_7_days,
                               appointments=appointments,
                               all_appointments=all_appointments,
                               department=department)
    
    elif request.method=='POST':
        

        try:
            data=request.get_json()
            slots=data.get('slots',[])
            doctor_id=doctor.id

            for slot in slots:
                date= slot['date']
                date_obj= datetime.strptime(date,'%d-%m-%Y').date()
                slot= slot['slot']

                existing_entry = Availability.query.filter_by(doctor_id=doctor_id, date=date_obj).first()

                if existing_entry:
                    existing_entry.time_slot=slot
                    db.session.commit()
                else:
                    new_availability = Availability(
                        doctor_id=doctor_id,
                        date=date_obj,
                        time_slot=slot
                    )
                    db.session.add(new_availability)
            db.session.commit()
            return jsonify({'message':'Availability saved successfully!'}),200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message':'An error occurred: ' + str(e)}),500
        

@controllers.route('/save_treatment',methods=['POST'])
def save_treatment():
    try:

        data = request.get_json()
        appointment_id = data.get('appointment_id')
        patient_id     = data.get('patient_id')

        treatment= Treatment.query.filter_by(appointment_id=appointment_id,patient_id=patient_id).first()
        if treatment:
            if 'visit_type' in data: treatment.visittype = data['visit_type']
            if 'test_done' in data: treatment.testdone = data['test_done']
            if 'diagnosis' in data: treatment.diagnosis = data['diagnosis']
            if 'prescription' in data: treatment.prescription = data['prescription']
            if 'notes' in data: treatment.notes = data['notes']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Updated existing treatment!'}), 200
        else:
            new_treatment = Treatment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                visittype=data.get('visittype'),
                testdone=data.get('testdone'),
                diagnosis=data.get('diagnosis'),
                prescription=data.get('prescription'),
                notes=data.get('notes'))

            db.session.add(new_treatment)
            db.session.commit()
            return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    

@controllers.route('/mark_appointment_complete', methods=['POST'])
def mark_appointment_complete():
    try:
        data = request.get_json()
        appointment_id = data.get('appointment_id')

        appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
        if appointment:
            appointment.status = 'completed'
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@controllers.route('/Patient', methods=['GET','POST'])
def patient():

    if request.method=='GET':
        username= session['username']
        return render_template('patient.html',username=username)
       


