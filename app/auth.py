from flask import Flask, render_template, request, Blueprint,  url_for, flash, redirect
from .models import User, Password
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                flash('Incorrect Password! Please try again.', category='error')

        else:
            flash('Incorrect email!. Please try again', category='error')

    return render_template('/login.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        first_name = data.get('firstName')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            print('Email already exitsts')
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = User(email = email, first_name = first_name, 
                            password = generate_password_hash(password1, method='pbkdf2:sha256', salt_length=8))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            print('SUCCESS')
            return redirect(url_for('routes.home'))
    
    
    return render_template('sign_up.html', user = current_user)
       