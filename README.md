odac-idp
========

Demo web application for accessing information contained in the government's numerous Integrated Development Plans.

The demo can be found at: http://odac-idp.demo4sa.org/


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
    sudo pip install -r requirements/local.txt

Run the Flask dev server:

    python runserver_backend.py

The frontend application should now be running at http://localhost:5000.

### Deploy instructions

To deploy this application to an Ubuntu 12.04 instance, which you can access via SSH:

Install the 'fabric' package for interacting with servers via ssh:

    sudo pip install fabric

Set up the relevant config paramenters for your server in `fabdefs.py`.

Navigate into the application folder and run the server setup and deploy scripts:

    cd odac_idp
    fab <server_name> setup
    fab <server_name> deploy
    fab <server_name> configure

More details about setup and deployment can be found in `fabfile.py`, the script that fabric runs during deployment.

### Maintenance

Logs can be found at:

* Flask:

        /path/to/project_dir/debug.log

* Nginx:

        /var/log/nginx/error.log
        /var/log/nginx/access.log

* Supervisor
        /var/log/supervisor/odac_idp.log
