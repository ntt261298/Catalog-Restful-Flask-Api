from main import app
import main.controllers

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')
