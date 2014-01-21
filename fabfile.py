from __future__ import with_statement
from fabric.api import *


def staging():
    """
    Env parameters for the staging environment.
    """

    env.hosts = ['ec2-54-194-218-89.eu-west-1.compute.amazonaws.com']
    env.envname = 'staging'
    env.user = 'ubuntu'
    env.group = 'ubuntu'
    env.key_filename = '~/.ssh/aws_code4sa.pem'
    env['config_dir'] = 'config_staging'
    print("STAGING ENVIRONMENT\n")
    return


def restart():

    sudo('service nginx restart')
    sudo('service uwsgi restart')
    return


def setup():
    """
    Install dependencies and create an application directory.
    """

    with settings(warn_only=True):
        sudo('service nginx stop')

    # update locale
    sudo('locale-gen en_ZA.UTF-8')

    # install packages
    sudo('apt-get install build-essential python python-dev')
    sudo('apt-get install python-pip')

    # TODO: setup virtualenv

    # clear pip's cache
    with settings(warn_only=True):
        sudo('rm -r /tmp/pip-build-root')

    # install the necessary Python packages
    put('requirements/base.txt', '/tmp/base.txt')
    put('requirements/production.txt', '/tmp/production.txt')
    sudo('pip install -r /tmp/production.txt')

    # install nginx
    sudo('apt-get install nginx')
    # restart nginx after reboot
    sudo('update-rc.d nginx defaults')
    sudo('service nginx start')
    return


def deploy():
    """
    Upload our package to the server.
    """

    # create application directory if it doesn't exist yet
    with settings(warn_only=True):
        if run("test -d /var/www/odac-idp").failed:
            # create project folder
            sudo('mkdir -p /var/www/odac-idp')

    # create a tarball of our package
    local('tar -czf frontend.tar.gz frontend/', capture=False)

    # upload the source tarball to the temporary folder on the server
    put('frontend.tar.gz', '/tmp/frontend.tar.gz')

    # enter application directory
    with cd('/var/www/odac-idp'):
        # and unzip new files
        sudo('tar xzf /tmp/frontend.tar.gz')

    # now that all is set up, delete the tarball again
    sudo('rm /tmp/frontend.tar.gz')
    local('rm frontend.tar.gz')

    sudo('touch /var/www/odac-idp/frontend/uwsgi.sock')

    # clean out old logfiles
    with settings(warn_only=True):
        sudo('rm /var/www/odac-idp/frontend/debug.log*')

    # ensure user www-data has access to the application folder
    sudo('chown -R www-data:www-data /var/www/odac-idp')
    sudo('chmod -R 775 /var/www/odac-idp')

    # and finally reload the application
    restart()
    return


def configure():
    """
    Upload config files, and restart server.
    """

    with settings(warn_only=True):
        sudo('stop uwsgi')

    with settings(warn_only=True):
        # disable default site
        sudo('rm /etc/nginx/sites-enabled/default')

    # upload nginx server blocks (virtualhost)
    put(env['config_dir'] + '/nginx.conf', '/tmp/nginx.conf')
    sudo('mv /tmp/nginx.conf /var/www/odac-idp/nginx.conf')

    with settings(warn_only=True):
        sudo('ln -s /var/www/odac-idp/nginx.conf /etc/nginx/conf.d/')

    # upload uwsgi config
    put(env['config_dir'] + '/uwsgi.ini', '/tmp/uwsgi.ini')
    sudo('mv /tmp/uwsgi.ini /var/www/odac-idp/uwsgi.ini')

    # make directory for uwsgi's log
    with settings(warn_only=True):
        sudo('mkdir -p /var/log/uwsgi')

    with settings(warn_only=True):
        sudo('mkdir -p /etc/uwsgi/vassals')

    # upload upstart configuration for uwsgi 'emperor', which spawns uWSGI processes
    put(env['config_dir'] + '/uwsgi.conf', '/tmp/uwsgi.conf')
    sudo('mv /tmp/uwsgi.conf /etc/init/uwsgi.conf')

    with settings(warn_only=True):
        # create symlinks for emperor to find config file
        sudo('ln -s /var/www/odac-idp/uwsgi.ini /etc/uwsgi/vassals')

    sudo('chown -R www-data:www-data /var/log/uwsgi')
    sudo('chown -R www-data:www-data /var/www/odac-idp')

    # upload flask config
    with settings(warn_only=True):
        sudo('mkdir /var/www/odac-idp/instance')
    put(env['config_dir'] + '/config.py', '/tmp/config.py')
    sudo('mv /tmp/config.py /var/www/odac-idp/instance/config.py')

    # upload data files
    put('instance/data_budget.json', '/tmp/data_budget.json')
    sudo('mv /tmp/data_budget.json /var/www/odac-idp/instance/data_budget.json')
    put('instance/data_councillors.json', '/tmp/data_councillors.json')
    sudo('mv /tmp/data_councillors.json /var/www/odac-idp/instance/data_councillors.json')

    restart()
    return