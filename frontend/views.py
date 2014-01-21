from flask import render_template
from frontend import app
import simplejson

@app.route('/')
def root():

    return render_template('home.html')

with app.open_instance_resource('data_budget.json') as f:
    data_budget = simplejson.loads(f.read())

with app.open_instance_resource('data_councillors.json') as f:
    data_councillors = simplejson.loads(f.read())

@app.route('/<ward_id>/')
def get_data(ward_id):
    out = {"projects": [], "councillor": {}}
    if data_budget.get(ward_id):
        out["projects"] = data_budget[ward_id]
    if data_councillors.get(ward_id):
        out["councillor"] = data_councillors[ward_id]
    return simplejson.dumps(out)