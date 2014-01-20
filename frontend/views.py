from flask import Flask
from flask import render_template

app = Flask("ODAC - IDP", instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)

@app.route('/')
def root():

    return render_template('base.html')

if __name__ == "__main__":
    # run Flask dev-server
    app.run(port=5000)