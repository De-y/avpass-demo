from flask import Flask, render_template
from flask_login import LoginManager
from prisma import Prisma, register
from prisma.models import User
from routes.login import login_blueprint
from routes.logout import logout_blueprint
from routes.dashboard import dashboard_blueprint
from routes.admin import admin_blueprint
from routes.auth import auth_blueprint
from routes.errors.notfound import notfound_blueprint
# from routes.post import post_blueprint

db = Prisma()
db.connect()
register(db)

app = Flask(__name__,template_folder='pages/',static_folder='./assets/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = "ABORT"
@app.login_manager.user_loader
def load_user(_id):
    if _id is not None:
      user = User.prisma().find_first(where={'id': _id})
      return user
    else:
      return None
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')
app.register_blueprint(logout_blueprint, url_prefix='/logout')
app.register_blueprint(auth_blueprint, url_prefix='/login')
# app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(notfound_blueprint, url_prefix='/404')
app.register_blueprint(login_blueprint, url_prefix='/callback')

if __name__ == "__main__":
  app.run(debug=True, port=5000, threaded=True)
