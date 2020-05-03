# compose_flask/app.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def ami_endpoint():
  return process_versions()

def process_versions():
    return request.form

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
