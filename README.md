odac-idp
========

Demo web application for accessing information contained in the government's numerous Integrated Development Plans.

The demo can be found at: http://idp.code4sa.org/


## What does this project do

The purpose of this application is to demonstrate an interface for giving citizens access to information
regarding their local government's Integrated Development Plans. The idea is for citizens to be able to identify
current & upcoming government-sponsored projects in their area, helping them keep track of the
their government's progress towards executing it's development goals.


## How it works

The application renders a Google map overlayed with demarcated areas.

When a user clicks on one of these areas, information relative to that area is rendered next to the map,
including a list of ongoing government projects.

## Contributing to the project

This project is open-source, and anyone is welcome to contribute. If you just want to make us aware of a bug / make
a feature request, then please add a new GitHub Issue (if a similar one does not already exist).

If you want to contribute to the code, please fork the repository, make your changes, and create a pull request.

### Local setup

To run this application in your local environment, use the builtin Flask dev-server:

Navigate into the application folder and install the required Python packages:

    cd odac_idp
    virtualenv --no-site-packages env
    source env/bin/activate
    pip install -r requirements.txt

Run the Flask dev server:

    python runserver_backend.py

The frontend application should now be running at http://localhost:5000.

### Deploy instructions

This application runs on Heroku. To deploy, just use `git push heroku`.

When setting up on Heroku, be sure to set the environment variables:

    FLASK_ENV=production
