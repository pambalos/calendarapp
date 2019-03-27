from templates import app
from flask import render_template, Blueprint

tutorprofile_blueprint = Blueprint('tutorprofile', __name__)

@tutorprofile_blueprint.route('/login')
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


@tutorprofile_blueprint.route('/register')
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
