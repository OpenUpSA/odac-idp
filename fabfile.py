from __future__ import with_statement
from fabric.api import *
from fabdefs import *


def set_permissions():
    """
    Ensure user www-data has access to the application folder.
    """
    sudo('chown -R www-data:www-data ' + env.project_dir)
    sudo('chmod -R 775 ' + env.project_dir)
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
    put(env.config_dir + '/nginx.conf', '/tmp/nginx.conf')
    sudo('mv /tmp/nginx.conf %s/nginx.conf' % env.project_dir)

    with settings(warn_only=True):
        sudo('ln -s %s/nginx.conf /etc/nginx/conf.d/' % env.project_dir)

    # upload uwsgi config
    put(env.config_dir + '/uwsgi.ini', '/tmp/uwsgi.ini')
    sudo('mv /tmp/uwsgi.ini %s/uwsgi.ini' % env.project_dir)

    # make directory for uwsgi's log
    with settings(warn_only=True):
        sudo('mkdir -p /var/log/uwsgi')

    with settings(warn_only=True):
        sudo('mkdir -p /etc/uwsgi/vassals')

    # upload upstart configuration for uwsgi 'emperor', which spawns uWSGI processes
    put(env.config_dir + '/uwsgi.conf', '/tmp/uwsgi.conf')
    sudo('mv /tmp/uwsgi.conf /etc/init/uwsgi.conf')

    with settings(warn_only=True):
        # create symlinks for emperor to find config file
        sudo('ln -s %s/uwsgi.ini /etc/uwsgi/vassals' % env.project_dir)

    sudo('chown -R www-data:www-data /var/log/uwsgi')
    sudo('chown -R www-data:www-data ' + env.project_dir)

    # upload flask config
    with settings(warn_only=True):
        sudo('mkdir %s/instance' % env.project_dir)
    put(env.config_dir + '/config.py', '/tmp/config.py')
    sudo('mv /tmp/config.py %s/instance/config.py' % env.project_dir)

    # upload data files
    put('instance/data_budget.json', '/tmp/data_budget.json')
    sudo('mv /tmp/data_budget.json %s/instance/data_budget.json' % env.project_dir)
    put('instance/data_councillors.json', '/tmp/data_councillors.json')
    sudo('mv /tmp/data_councillors.json %s/instance/data_councillors.json' % env.project_dir)

    set_permissions()
    restart()
    return


def deploy():
    """
    Upload our package to the server.
    """

    # create application directory if it doesn't exist yet
    with settings(warn_only=True):
        if run("test -d " + env.project_dir).failed:
            # create project folder
            sudo('mkdir -p ' + env.project_dir)

    # create a tarball of our package
    local('tar -czf frontend.tar.gz frontend/', capture=False)

    # upload the source tarball to the temporary folder on the server
    put('frontend.tar.gz', '/tmp/frontend.tar.gz')

    # enter application directory
    with cd(env.project_dir):
        # and unzip new files
        sudo('tar xzf /tmp/frontend.tar.gz')

    # now that all is set up, delete the tarball again
    sudo('rm /tmp/frontend.tar.gz')
    local('rm frontend.tar.gz')

    sudo('touch %s/frontend/uwsgi.sock' % env.project_dir)

    # clean out old logfiles
    with settings(warn_only=True):
        sudo('rm %s/frontend/debug.log*' % env.project_dir)

    set_permissions()
    restart()
    return


