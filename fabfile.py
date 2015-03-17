# -*- encoding: utf8 -*-

#### Django deployment for Debian Based servers ######

from __future__ import unicode_literals
import re
import os
import getpass

from fabric.api import *
from fabric.contrib.files import exists, upload_template


env.cibb_repo = 'git@bitbucket.org:jvacx/cibb.git'

# App configuration

app = {
    "url"        : "cib-bolivia.com",
    "name"       : "cibb_app",
    "superuser"  : "jvacx",
    "user"       : "cibb_user",
    "group"      : "cibb_team",
    "path"       : "/webapps",
    "deps"       : [  # System's Packages dependencies
        "build-essential",
        "python",
        "python-setuptools",
        "python-virtualenv",
        "python-pip",
        "python-dev",
        "nginx",
        "gunicorn",
        "supervisor",
        "postgresql",
        "postgresql-contrib",
        "libpq-dev",
        "git",
        "zip",
        "rpl",
        "libjpeg-dev",
        "libfreetype6-dev",
        "zlib1g-dev",
    ],
}


# Database Configuration
DB_NAME = app["name"]
DB_USER = app["user"]
DB_PASS = "12345678x"

# Path configurations.
CONFIG_DIR = './config'  # Locally
NGINX_DIR = '/etc/nginx' # Remote
SUPERVISOR_DIR = '/etc/supervisor' # Remote

PROJECT_PATH = "%s/%s/%s"%(app["path"], app["user"], app["name"])
USER_HOME = "%s/%s"%(app["path"], app["user"])


# Servers configuration.
servers = {
    "production": {
        "domain": "104.236.57.9",
        "ssh_port": "22",
        "path": "/var/www/cibb",
        "branch": "master",
    },
    "stage": {
        "domain": "stage.jvacx.com:2290",
        "ssh_port": "2290",
        "path": "/var/www/cibb",
        "branch": "stage",
    },
    "develop": {
        "domain": "localhost",
        "ssh_port": "2290",
        "path": os.path.dirname(os.path.abspath(__file__)),
        "branch": "develop",
    },
}


## ~$ UTILS
####---------------------------------------------------------------------

class Server(object):
    @staticmethod
    def upgrade():
        sudo('apt-get update -y')
        sudo('apt-get upgrade -y')

    @staticmethod
    def deps():
        sudo('apt-get install -y %s' % ' '.join(app["deps"]))

    @staticmethod
    def restart_services():
        sudo('service nginx restart')
        sudo('service supervisor restart')
        sudo('supervisorctl restart %s'%app["name"])

    @staticmethod
    def clean():
        sudo('apt-get remove %s' % ' '.join(app["deps"]))


