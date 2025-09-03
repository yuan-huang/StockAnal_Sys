import os
from app.web.web_server import app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port,load_dotenv=True, debug=True)
