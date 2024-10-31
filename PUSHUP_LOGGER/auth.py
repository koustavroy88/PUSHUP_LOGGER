from flask import Blueprint, render_template, redirect, url_for, request, flash
from .model import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
auth_bp=Blueprint('auth_bp',__name__)

@auth_bp.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        print(name,email,password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists")
            print("User already exists")
            return redirect(url_for('auth_bp.signup'))        
        user = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth_bp.login'))        
        
    return render_template('signup.html')

@auth_bp.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        email=request.form.get("email")
        password1=request.form.get("password")
        user=User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password,password1):
            flash("Wrong Credentials")
            print("Wrong Credentials")
            return redirect(url_for('auth_bp.login'))
        
        login_user(user)
        return redirect(url_for('main_bp.profile'))
    return render_template('login.html')

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.home'))
