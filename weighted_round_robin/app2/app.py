from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello():
    server_name = os.environ.get('SERVER_NAME', 'Unknown')
    return f"Hello from {server_name}!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
