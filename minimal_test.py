from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello! The app is working!"

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working!"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 