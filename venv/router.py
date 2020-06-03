from flask import Flask, render_template, request
from .contact_us_email import send_contact_us_email
from .add_subscription import add_subscriber_to_db
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email_address = request.form['subscribe_email']
    print(f"Add {email_address} to the database.")
    add_subscriber_to_db(email_address)
    return render_template('thank_you.html')


@app.route('/contact', methods=['POST'])
def contact():
    send_contact_us_email(request.form['email'], request.form['subject'], request.form['message'])
    return render_template('contacted.html')
