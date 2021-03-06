#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm 
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse 
from app import db
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'everybody'}
    posts = [
        {
            'author': {'username': 'СТРАНЫ'},
            'body': 'Россия, Франция, Польша, Чехия, Литва ... '
        },
        {
            'author': {'username': 'ГОРОДА'},
            'body': 'Москва, Лондон, Копенгаген, Барселона, Рига ... '
        }, 
        {
            'author': {'username': 'АВИАКОМПАНИИ'},
            'body': ' Белка, Стрелка, Ракета ... '
        }
    ]
    return render_template("index.html", title='Мой профиль', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ошибка в имени или пароле!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ура, теперь вам доступна покупка билетов!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/calen')
def calen():
    return render_template('calendar.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/call')
def call():
    return render_template('call.html')

@app.route('/pokupka')
def pokupka():
    return render_template('pokupka.html')

@app.route('/oplata')
def oplata():
    return render_template('oplata.html')


