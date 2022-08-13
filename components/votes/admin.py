from flask_admin.contrib.sqla import ModelView
from components.votes.models import Vote


class VoteView(ModelView):

    column_list = (
        'id',
        'uuid',
        'win_id',
        'lose_id',
        'timestamp'
    )
    create_modal = True
    edit_modal = True


def load_views(admin, session):
    admin.add_view(VoteView(Vote, session))
