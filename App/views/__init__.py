from App.views.qq_groups_view import qq_group_bluprint


def init_view_router(app):
    app.register_blueprint(blueprint=qq_group_bluprint)