class Conf(object):
    @staticmethod
    def nginx():
        """
        1. Remove default nginx config file
        2. Create new config file
        3. Copy local config to remote config
        4. Setup new symbolic link
        5. Restart nginx
        """
        if exists('%s/sites-enabled/default'%NGINX_DIR):
            sudo('rm %s/sites-enabled/default'%NGINX_DIR)
        if exists('%s/sites-enabled/%s'%(NGINX_DIR,app["url"])):
            sudo('rm %s/sites-enabled/%s'%(NGINX_DIR,app["url"]))
        if exists('%s/sites-available/%s'%(NGINX_DIR,app["url"])):
            sudo('rm %s/sites-available/%s'%(NGINX_DIR,app["url"]))

        with lcd(CONFIG_DIR):
            with cd('%s/sites-available/'%NGINX_DIR):
                upload_template(
                    filename="./nginx.conf",
                    destination='%s/sites-available/%s'%(NGINX_DIR,app["url"]),
                    template_dir="./",
                    context={
                        "project_name": app["name"],
                        "project_path": PROJECT_PATH,
                        "project_url": app["url"],
                    },
                    use_sudo=True,
                )

        sudo('ln -s %s/sites-available/%s \
            %s/sites-enabled/'%(NGINX_DIR,app["url"],NGINX_DIR))

        # sudo('service nginx restart')


    @staticmethod
    def gunicorn():
        """
        1. Create new gunicorn start script
        2. Copy local start script template redered to server
        """

        sudo('rm -rf %s/bin'%PROJECT_PATH)
        sudo('mkdir -p %s/bin'%PROJECT_PATH)

        with lcd(CONFIG_DIR):
            with cd('%s/bin'%PROJECT_PATH):
                sudo('ls')
                upload_template (
                    filename='./start_prod.sh',
                    destination='%s/bin/start.sh'%PROJECT_PATH,
                    template_dir="./",
                    context={
                        "project_name": app["name"],
                        "project_path": PROJECT_PATH,
                        "app_user": app["user"],
                        "app_group": app["group"],
                    },
                    use_sudo=True,
                )
                sudo('chmod +x %s/bin/start.sh'%PROJECT_PATH)


    @staticmethod
    def supervisor():
        """
        1. Create new supervisor config file
        2. Copy local config to remote config
        3. Register new command
        """
        if exists('%s/conf.d/%s.conf'%(SUPERVISOR_DIR,app["name"])):
            sudo('rm %s/conf.d/%s.conf'%(SUPERVISOR_DIR,app["name"]))

        with lcd(CONFIG_DIR):
            with cd('%s/conf.d'%SUPERVISOR_DIR):
                upload_template(
                    filename="./supervisor.conf",
                    destination='./%s.conf'%app["name"],
                    template_dir="./",
                    context={
                        "project_name": app["name"],
                        "project_path": PROJECT_PATH,
                        "app_user": app["user"],
                    },
                    use_sudo=True,
                )
        sudo('supervisorctl reread')
        sudo('supervisorctl update')


    @staticmethod
    def git():
        """
        1. Setup bare Git repo
        2. Create post-receive hook
        """
        if exists(app["path"]) is False:
            sudo('mkdir %s' % app["path"])

        if exists(USER_HOME) is False:
            sudo("mkdir %s"%USER_HOME)

        if exists(PROJECT_PATH) is False:
            sudo("mkdir %s"%PROJECT_PATH)

        with cd(USER_HOME):
            sudo('mkdir -p %s.git'%app["name"])
            with cd('%s.git'%app["name"]):
                sudo('git init --bare')
                with lcd(CONFIG_DIR):
                    with cd('hooks'):
                        upload_template(
                            filename="post-receive",
                            destination=PROJECT_PATH+".git/hooks",
                            template_dir="./",
                            context={
                                "project_path": PROJECT_PATH,
                            },
                            use_sudo=True,
                        )
                        sudo('chmod +x post-receive')

            sudo('chown -R %s:%s %s.git'%(app["user"], app["group"], app["name"]))

    @staticmethod
    def add_remote():
        local('git remote remove %s'%env.remote)
        local('git remote add %s %s@%s:%s/%s.git'%(
            env.remote,app["user"], env.hosts[0], USER_HOME, app["name"],
        ))

    @staticmethod
    def roles():
        """
        1. Create app group
        2. Create app user
        3. Asociate user home
        4. Fix Permissions
        """
        # Create user and group
        sudo('groupadd --system %s'%app["group"])
        sudo('useradd --system --gid %s \
              --shell /bin/bash --home %s %s'
            % (app["group"], USER_HOME, app["user"]))

        # Create and asociate home to app user
        sudo('adduser %s sudo'%app["user"])
        sudo('mkdir -p %s'%USER_HOME)
        sudo('chown -R %s %s'%(app["user"],USER_HOME))
        sudo('chown -R %s:%s %s'%(
            app["user"],app["group"],
            PROJECT_PATH,
        ))
        sudo('chmod -R g+w %s'%PROJECT_PATH)

    @staticmethod
    def postgresql():
        """
        1. Create DB user
        2. Create DB and assign to user
        """
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER \
            ENCRYPTED PASSWORD E\'%s\'"' % (DB_USER, DB_PASS), user='postgres')
        sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"' % (
        DB_NAME, DB_USER), user='postgres')

    @staticmethod
    def fix_permissions():
        sudo('chown -R %s %s'%(app["user"],USER_HOME))
        sudo('chown -R %s:%s %s'%(
            app["user"], app["group"], PROJECT_PATH,
        ))
        sudo('chmod -R g+w %s'%PROJECT_PATH)

    @staticmethod
    def clean():
        """
        1. Delete app group
        2. Delete app user
        3. Delete related files
        4. Delete config files
        5. Delete DB and user DB
        """
        sudo('groupdel %s'%app["group"])
        sudo('userdel -r %s'%app["user"])
        if exists(PROJECT_PATH):
            sudo('rm -r %s'%PROJECT_PATH)
        if exists('%s/conf.d/%s.conf'%(SUPERVISOR_DIR,app["name"])):
            sudo('rm %s/conf.d/%s.conf'%(SUPERVISOR_DIR,app["name"]))
        if exists('%s/sites-enabled/%s'%(NGINX_DIR,app["name"])):
            sudo('rm %s/sites-enabled/%s'%(NGINX_DIR,app["name"]))
        if exists('%s/sites-available/%s'%(NGINX_DIR,app["name"])):
            sudo('rm %s/sites-available/%s'%(NGINX_DIR,app["name"]))
        sudo('dropuser %s' % DB_USER)
        sudo('psql -c "DROP DATABASE %s"' % DB_NAME, user='postgres')

