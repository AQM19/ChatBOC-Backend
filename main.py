from src.api import deploy_api

app = deploy_api()

if __name__ == '__main__':
    app.run(debug=True)