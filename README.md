odac-idp
========

Demo Web application for browsing through information relating to the government's numerous Integrated Development Plans.


NOTES:
------
To access this server via SSH:

    ssh -v -i ~/.ssh/aws_code4sa.pem ubuntu@ec2-54-194-218-89.eu-west-1.compute.amazonaws.com

Logs can be found at:

* Flask:

        /var/www/odac-idp/debug.log

* Nginx:

        /var/log/nginx/error.log
        /var/log/nginx/access.log

* uWSGI:

        /var/log/uwsgi/emperor.log
        /var/log/uwsgi/uwsgi.log