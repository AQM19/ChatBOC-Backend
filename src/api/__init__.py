from flask import Flask

def deploy_api():
    api = Flask(__name__)

    with api.app_context():
        
        from .auth import authBp
        from .ollama import ollamaBp
        
        api.register_blueprint(authBp)
        api.register_blueprint(ollamaBp)

    return api
