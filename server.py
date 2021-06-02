from flask import Flask, redirect, url_for, render_template
from threading import Thread

app = Flask(__name__)
result = ""
@app.route('/')
def main():
  return render_template('index.html')

@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    result = language
def run():
  app.run(host='0.0.0.0', port=8080)

def server():
  server = Thread(target=run)
  server.start()
