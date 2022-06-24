#!/usr/bin/python3

# python3 -m pip venv env
# python3 -m pip install -r requirements.txt --no-cache-dir
from flask_cors import CORS

from vine import create_app
from vine import Config

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, ssl_context=(Config.CRT_FILE, Config.CRT_KEY), debug=Config.DEBUG)
