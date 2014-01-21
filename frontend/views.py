from flask import render_template
from frontend import app
import simplejson

@app.route('/')
def root():

    return render_template('home.html')

f = open('data_budget.json', 'r')
data_budget = simplejson.loads(f.read())

@app.route('/<ward_id>/')
def get_data(ward_id):
    out = []
    if data_budget.get(ward_id):
        out = data_budget[ward_id]
    return simplejson.dumps(out)