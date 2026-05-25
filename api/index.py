import traceback

try:
    from python.web_dashboard import app
except Exception as e:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"Import Error: {traceback.format_exc()}", 500
