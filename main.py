from src.api import deploy_api
from flask import Flask
from flask_cors import CORS
from src.api.ollama.ollama_bp import ollamaBp


app = Flask(__name__)
app.register_blueprint(ollamaBp)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)