"""This is the main flask python file"""
import pyfair
from flask import Flask, flash, request, render_template, redirect, url_for, session, g
import seed
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from person import Person
from fieldsClass import Field
import numpy

app = Flask(__name__)

# Database Details
app.config['MYSQL_HOST'] = seed.host
app.config['MYSQL_USER'] = seed.user
app.config['MYSQL_PASSWORD'] = seed.password
app.config['MYSQL_PORT'] = seed.port
app.config['MYSQL_DB'] = seed.db_name

# EMAIL SMTP DETAILS
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "legendbest123@gmail.com"
app.config['MAIL_PASSWORD'] = "gcpvxzooaxjqabdb"
app.config['MAIL_DEFAULT_SENDER'] = "legendbest123@gmail.com"
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# SECRET KEY

app.secret_key = seed.secret_key


mysql = MySQL(app)
mail = Mail(app)

members1: list = []
members2: list = []
simulation = 0
# FOR HOME PAGE #
####################################
# BACKEND: COMPLETED
# FRONTEND:
####################################

user = Person()


@app.route("/")
def index():
    if 'Email' in session:
        g.email = session['Email']
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/registration", methods=['GET'])
def registration():
    if 'Email' in session:
        g.email = session['Email']
        return redirect(url_for('dashboard'))

    else:
        return render_template("registration.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/process-registration", methods=['POST'])
def process_registration():
    if 'Email' in session:
        g.username = session['Email']
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':

        if request.form['action'] == "signUpBtn":
            user.Email = request.form["Email"]
            user.Password = request.form["Password"]
            user.First_Name = request.form['First_Name']
            user.Last_Name = request.form['Last_Name']
            hashedPassword = generate_password_hash(user.Password)

            try:

                # Email sent to the user
                try:

                    msg = Message('Welcome to The PyFair Application',
                                  sender="legendbest123@gmail.com", recipients=[user.Email])

                    msg.body = 'Your Account is created'

                    cur = mysql.connection.cursor()
                    cur.execute(
                        "INSERT INTO users(First_Name,Last_Name,Email,Password) VALUES (%s,%s,%s,%s)",
                        (user.First_Name, user.Last_Name, user.Email, hashedPassword,))
                    mail.send(msg)
                    mysql.connection.commit()
                    cur.close()
                    flash("Successfully Registered", "success")
                    return redirect(url_for('login'))

                except:
                    flash("Email not valid", "danger")
                    return redirect(url_for('registration'))
                # ----------------------------

            except:
                flash("Server is busy", "warning")
                return redirect(url_for("login"))
        else:
            flash("Unknown Authorization", "warning")
            return redirect(url_for("login"))
    else:
        flash("Session Ended", "warning")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'Email' in session:
        g.username = session['Email']
        return redirect(url_for('dashboard'))

    elif request.method == 'POST':

        # login check over here if it is done go to dashboard
        #
        #
        #

        session.pop('Email', None)
        session.pop('First_Name', None)
        session.pop('Last_Name', None)
        email = request.form['Email']
        password = request.form['Password']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                '''SELECT First_Name,Last_Name,Email,Password FROM users WHERE Email=%s''',
                (email,))
            person = cur.fetchone()
            if person is None:

                flash("Email Incorrect", "danger")
                return render_template("login.html")
            else:
                if check_password_hash(person[3], password):
                    session['First_Name'] = person[0]
                    session['Last_Name'] = person[1]
                    session['Email'] = person[2]

                    mysql.connection.commit()
                    return redirect(url_for('dashboard'))
                else:
                    # Password error
                    flash("Password Incorrect", "danger")
                    return redirect(url_for("login"))
        except:
            flash("Server is busy", "danger")
            return redirect(url_for("login"))

    else:
        return render_template("login.html")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'Email' in session:
        g.username = session['Email']
        return render_template("dashboard.html", session=session)
    else:
        flash("Session Ended", "warning")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/model-2", methods=["GET", "POST"])
