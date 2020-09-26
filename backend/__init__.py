from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_mail import Mail, Message
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import gc
from flask_cors import CORS
from backend.nearby_hospitals import nearby_hospitals
import json

app = Flask(__name__)
cors = CORS(app)
mail = Mail(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vaccfinder@gmail.com'
app.config['MAIL_PASSWORD'] = 'vaccfinder12!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/json", methods=["POST"])
def read_form_json():
    if request.is_json:
        req = request.get_json()

        fullname = req.get("fullname"),
        email = req.get("email"),
        dob = req.get("dob"),
        phone = req.get("phone"),
        appointmentTime = req.get("appointmentTime")
        hospital = req.get()

        msg = Message('Hello', sender = 'vaccfinder@gmail.com', recipients = [email])
        msg.body = "Thank you for requesting a vaccination appointment at HOSPITAL_NAME through VaccFind. Your details are as below:\nFull name: "+fullname+"\nDate of Birth: "+dob+"\nPhone number: "+"phone\nAppointment Date & Time: "+appointmentTime+"Please reply to this email if any details are incorrect. The hospital will contact you through phone sometime before the appointment date."
        mail.send(msg)

        return "Sent"

    else:

        return "Request was not JSON", 400

@app.route('/register/', methods=["POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            fullname  = form.fullname.data
            email = form.email.data
            dob = form.dob.data
            phone = form.phone.data
            appointmentTime = form.appointmentTime.data
            "fullname\n"

    except Exception as e:
        return(str(e))

@app.route('/location')
def index():
    msg = Message('Hello', sender = 'vaccfinder@gmail.com', recipients = ['someone1@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    
    long = request.args['longitude']
    lat = request.args['latitude']

    location = str(long) + "," + str(lat)

    hospitals = nearby_hospitals(location)
    return json.dumps({ "hospitals": hospitals })

if __name__ == '__main__':
    app.run()
