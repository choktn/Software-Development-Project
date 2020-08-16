# these are modules for running program

from flask import Flask, render_template, url_for,session,redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,DateTimeField ,DateField,TextAreaField,BooleanField,RadioField,IntegerField,FloatField, SubmitField
from wtforms_components import TimeField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import time
import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import g



Base = declarative_base()
app = Flask(__name__) # created flask app called app
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!' # secret key for security reasons

base_dir = os.path.abspath(os.path.dirname(__file__)) # get file path from base directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)  # create database
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin=Admin(app)
# user class for storing sign-up form data in SQLite

class User(UserMixin, db.Model):
# date 15-june-2019     @author RAJ CHHATBAR
    id = db.Column(db.Integer ,primary_key=True, autoincrement = True)
    username = db.Column(db.String(15), unique=True)
    name=db.Column(db.String(15))
    gender=db.Column(db.String(7))
    address=db.Column(db.String(130))
    city=db.Column(db.String(100))
    state=db.Column(db.String(80))
    zipcode=db.Column(db.String(80))
    date_of_birth=db.Column(db.Date)
    phone_number=db.Column(db.String(15))
    security_question=db.Column(db.String(150))
    security_question_answer=db.Column(db.String(150))

    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


# Account class for storing account balance in SQLite

class Account(db.Model):
# date 15-june-2019     @author RAJ CHHATBAR
    account_id=db.Column(db.Integer , db.ForeignKey('user.id'), primary_key=True,autoincrement = True)
    balance=db.Column(db.Float)



# Transaction class for storing each transaction 

class Transaction(db.Model):
# date 16-june-2019     @author RAJ CHHATBAR
    transfer_id= db.Column(db.Integer ,primary_key=True, autoincrement = True)
    account_id=db.Column(db.Integer,db.ForeignKey('account.account_id'))
    amount=db.Column(db.Float)
    balance=db.Column(db.Float)
    time=db.Column(db.DateTime)
    type=db.Column(db.String(30))

#Make_an_appointment class for storing appointments
# date 22-june-2019     @author RAJ CHHATBAR
class Make_an_appointment(db.Model):
    appointment_id=db.Column(db.Integer ,primary_key=True, autoincrement = True)
    appointment_account_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    appointment_date=db.Column(db.Date)
    appointment_time=db.Column(db.Time)
    appointment_location=db.Column(db.String(60))
    about_what=db.Column(db.String(100))


# get current login user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class LoginForm for user login

class LoginForm(FlaskForm):
# date 15-june-2019     @author TAVIN CHOK
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


# class sign-up form for user signup
# date 15-june-2019     @author RAJ CHHATBAR
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    name = StringField('name', validators=[InputRequired(), Length(min=2, max=60)])
    gender = RadioField('gender', choices = [('male','Male'),('female','Female'),('other','Other')], validators=[InputRequired()])
    address=TextAreaField("Address",validators=[InputRequired(), Length(min=4, max=130)])
    city=StringField("city",validators=[InputRequired(), Length(min=2, max=100)])
    state=StringField("state",validators=[InputRequired(), Length(min=2, max=80)])
    zipcode=StringField("zip-code",validators=[InputRequired(), Length(min=2, max=80)])
    date_of_birth=DateField("Date of Birth",validators=[InputRequired()], format='%m/%d/%y')
    phone_number=StringField("Phone No.",validators=[InputRequired(), Length(min=4, max=15)])
    security_question=StringField("Security question",validators=[InputRequired(), Length(min=4, max=150)])
    security_question_answer=StringField("Security question answer",validators=[InputRequired(), Length(min=4, max=150)])

    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# date 16-june-2019     @author TAVIN CHOK
# class deposit form form deposit form input
class DepositForm(FlaskForm):
    amount_deposit = FloatField('Deposit amount', validators=[InputRequired()])
    deposit=SubmitField("Deposit")


# date 16-june-2019     @author RAJ CHHATBAR
# class withdrawalForm form withdraw form input
class WithdrawForm(FlaskForm):
    amount_withdraw = FloatField('Withdraw amount', validators=[InputRequired()])
    withdraw=SubmitField("Withdraw")

# date 17-june-2019     @author TAVIN CHOK
# class TransferForm form form Transfer form input
class TransferForm(FlaskForm):
    amount_transfer = FloatField('Transfer amount', validators=[InputRequired()])
    account_number=IntegerField('Account number', validators=[InputRequired()])
    transfer=SubmitField("Transfer")

