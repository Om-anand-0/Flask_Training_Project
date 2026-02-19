from flask import Blueprint, request
from app.models import User
from app import bcrypt, db, app, login_manager
from identicons import generate, save
from flask import render_template, redirect, url_for
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return 'Invalid username or password'
        login_manager.user_loader(user)
        return 'Login successful'
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        image = request.files.get('image')
        file_name = f"{username}.png"
        if image_file:
            image_file.save(os.path.join("app/static/images", file_name))
        else:
            img =generate(username)
            save(img,os.path.join("app/static/images", file_name), 500, 500)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.query.filter_by(username=username).first()
        if user:
            return 'User already exists'
        user = User(username=username, email=email, password=hashed_password, avatar_url=f'{username}.png')
        db.session.add(user)
        db.session.commit()
        return 'User registered successfully'
    return render_template('auth/register.html')
