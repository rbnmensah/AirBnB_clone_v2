#!/usr/bin/python3
# Fabfile to distribute an archive to a web servers

import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["52.55.249.213", "54.157.32.137"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) == False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed == True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed == True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed == True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed == True:
        return False
    if run("rm /tmp/{}".format(file)).failed == True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed == True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed == True:
        return False
    if run("rm -rf /data/web_static/current").failed == True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed == True:
        return False
    return True