def model_2():
    if 'Email' in session:
        g.username = session['Email']
        members = []
        if request.method == "POST":

            if request.form['action'] == 'next':
                try:
                    global simulation
                    simulation = int(request.form['simulation'])
                    global members1
                    members1 = []
                    # storing size of form values like number of participants
                    rows = int((len(request.form) - 1) / 8)

                    for i in range(1, rows + 1):

                        row_array = {}
                        fields = Field()

                        fields.field_name = request.form["field{}".format(i)]
                        fields.gamma = request.form["gamma{}".format(i)]
                        fields.low = request.form["low{}".format(i)]
                        fields.mode = request.form["mode{}".format(i)]
                        fields.high = request.form["high{}".format(i)]
                        fields.constant = request.form["constant{}".format(i)]
                        fields.mean = request.form["mean{}".format(i)]
                        fields.std = request.form["std{}".format(i)]

                        row_array['name'] = fields.field_name
                        if (fields.gamma != ""):
                            row_array['gamma'] = int(fields.gamma)

                        if (fields.low != ""):
                            row_array['low'] = int(fields.low)

                        if (fields.mode != ""):
                            row_array['mode'] = int(fields.mode)

                        if (fields.high != ""):
                            row_array['high'] = int(fields.high)

                        if (fields.constant != ""):
                            row_array['constant'] = int(fields.constant)

                        if (fields.mean != ""):
                            row_array['mean'] = float(fields.mean)

                        if (fields.std != ""):
                            row_array['std'] = float(fields.std)

                        members1.append(row_array)
                    # for storing data into array
                    return render_template("model-2.html")

                except:

                    flash("Please Fill the information Carefully", "danger")
                    return redirect(url_for("dashboard"))

            else:
                pass
        else:
            return redirect(url_for("dashboard"))

    else:
        return redirect(url_for("login"))


# ---------------------------------------------------


@app.route("/result", methods=["GET", "POST"])
def result():
    if 'Email' in session:
        g.username = session['Email']

        if request.method == "POST":

            if request.form['action'] == 'generate':
                try:
                    global members2
                    members2 = []
                    # storing size of form values like number of participants
                    rows = int((len(request.form) - 1) / 8)

                    for i in range(1, rows + 1):

                        row_array = {}
                        fields = Field()

                        fields.field_name = request.form["field{}".format(i)]
                        fields.gamma = request.form["gamma{}".format(i)]
                        fields.low = request.form["low{}".format(i)]
                        fields.mode = request.form["mode{}".format(i)]
                        fields.high = request.form["high{}".format(i)]
                        fields.constant = request.form["constant{}".format(i)]
                        fields.mean = request.form["mean{}".format(i)]
                        fields.std = request.form["std{}".format(i)]

                        row_array['name'] = fields.field_name
                        if (fields.gamma != ""):
                            row_array['gamma'] = int(fields.gamma)

                        if (fields.low != ""):
                            row_array['low'] = int(fields.low)

                        if (fields.mode != ""):
                            row_array['mode'] = int(fields.mode)

                        if (fields.high != ""):
                            row_array['high'] = int(fields.high)

                        if (fields.constant != ""):
                            row_array['constant'] = int(fields.constant)

                        if (fields.mean != ""):
                            row_array['mean'] = float(fields.mean)

                        if (fields.std != ""):
                            row_array['std'] = float(fields.std)

                        members2.append(row_array)

                    # for storing data into array
                    model1 = pyfair.FairModel(
                        name="Regular Model 1", n_simulations=simulation)
                    global members1
                    for i in range(len(members1)):

                        if 'low' in members1[i].keys():
                            model1.input_data(members1[i]['name'], low=members1[i]['low'],
                                              mode=members1[i]['mode'], high=members1[i]['high'])

                        elif 'constant' in members1[i].keys():
                            model1.input_data(members1[i]['name'],
                                              constant=members1[i]['constant'])
                        elif 'mean' in members1[i].keys():
                            model1.input_data(
                                members1[i]['name'], mean=members1[i]['mean'], stdev=members1[i]['std'])

                    model1.calculate_all()
                    model2 = pyfair.FairModel(
                        name="Regular Model 2", n_simulations=simulation)

                    for i in range(len(members2)):

                        if 'low' in members2[i].keys():
                            model2.input_data(members2[i]['name'], low=members2[i]['low'],
                                              mode=members2[i]['mode'], high=members2[i]['high'])

                        elif 'constant' in members2[i].keys():
                            model2.input_data(members2[i]['name'],
                                              constant=members2[i]['constant'])
                        elif 'mean' in members2[i].keys():
                            model2.input_data(
                                members2[i]['name'], mean=members2[i]['mean'], stdev=members2[i]['std'])

                    mm = pyfair.FairMetaModel(
                        name='My Meta Model!', models=[model1, model2])
                    mm.calculate_all()
                    # #modelMMResult = mm.export_results().to_dict()
                    fsr = pyfair.FairSimpleReport([model1, mm])
                    fsr.to_html('./templates/result.html')
                    # print (modelMMResult)

                    return render_template("result.html")
                except:
                    flash("Please Fill the information Carefully", "danger")
                    return redirect(url_for("dashboard"))

            else:
                redirect(url_for("dashboard"))
        else:
            return redirect(url_for("dashboard"))

    else:
        return redirect(url_for("login"))


