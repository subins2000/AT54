from flask import Flask, jsonify, request
import dataset


db = dataset.connect('sqlite:///db.sqlite3')
failures = db['failures']

app = Flask(__name__)

@app.route('/')
def hello():
    return ''

def add(serial_number, model, failure_when, probability):
    failures.insert(
        dict(
            serial_number = serial_number,
            model = model,
            failure_when = failure_when,
            probability = probability
        )
    )

@app.route('/add', methods=['POST'])
def addPrediction():
    model = request.form['model']
    serial_number = request.form['serial_number']
    failure_when = request.form['failure_when']
    probability = request.form['probability']

    add(serial_number, model, failure_when, probability)

    return 'added'