# date 22-june-2019     @author RAJ CHHATBAR
# class AppointmentForm form Appointment form input
class AppointmentForm(FlaskForm):
    appointment_date=DateField("Date" ,validators=[InputRequired()], format='%m/%d/%y')
    appointment_time=TimeField("Time" ,validators=[InputRequired()])
    appointment_location=StringField('location', validators=[InputRequired(), Length(min=2, max=60)])
    about_what=StringField('About what', validators=[InputRequired(), Length(min=2, max=100)])
    schedule=SubmitField("Schedule")

# date 23-june-2019     @author RAJ CHHATBAR
# class ResetForm form Reset form input
class ResetForm(FlaskForm):
    reset_username = StringField('Enter username', validators=[InputRequired(), Length(min=4, max=15)])
    next=SubmitField("Next")

# date 23-june-2019     @author RAJ CHHATBAR
# class SecurityForm form Security form input
class SecurityForm(FlaskForm):
    question_answer=StringField("Security question answer",validators=[InputRequired(), Length(min=4, max=150)])

# date 23-june-2019     @author RAJ CHHATBAR
# class ResetPasswordForm form Security form input
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[InputRequired(), Length(min=8, max=80)])




@app.route('/')
def index():
    return render_template('index.html')

# date 15-june-2019     @author TAVIN CHOK
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()      #create login form object

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # find user in database
        if user:
            if check_password_hash(user.password, form.password.data):  # check hash password
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard')) # redirect to dashboard

        return '<h1>Invalid username or password</h1>' # if incorrect display message
 

    return render_template('login.html', form=form)

# date 15-june-2019     @author TAVIN CHOK
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()   # create registration form object

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256') # generate hash password
        new_user = User(username=form.username.data,name=form.name.data, email=form.email.data, gender=form.gender.data,address=form.address.data,city=form.city.data,state=form.state.data,zipcode=form.zipcode.data,date_of_birth=form.date_of_birth.data,phone_number=form.phone_number.data,security_question=form.security_question.data,security_question_answer=form.security_question_answer.data ,password=hashed_password) # create new user object
        new_account=Account(balance=0.0)  # set balance to zero
      

        db.session.add(new_user)  # add user to session
        db.session.add(new_account) # add account details to sessions
        db.session.commit()  # commit changes to database

        return '<h1>New user has been created!</h1>'  #message for new user
       

    return render_template('signup.html', form=form) # display html file plus get user input

@app.route('/dashboard')  # set url for dashboard
@login_required   # loginrequired to accessing dashboard

# date 15-june-2019     @author RAJ CHHATBAR
def dashboard(): 
    user = User.query.filter_by(username=current_user.username).first() # get user from database
    account = Account.query.filter_by(account_id=user.id).first()  #get account form database
    all_transactions= Transaction.query.filter_by(account_id=user.id) #get all transactions from database
    return render_template('dashboard.html', all_transactions=all_transactions,id=user.id ,user_name=current_user.username,name=user.name,address=user.address,city=user.city,state=user.state,zipcode=user.zipcode,phone=user.phone_number,balance=account.balance )
# here all variable are taking input from form HTML


# date 16-june-2019     @author TAVIN CHOK
@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():

    form=DepositForm()   # form class for deposit
    user = User.query.filter_by(username=current_user.username).first() # get user from database
    account = Account.query.filter_by(account_id=user.id).first() #get account form database
    if form.validate_on_submit():  # validate on submit for input by user
 
        new_transaction=Transaction(account_id=user.id, amount=form.amount_deposit.data, balance=float((account.balance)+form.amount_deposit.data) , time=datetime.datetime.now(), type="Deposit") # create new transaction 
        account.balance=((account.balance)+form.amount_deposit.data) # update balance
        db.create_all()
        db.session.add(new_transaction)  
        db.session.commit()    # commit new transection and updated balance in database
        return '<h1>New depost made!</h1>'

    return render_template('deposit.html', form=form )
    #return '<h1> deposit!</h1>'

# date 16-june-2019     @author RAJ CHHATBAR
@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    form=WithdrawForm()   # object for withdraw form
    user = User.query.filter_by(username=current_user.username).first()
    account = Account.query.filter_by(account_id=user.id).first()
    if form.validate_on_submit():
        if (form.amount_withdraw.data)<=account.balance:    # check withdraw less than balance
            new_transaction=Transaction(account_id=user.id, amount=(-(form.amount_withdraw.data)), balance=float((account.balance)-form.amount_withdraw.data) , time=datetime.datetime.now(), type="Withdraw")
            account.balance=((account.balance)-form.amount_withdraw.data)

            db.session.add(new_transaction)
            db.session.commit()
            return '<h1>New withdraw made!</h1>'
        else:
            return '<h1>Insufficient balance!</h1>'   # display insufficient balance

    return render_template('withdraw.html', form=form )
    #return '<h1> withdraw!</h1>'


