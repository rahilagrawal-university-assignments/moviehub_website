from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user, UserMixin
from server import app,login_manager
from dbFunctions import checkUser

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

def loginUser(username, password):
    if checkUser(username, password):
        user = User(username)
        login_user(user)
        return True

    return False

def get_user(username):

    return User(username)


@login_manager.user_loader
def load_user(username):
    # get user information from db
    user = get_user(username)
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
