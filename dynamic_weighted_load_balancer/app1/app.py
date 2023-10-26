from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/cpu-load')
def get_cpu_load():
    cpu_load = psutil.cpu_percent(interval=1)
    return jsonify({"cpu_load": cpu_load})

@app.route('/')
def hello():
    return "Hello from App1!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
