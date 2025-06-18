from flask import Flask, jsonify, render_template, request, Blueprint,  url_for, flash, redirect
from .models import User, Password
from .database import db
from flask_login import current_user, login_required
import json


routes = Blueprint("routes", __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        password = request.form.get('password')
        name = request.form.get('name')

        new_password = Password(data=password, name = name, user_id = current_user.id)
        db.session.add(new_password)
        db.session.commit()
        flash('Password Saved!', category='success')
    
    passwords = Password.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', user=current_user, passwords=passwords)


@routes.route('/delete-password', methods=['POST'])
@login_required
def delete_password():
    try:
        password_data = json.loads(request.data)
        password_id = password_data.get('passwordId')


        password = Password.query.get(password_id)

        if password and password.user_id == current_user.id:
            db.session.delete(password)
            db.session.commit()
            return jsonify({}), 200  # Return success response

        return jsonify({'error': 'Unauthorized or password not found'}), 403  # Return error response
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle unexpected errors