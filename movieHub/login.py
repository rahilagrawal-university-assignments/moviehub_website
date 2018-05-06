from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app,login_manager
import sqlite3

def _dbselect(query):
    # Logic to connect to the database.
    connection = sqlite3.connect('systemDb.db')
    cursorObj = connection.cursor()
    # execute the query
    rows = cursorObj.execute(query)
    connection.commit()
    results = []
    for row in rows:
        results.append(row)
    cursorObj.close()
    return results

def check_password(user_id, password):
    query = 'SELECT * FROM admin WHERE zid = {} AND pw = "{}";'.format(user_id, password)
    results = _dbselect(query);
    if results:
        user = Admin(user_id)        
        login_user(user)
        return True
    
    query = 'SELECT * FROM student WHERE zid = {} AND pw = "{}"'.format(user_id, password)
    results = _dbselect(query)
    if results:
        user = Student(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        login_user(user)
        return True
    
    query = 'SELECT * FROM staff WHERE zid = {} AND pw = "{}"'.format(user_id, password)
    results = _dbselect(query);
    if results:
        user = Staff(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        login_user(user)
        return True
    
    query = '''SELECT * FROM guest WHERE zid = {} AND pw = "{}"'''.format(user_id, password)
    results = _dbselect(query)
    if results:
        user = Guest(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        login_user(user)
        return True

    return False

def get_user(user_id):
    """
    Your
    get user should get user details from the database
    """
    query = 'SELECT * FROM admin WHERE zid = "{}"'.format(user_id)
    results = _dbselect(query);
    if results:
        return Admin(user_id)
    
    query = 'SELECT * FROM student WHERE zid = "{}"'.format(user_id)
    results = _dbselect(query);
    if results:
        user = Student(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        return user
    
    query = 'SELECT * FROM staff WHERE zid = "{}"'.format(user_id)
    results = _dbselect(query);
    if results:
        user = Staff(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        return user

    query = '''SELECT * FROM guest WHERE zid = {}'''.format(user_id)
    results = _dbselect(query)
    if results:
        user = Guest(user_id)
        query = '''SELECT crs_offer_id FROM enrollment WHERE zid = {};'''.format(user_id)
        courses = _dbselect(query)
        for i in courses:
            query = '''SELECT crs_id,sem FROM course_offer WHERE crs_offer_id = {};'''.format(i[0])
            data = _dbselect(query)
            data = ' '.join(data[0])
            user.set_enrolments(data)
        return user


@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    user = get_user(user_id)
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login', unauthorized=1))

def check_user(user_id):
    query = 'SELECT * FROM admin WHERE zid = {};'.format(user_id)
    results = _dbselect(query);
    if results:
        return False
    
    query = 'SELECT * FROM student WHERE zid = {}'.format(user_id)
    results = _dbselect(query)
    if results:
        return False
    
    query = 'SELECT * FROM staff WHERE zid = {}'.format(user_id)
    results = _dbselect(query);
    if results:
        return False

    query = 'SELECT * FROM guest WHERE zid = {}'.format(user_id)
    results = _dbselect(query);
    if results:
        return False

    return True
