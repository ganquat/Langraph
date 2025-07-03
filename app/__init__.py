from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # app.config.from_object('config.Config') # If you have a config file

    with app.app_context():
        from . import routes
        # You can also register blueprints here if your app grows
        # app.register_blueprint(some_blueprint)

    return app
