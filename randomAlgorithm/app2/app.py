from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from App2!"  # Replace "AppX" with the specific app name

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