# date 16-june-2019     @author TAVIN CHOK
@app.route('/transfer', methods=['GET', 'POST'])    # transfer function
@login_required
def transfer():
    form=TransferForm()   # object for transfer form
    user_sender = User.query.filter_by(username=current_user.username).first()
    account_sender = Account.query.filter_by(account_id=user_sender.id).first()
    if form.validate_on_submit():

        user_recieve = User.query.filter_by(id=form.account_number.data).first()   # recipient user
        if user_recieve:
            account_recieve = Account.query.filter_by(account_id=user_recieve.id).first() #recipient account
            if (form.amount_transfer.data)<=account_sender.balance:    # check for transfer amount less than balance

                new_transaction_debit=Transaction(account_id=user_sender.id, amount=(-(form.amount_transfer.data)), balance=float((account_sender.balance)-form.amount_transfer.data) , time=datetime.datetime.now(), type=("Transfer to, {}." .format(user_recieve.name)) )
# sender user debit transection
                new_transaction_credit=Transaction(account_id=user_recieve.id, amount=((form.amount_transfer.data)), balance=float((account_recieve.balance)+form.amount_transfer.data) , time=datetime.datetime.now(), type=("Transfer from, {}." .format(user_sender.name))  )
                account_sender.balance=((account_sender.balance)-form.amount_transfer.data)
                account_recieve.balance=((account_recieve.balance)+form.amount_transfer.data)

                db.session.add(new_transaction_debit)
                db.session.add(new_transaction_credit)
                db.session.commit()
                return '<h1>New transfer made!</h1>'
            else:
                return '<h1>Insufficient balance!</h1>'

        else:
            return '<h1>Invalid account number!</h1>'



    return render_template('transfer.html', form=form )

    #return render_template('transfer.html',  )
    #return '<h1> transfer!</h1>'

# date 22-june-2019     @author TAVIN CHOK
@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    form=AppointmentForm()  # object for appointment form
    user = User.query.filter_by(username=current_user.username).first()
    all_appointment= Make_an_appointment.query.filter_by(appointment_account_id=user.id).first() # make an appointment database query for any upcoming appointment
    if form.validate_on_submit():
        new_appointment=Make_an_appointment(appointment_account_id=user.id,appointment_date=form.appointment_date.data,appointment_time=form.appointment_time.data, appointment_location=form.appointment_location.data, about_what=form.about_what.data)
        db.session.add(new_appointment)
        db.session.commit()
        return '<h1>New appointment made!</h1>'


    return render_template('appointment.html',all_appointment=all_appointment , form=form  )
    #return '<h1> appointment!</h1>'



# date 23-june-2019     @author RAJ CHHATBAR
@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    form=ResetForm()    # reset password form for username
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.reset_username.data).first()
        if user:
            session['forgot_user_name'] = (form.reset_username.data)  # store user name in session for use in another function

            return redirect(('security_question'))
        else:
            return '<h1>Invalid user!</h1>'

    return render_template('reset.html' , form=form   )

# date 23-june-2019     @author TAVIN CHOK
@app.route('/security_question', methods=['GET', 'POST'])
def reset_user_password():
    form=SecurityForm()  # object for security question answer form
    forgot_user = session.get('forgot_user_name', None)  # get user from session
    user = User.query.filter_by(username=forgot_user).first()
    question_asked=user.security_question
    if form.validate_on_submit():
        que_answer=user.security_question_answer  # question answer from user
        if (str(que_answer)==str(form.question_answer.data)):  # validate user answer
            return redirect(url_for('reset_link'))
        else:
            return "<h1>Invalid answer!</h1>"

    return render_template('security_question.html' , question_asked=question_asked,form=form   )

# date 23-june-2019     @author RAJ CHHATBAR
@app.route('/reset_link', methods=['GET', 'POST'])
def reset_link():
    form=ResetPasswordForm()  # object for reset password field
    forgot_user = session.get('forgot_user_name', None)
    user = User.query.filter_by(username=forgot_user).first()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256') # generate new hashed password
        user.password=hashed_password
        db.session.commit()   # commit new password to that user database
        return "<h1>Password changed!</h1>"

    return render_template('reset_link.html' , form=form   )

@app.route('/logout')
@login_required
def logout():   # logot method by using logout_user() prebuild method
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # creare database table
    app.run(debug=True)  # run system in debug mode

