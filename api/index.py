import traceback
from flask import Flask

try:
    from importlib import import_module

    app = import_module("python.web_dashboard").app

except Exception:

    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):

        return f"""
        <h2>Vercel Import Error</h2>
        <pre>{traceback.format_exc()}</pre>
        """, 500