class Project(object):

    @staticmethod
    def push():
        """Push cambios del repositorio al servidor principal"""
        local("git push %s %s" %(env.remote, env.branch) )

    @staticmethod
    def install():
        with cd(PROJECT_PATH):
            run("make install")

    @staticmethod
    def start():
        sudo("supervisorctl start %s"%app["name"])

    @staticmethod
    def restart():
        sudo("supervisorctl restart %s"%app["name"])

    @staticmethod
    def stop():
        sudo("supervisorctl stop %s"%app["name"])

    @staticmethod
    def clean_cache():
        with cd("%s/var/cache"%PROJECT_PATH):
            run("rm -r *")

    @staticmethod
    def clean_logs():
        with cd("%s/var/log"%PROJECT_PATH):
            run("rm -r *")

    @staticmethod
    def backup_db():
        with cd(env.path):
            with prefix('source env/bin/activate'):
                res = run("python manage.py backup_db")
                backup_name = re.search('Backup: (.+)', res).groups(0)[0]
                if 'download' in args:
                    get('var/backup/local/{0}'.format(backup_name), 'var/backup/remote/')

    @staticmethod
    def test():
        pass


def deploy(*args):
    """Deploy application on a server"""
    if len(args) <= 0:
        print_servers()
    for server in args:
        if server in servers.keys():
            env.user = app["user"]
            env.hosts = [servers[server]["domain"], ]
            env.path = servers[server]["path"]
            env.remote = server
            env.branch = servers[server]["branch"]
            with settings(warn_only=True):
                execute(Project.push, hosts=[servers[server]["domain"], ])
                # execute(Project.clean_logs, hosts=[servers[server]["domain"], ])
                # execute(Project.clean_cache, hosts=[servers[server]["domain"], ])
                execute(Project.install, hosts=[servers[server]["domain"], ])
                # execute(Project.restart, hosts=[servers[server]["domain"], ])
        else:
            print_servers()


def init(*args):
    """Init base of application on a server"""
    if len(args) <= 0:
        print_servers()
    for server in args:
        if server in servers.keys():
            env.user = app["superuser"]
            env.hosts = [servers[server]["domain"], ]
            env.path = servers[server]["path"]
            env.remote = server
            with settings(warn_only=True):
                HOST = "%s:%s" % (
                    servers[server]["domain"],
                    servers[server]["ssh_port"],
                )
                execute(Conf.clean, hosts=[HOST,])
                execute(Server.deps, hosts=[HOST,])
                execute(Conf.roles, hosts=[HOST,])
                execute(Conf.postgresql, hosts=[HOST,])
                execute(Conf.git, hosts=[HOST,])
                execute(Conf.add_remote, hosts=[HOST,])
                execute(Conf.nginx, hosts=[HOST,])
                execute(Conf.gunicorn, hosts=[HOST,])
                execute(Conf.supervisor, hosts=[HOST,])
                execute(Conf.fix_permissions, hosts=[HOST,])
        else:
            print_servers()

def clean(*args):
    """Clean app and related files od server"""
    if len(args) <= 0:
        print_servers()
    for server in args:
        if server in servers.keys():
            env.user = app["superuser"]
            env.hosts = [servers[server]["domain"], ]
            env.path = servers[server]["path"]
            with settings(warn_only=True):
                HOST = "%s:%s" % (
                    servers[server]["domain"],
                    servers[server]["ssh_port"],
                )
                execute(Conf.clean, hosts=[HOST,])
        else:
            print_servers()

def restart(*args):
    """ Restart app servers """
    if len(args) <= 0:
        print_servers()
    for server in args:
        if server in servers.keys():
            env.user = app["superuser"]
            env.hosts = [servers[server]["domain"], ]
            env.path = servers[server]["path"]
            with settings(warn_only=True):
                HOST = "%s:%s" % (
                    servers[server]["domain"],
                    servers[server]["ssh_port"],
                )
                execute(Server.restart_services, hosts=[HOST,])
                execute(Conf.fix_permissions, hosts=[HOST,])
        else:
            print_servers()


def add_remote(*args):
    """ Restart app servers """
    if len(args) <= 0:
        print_servers()
    for server in args:
        if server in servers.keys():
            env.user = app["superuser"]
            env.hosts = [servers[server]["domain"], ]
            env.path = servers[server]["path"]
            env.remote = server
            with settings(warn_only=True):
                HOST = "%s:%s" % (
                    servers[server]["domain"],
                    servers[server]["ssh_port"],
                )
                execute(Conf.add_remote, hosts=[HOST,])
        else:
            print_servers()

def print_servers():
    print "Available servers:"
    for server in servers.keys():
        print "   - "+server