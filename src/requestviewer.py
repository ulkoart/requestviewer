import datetime
import json

from flask import Flask, request, render_template, redirect

app = Flask(__name__)


def log_writer(request):
    try:
        with open('logs.json', 'r') as log_file:
            log_data = json.load(log_file)

    except(json.decoder.JSONDecodeError, OSError):
        log_data = {"data": []}

    r = {
        "dateTime": datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y %H:%M:%S'),
        "postData": request.data.decode('utf-8'),
        "ip": request.environ.get('REMOTE_ADDR'),
        "HTTP_USER_AGENT": request.environ.get('HTTP_USER_AGENT'),
    }
    logs = log_data.get('data')
    logs.append(r)
    with open('logs.json', 'w') as log_file:
        json.dump(log_data, log_file)


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/howitworks', methods=['GET'])
def howitworks_page():
    return render_template('howitworks.html')


@app.route('/clear', methods=['GET'])
def clear_page():
    with open('logs.json', 'w'):
        return redirect('/log')


@app.route('/log', methods=['GET', 'POST'])
def log_page():
    if request.method == 'POST':
        log_writer(request)
        return 'done'

    elif request.method == 'GET':
        with open('logs.json', 'r') as log_file:
            try:
                log_data = json.load(log_file)
                logs = log_data.get("data")
            except json.decoder.JSONDecodeError:
                logs = None
        return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
