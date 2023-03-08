#####################################################################################
# Importing the required packages and modules
#####################################################################################

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

#####################################################################################
# Initializing the Flask application and SQLAlchemy ORM
#####################################################################################

# initializing the Flask web application
app = Flask(__name__)

# database for this web application is called phone
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone.db'

# initializing the database
db = SQLAlchemy(app)

#####################################################################################
# MODELS used in the Database
#####################################################################################

# Table to store the contact information about a user
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # there are 4 fields in the data table
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    # string representation of one entry in the database                
    def __repr__(self):
        return '<name : %r>' % self.phone

#####################################################################################

# we have to initialize the database schemas which are stored in the models
with app.app_context():
    db.create_all()

#####################################################################################
# ROUTES for various functions in the web application
#####################################################################################

# HOME PAGE
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html'
        )
    
    # POST request means a new entry has been made to the Directory
    if request.method == 'POST':
        new_entry = Contact(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address']
        )

        try:
            # adding and commiting the new entry
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/')
        except:
            return """[ERROR] Could not push new entry to Directory!!"""


# DISPLAY PAGE
@app.route('/display', methods=['GET', 'POST'])
def display():
    contacts = Contact.query.all()

    return render_template(
        'display.html',
        contacts = contacts # use this variable in jinja2 template
    )

#####################################################################################
# Running the application
#####################################################################################

if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0'
    )

