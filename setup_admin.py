from flask import Flask
from flask_admin import Admin

from db import session
from settings import config

from components.votes import admin as votes_view
from components.users import admin as users_view
from flask_babelex import Babel

def admin_start():

    app = Flask(__name__)

    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        return 'ru'

    admin = Admin(app, name='Facemash-Admin', template_mode='bootstrap3')

    users_view.load_views(admin, session)
    votes_view.load_views(admin, session)

    app.config.from_object(config)
    app.run(host="0.0.0.0", port=9970)
