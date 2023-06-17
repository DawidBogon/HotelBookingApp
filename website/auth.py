from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import WebsiteUser
from .utils import validate_email
import requests

auth = Blueprint('auth', __name__)

website = WebsiteUser()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        payload = dict(email=email, password=password)
        res = requests.post('http://localhost:5001/login', json=payload)
        if res.status_code == 200:
            res_json = res.json()
            if res_json['result']:
                flash('Logged in successfully!', category='success')
                session['user_id'] = res_json['id']
                if 'first_name' in res_json:
                    session['first_name'] = res_json['first_name']
                else:
                    session['first_name'] = None
                if 'last_name' in res_json:
                    session['last_name'] = res_json['last_name']
                else:
                    session['last_name'] = None
                session['logged_in'] = True
                if session.get('prev_url'):
                    prev_url = session.get('prev_url')
                    session.pop('prev_url')
                    return redirect(prev_url)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=session.get('logged_in'))


@auth.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    res = requests.post('http://localhost:5001/logout')
    if res.status_code == 200:
        res_json = res.json()
        if res_json['result']:
            flash('Logged out successfully', category='success')
            session['user_id'] = None
            session['logged_in'] = None
        else:
            flash('Failed to logout', category='error')
    else:
        flash('Failed to logout', category='error')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        login = request.form.get('login')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not validate_email(email):
            flash('Invalid email', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            payload = dict(email=email, login=login, first_name=first_name, last_name=last_name, password=password1)
            res = requests.post('http://localhost:5001/sign_up', json=payload)
            if res.status_code == 200:
                res_json = res.json()
                if res_json['result']:
                    flash('Account created!', category='success')
                    session['user_id'] = res_json['user_id']
                    session['logged_in'] = True
                    return redirect(url_for('views.home'))
                else:
                    flash('Failed to create user.', category='error')
    return render_template("sign_up.html", user=session.get('logged_in'))