# -----------------------------------------------------

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'Email' in session:
        g.username = session['Email']
        return render_template("profile.html", session=session)
    else:
        flash("Session Ended", "warning")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/update_profile", methods=['GET', 'POST'])
def update_profile():

    if 'Email' in session:
        if request.method == "POST":
            if request.form['action'] == "update":
                updatePerson = Person()

                updatePerson.First_Name = request.form["First_Name"]
                updatePerson.Last_Name = request.form["Last_Name"]
                updatePerson.Email = session['Email']
                if request.form["Password"] == request.form["Confirm_Password"]:
                    updatePerson.Password = request.form["Password"]
                    updatePerson.Password = generate_password_hash(
                        updatePerson.Password)
                    try:

                        # Email sent to the user
                        try:

                            msg = Message('Email Updated !',
                                          sender="legendbest123@gmail.com", recipients=[updatePerson.Email])

                            msg.body = 'Your Account email is updated'

                            cur = mysql.connection.cursor()
                            cur.execute(
                                "UPDATE users set First_Name=%s,Last_Name=%s,Password=%s WHERE Email = %s",
                                (updatePerson.First_Name, updatePerson.Last_Name, updatePerson.Password, updatePerson.Email))
                            mail.send(msg)
                            mysql.connection.commit()
                            cur.close()
                            session['First_Name'] = updatePerson.First_Name
                            session['Last_Name'] = updatePerson.Last_Name
                            session['Email'] = updatePerson.Email
                            flash("Successfully Updated", "success")
                            return redirect(url_for("profile"))

                        except:
                            flash("Server is busy!", "warning")
                            return redirect(url_for("profile"))
                        # ----------------------------

                    except:
                        flash("Server is busy!", "warning")
                        return redirect(url_for("profile"))
                else:
                    flash("Password Not Matched", "danger")
                    return redirect(url_for("profile"))

            else:
                return redirect(url_for("profile"))
        else:
            return redirect(url_for("profile"))
    else:
        flash("Session Ended", "warning")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/logout")
def logout():
    if 'Email' in session:
        session.pop('Email', None)
        session.pop('First_Name', None)
        session.pop('Last_Name', None)
        flash("Account Logged Out", "success")
        return redirect(url_for("login"))
    else:
        flash("Access Denied", "danger")
        return redirect(url_for("login"))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


if __name__ == "__main__":
    app.run(debug=True)
