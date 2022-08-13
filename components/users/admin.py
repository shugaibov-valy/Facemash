from flask_admin.contrib.sqla import ModelView
from components.users.models import User


class UserView(ModelView):

    column_list = (
        'id',
        'vk_id',
        'photo',
        'rating',
        'times'
    )
    create_modal = True
    edit_modal = True

    column_searchable_list = ["vk_id", "photo"]


def load_views(admin, session):
    admin.add_view(UserView(User, session))
