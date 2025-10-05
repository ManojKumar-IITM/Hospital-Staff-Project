import os
from flask import Flask, render_template ,request
from application.database import db
from application.controllers import *
from application.models import *


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'db_directory', 'Hospital_staff_database.db')





def create_app():
    app = Flask(__name__ , template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    app.register_blueprint(controllers)

    return app





app = create_app()







if __name__== '__main__':

    with app.app_context():
        from application import models  # Make sure Admin class is imported
        db.create_all()
    
    app.run(host='0.0.0.0', debug=True)