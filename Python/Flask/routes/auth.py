from flask import Blueprint, request, render_template, redirect
from prisma.models import stateService
import json
from flask_login import login_user, logout_user, login_required, current_user
from libraries.db.models import UserModel, get_user
import requests, hashlib, uuid
from libraries.essentials.getenv import get_env

client_id = get_env('client_id')
client_secret = get_env('client_secret')


auth_blueprint = Blueprint('auth', __name__ , template_folder='../pages/', static_folder='../assets/')
@auth_blueprint.route('/', methods=['GET'])
def auth():
    state = hashlib.sha512(str(uuid.uuid4()).encode()).hexdigest()
    stateService.prisma().create(data={'ipAddress': str(request.environ['REMOTE_ADDR']), 'state': state})
    url = 'http://localhost:3000/oauth/initiate'
    myobj = {'state': state, 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': 'http://localhost:5000/callback/avpass'}
    x = requests.post(url, json = myobj)
    response_json = json.loads(x.content.decode('utf-8'))
    uri = response_json['uri']

    return redirect(uri)