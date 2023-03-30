from flask import Blueprint, request, render_template, redirect
from prisma.models import User, stateService
from flask_login import login_user, logout_user, login_required, current_user
from libraries.db.models import UserModel, get_user
import hashlib, requests, json
from libraries.essentials.getenv import get_env

client_id = get_env('client_id')
client_secret = get_env('client_secret')


login_blueprint = Blueprint('login', __name__ , template_folder='../pages/', static_folder='../assets/')

@login_blueprint.route('/avpass', methods=['GET','POST'])
def login():
  code = request.args.get("code")
  state = request.args.get("state")

  if request.method == 'GET':
    if current_user.is_authenticated:
      return redirect('/dashboard')

    url = 'http://localhost:3000/oauth/api/user_info'
    myobj = {'auth_code': code, 'client_id': client_id, 'client_secret': client_secret}
    x = requests.post(url, json = myobj)
    response_json = json.loads(x.content.decode('utf-8'))


    stateValidator = stateService.prisma().find_first(where={'ipAddress': str(request.remote_addr), 'state': state})

    if stateValidator is None:
      return {'error': 'Invalid state'}, 403

    try:
      check = User.prisma().find_first(where={'email': response_json['email']})
      if check.email == response_json['email']:
        user = get_user(response_json['email'])
        login_user(UserModel(user))
        return redirect('/dashboard')

    except:
      if response_json['emailVerified'] == False:
        return redirect('/auth')

      user = User.prisma().create(data={'email': response_json['email'], 'username': response_json['username'], 'admin': True})
      user2 = get_user(response_json['email'])
      login_user(UserModel(user2))
      return redirect('/dashboard')
