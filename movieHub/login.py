from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from server import app,login_manager
from dbFunctions import checkUser, getUser

class User(UserMixin):
    def __init__(self, username, firstName, lastName):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
    def get_id(self):
        return self.username        

def loginUser(username, password):
    if checkUser(username, password):
        userDetails = getUser(username)
        user = User(username, userDetails[0].firstName, userDetails[0].lastName)
        login_user(user)
        return True

    return False

def get_user(username):
    userDetails = getUser(username)    
    if userDetails:
        user = User(username, userDetails[0].firstName, userDetails[0].lastName)
        return user
    return None


@login_manager.user_loader
def load_user(username):
    # get user information from db
    user = get_user(username)
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
