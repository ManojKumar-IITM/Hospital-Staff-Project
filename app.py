import os
from flask import Flask, render_template ,request
from flask_migrate import Migrate
from application.database import db
from application.controllers import *
from application.models import *


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'db_directory', 'Hospital_staff_database.db')




migrate=Migrate()
def create_app():
    app = Flask(__name__ , template_folder='templates')
    app.secret_key= 'thisisaverystrongsecretkeynobodycannotfindit'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    migrate.init_app(app,db)                #for database updation (changes updation)
    app.register_blueprint(controllers)     #to attack controllers to app.py

    return app





app = create_app()








if __name__== '__main__':

    
    
    app.run(host='0.0.0.0', debug=True)