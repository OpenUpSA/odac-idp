from fabric.api import *

"""
Define the server environments that this app will be deployed to.
Ensure that you have SSH access to the servers for the scripts in 'fabfile.py' to work.
"""


def production():
    """
    Env parameters for the staging environment.
    """

    env.hosts = ["root@5.9.195.1"]
    env.project_dir = '/var/www/idp.code4sa.org'  # the directory where the application resides on the server
    env.config_dir = 'config'  # the local directory where the config files for this server is kept
    env.env_dir = env.project_dir + "/env"  # path to this app's virtualenv (important if it runs on a shared server)
    env.activate = 'source %s/env/bin/activate' % env.project_dir
    return


def staging():
    """
    Env parameters for the staging environment.
    """

    env.hosts = ["root@5.9.195.6"]
    env.project_dir = '/var/www/idp.code4sa.org'  # the directory where the application resides on the server
    env.config_dir = 'config'  # the local directory where the config files for this server is kept
    env.env_dir = env.project_dir + "/env"  # path to this app's virtualenv (important if it runs on a shared server)
    env.activate = 'source %s/env/bin/activate' % env.project_dir
    return