from flask import Flask

def deploy_api():
    api = Flask(__name__)

    with api.app_context():
        from .demo import bp
        api.register_blueprint(bp)

    return api
