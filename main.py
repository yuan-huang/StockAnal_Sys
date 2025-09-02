import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from app.web.web_server import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=True)
