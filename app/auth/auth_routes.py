from app.models import Users, db
from app.auth.auth_helpers import basic_auth, token_auth
from flask import Blueprint, request

auth = Blueprint('auth',__name__)

@auth.post('/signup')
def signup():
    data = request.json

    # Get data from request
    username = data['username']
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    confirm_password = data['confirm_password']

    if password != confirm_password:
        return {
            'status': 'not ok',
            'message': 'Passwords do not match.',
            'severity':'error'
        }, 400
    
    # See if user exists
    user = Users.query.filter_by(username=username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'Please choose a different username.',
            'severity':'error'
        }, 400
    
    user = Users.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'Please choose a different email.',
            'severity':'error'
        }, 400

    # Create a new user
    user = Users(username, email, password, first_name,last_name)
    user.saveToDB()

    return {
        'status': 'ok',
        'message': "You have successfully created an account."
    }, 201


@auth.post('/login')
@basic_auth.login_required
def login():
    # user = basic_auth.verify_password()
    return {
        'status': 'ok',
        'message': "You have successfully logged in.",
        'data': basic_auth.current_user().to_dict()
    }, 200