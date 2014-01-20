from flask import Flask
from flask import render_template

app = Flask("ODAC - IDP")

@app.route('/')
def root():

    return render_template('base.html')

if __name__ == "__main__":
    # run Flask dev-server
    app.run(port=5000)