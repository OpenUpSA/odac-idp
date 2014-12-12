import os
from flask import Flask

# setup configs
env = os.environ.get('FLASK_ENV', 'development')

app = Flask(__name__)
app.config['DEBUG'] = (env != 'production')

import odac_idp.views
