import os
from project import app

FLASK_PORT = os.environ.get("FLASK_PORT", 5000)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=FLASK_PORT)