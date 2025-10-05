from flask import Flask, render_template ,request







app = Flask(__name__ , template_folder='templates')





@app.route('/',methods=['GET','POST'])
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
        

@app.route('/signup' , methods = ["GET","POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method =="POST":
       firstname= request.form.get('firstname')
       lastname=  request.form.get('lastname')
       username=  request.form.get('username')
       password=  request.form.get('password')
       
       return render_template("signup.html")
       


@app.route('/Admin')
def Admin():
    return render_template('Admin.html')


@app.route('/Doctor')
def Doctor():
    return render_template('doctor.html')



@app.route('/Patient')
def Patient():
    return render_template('patient.html')










if __name__== '__main__':
    
    app.run(host='0.0.0.0', debug=True)