from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from keys import *
from forms import LoginForm
from models import Event, CbookInfo, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "sZWjFJmyFQnzkVMxbOIAIZNJhaJV"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #importing sqldatabase
db = SQLAlchemy(app)
db.app = app
oauth = OAuth(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')  #request.args is a dictionary but accessing with ['next'] would throw an error if nonexistent
            flash(f'Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            if user:
                flash(f'Login failed, please check password', 'danger')
            else:
                flash(f'That email is not in use, please try again or register', 'danger')
    return render_template('login.html', title = 'Login', form = form )

@app.route('/register')
def register():
    form = RegistrationForm(FlaskForm)
    if form.validate_on_submit():
        hashp = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(email = form.email.data, password = hashp)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for { form.email.data } created, you may now login.', 'success')
        return redirect(url_for('login'))
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')




# OAuth routes
@app.route('/authorize/checkbook')
def authorizeCbook():
    cbook = OAuth2Session(client_id, scope = 'check')
    authorization_url, state = cbook.authorization_url(cbook_auth_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/authorize/checkbook/callback')
def cbookcallback():
    codestring = str(request.url)
    trash, acode = codestring.split('code=')
    token_headers = {
        'client_id' : client_id,
        'grant_type': 'authorization_code',
        'scope' : ['check'],
        'code' : acode,
        'redirect_uri' : url_for('cbookcallback'),
        'client_secret' : api_secret
    }
    response = requests.post(cbook_token_url, data = token_headers)
    time_requested = datetime.now()
    response_date = json.loads(response.text)
    token_expires = time_requested + timedelta(seconds = response_date['expires_in'])
    user = User.query.filter_by(email = current_user.email).first()
    payment_info = CbookInfo(userID = user.id, token = response_date['access_token'], refresh_token = response_date['refresh_token'], token_expires = token_expires)
    db.session.commit()

# API for retrieving my calendar
@app.route('api/getcalendar/<int:date>', methods = ["GET", "POST"])
def getCalendar():
