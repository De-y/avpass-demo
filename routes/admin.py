from flask import Blueprint, request, render_template
from flask_login import current_user

admin_blueprint = Blueprint('admin', __name__ , template_folder='../pages/',static_folder='../assets/')

@admin_blueprint.route('/', methods=['GET','POST'])
def admin():
  if request.method == 'GET':
    if not current_user.is_authenticated:
      return render_template('errors/404.html')
    if current_user.admin == False:
      return render_template('errors/404.html')
    return render_template('admin.html')