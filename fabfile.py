# -*- coding: utf-8 -*-
import datetime
import os

from fabric.api import run, cd, env, shell_env, local, settings, hide, prefix, sudo, lcd
from fabric.colors import red, green, yellow, white, blue


def banner(env):
    dev = yellow("""
    ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██╔════╝██║   ██║
    ██║  ██║█████╗  ██║   ██║
    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██████╔╝███████╗ ╚████╔╝
    ╚═════╝ ╚══════╝  ╚═══╝
    """)
    prod = red("""
    ██████╗ ██████╗  ██████╗ ██████╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
    ██████╔╝██████╔╝██║   ██║██║  ██║
    ██╔═══╝ ██╔══██╗██║   ██║██║  ██║
    ██║     ██║  ██║╚██████╔╝██████╔╝
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
    """)
    if env in ('development', 'production'):
        print(dev if env == 'development' else prod)


# def dev():
#     env.hosts = ['XX.XX.XX.XX']
#     env.name = 'development'
#     env.project_name = 'project_core'
#     env.user = env.project_name
#     env.db_name = env.project_name
#     env.port = 337
#     env.shell = '/bin/sh -c'
#     env.project_dir = '/home/{0}/{0}/{0}/'.format(env.project_name)
#     env.run_dir = '/home/{}/run/'.format(env.project_name)
#     env.backup_dir = '/home/{}/backups/'.format(env.project_name)
#     env.env = 'env'
#     env.env_path = '/home/{0}/{0}/{1}/'.format(env.project_name, env.env)
#     env.branch = 'development'
#     env.conf_path = './contrib/configurations/{}/'.format(env.name)
#     env.requirements_file = './requirements/requirements_{}.txt'.format(env.name)
#     env.django_settings_module = '{}.settings.local'.format(env.project_name)
#     env.activate = '. {}bin/activate'.format(env.env_path)
#     env.allow_fast_deploy = True


def prod():
    env.hosts = ['195.123.216.14']
    env.name = 'production'
    env.project_name = 'project_core'
    env.user = env.project_name
    env.db_name = env.project_name
    env.port = 337
    env.shell = '/bin/sh -c'
    env.project_dir = '/home/{0}/{0}/{0}/'.format(env.project_name)
    env.run_dir = '/home/{}/run/'.format(env.project_name)
    env.backup_dir = '/home/{}/backups/'.format(env.project_name)
    env.env = 'env'
    env.env_path = '/home/{0}/{0}/{1}/'.format(env.project_name, env.env)
    env.branch = 'master'
    env.conf_path = './contrib/configurations/{}/'.format(env.name)
    env.requirements_file = './requirements/requirements_{}.txt'.format(env.name)
    env.django_settings_module = '{}.settings.local'.format(env.project_name)
    env.activate = '. {}bin/activate'.format(env.env_path)
    env.allow_fast_deploy = False


def check_python():
    with settings(warn_only=True):
        local('flake8 --ignore=E501 --exclude=migrations --max-line-length=120 --statistics --exit-zero .')


def check():
    check_python()


def reset():
    print blue('* Reset')
    with cd(env.project_dir):
        with hide('running', 'stdout', 'stderr'):
            print green("  Reset uncommited changes made to source code..."),
            run('git reset --hard')
            print green("DONE")


def sync():
    print blue('* Sync')
    with cd(env.project_dir):
        with hide('running', 'stdout', 'stderr'):
            print green("  Sync code from remote repository into branch `{}`...".format(env.branch)),
            run('git pull --ff-only -u origin {}'.format(env.branch))
            print green("DONE")


def ramona(command):
    with cd(env.project_dir):
        with prefix(env.activate):
            return run('./{}.py -c {}ramona.conf '.format(env.project_name, env.conf_path) + command, pty=False)


def restart_django():
    ramona("restart django")


def restart_tornado():
    ramona("restart tornado")


def restart_all():
    print blue('* Application')
    with hide('running', 'stdout', 'stderr'):
        print green("  Restart application processes... ")
        output = ramona("restart")
        for line in output.split('\n'):
            print "\t\t" + yellow(line)
        print green("  ...DONE")


def restart_nginx():
    print blue('* Nginx')
    with hide('running', 'stdout', 'stderr'):
        print green("  Restarting nginx... "),
        sudo("service nginx restart", shell=False)
        print green("DONE")


def django(command):
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        with cd(os.path.join(env.project_dir, 'django')):
            run(os.path.join(env.env_path, 'bin/python') + ' manage.py ' + command, pty=False)


def virtualenv(command):
    run(os.path.join(env.env_path, 'bin/') + command, pty=False)


def collectstatic():
    print blue('* Static files')
    with hide('running', 'stdout', 'stderr'):
        print green("  Syncing static files... "),
        django('collectstatic --noinput')
        print green("DONE")


def syncdb_migrate():
    print blue('* Migrate DB')
    with hide('running', 'stdout', 'stderr'):
        print green("  Apply database changes... "),
        django('migrate --noinput')
        print green("DONE")


def sync_requirements():
    print blue('* Sync requirements')
    with cd(env.project_dir):
        with shell_env(PIP_DOWNLOAD_CACHE='~/.pip-cache'):
            with hide('running', 'stdout', 'stderr'):
                print green("  Installing python packages from {}... ".format(env.requirements_file)),
                run(os.path.join(env.env_path, 'bin/pip') + ' install -U -r ' + env.requirements_file)
                print green("DONE")


def backup_maintenance(days=30):
    print blue('* Backup directory maintenance')
    # Remove files older than `days` days in case there is more recent backup files.
    BACKUPS_TO_KEEP = 3
    BACKUP_FILES = 2
    REMOVE_FILES_OLDER_THAN = days
    with hide('running', 'stdout', 'stderr'):
        with cd(env.backup_dir):
            count_new = int(run('find . -type f -name "*" -mtime -{} -print | wc -l'.format(REMOVE_FILES_OLDER_THAN), pty=False))
            count_old = int(run('find . -type f -name "*" -mtime +{} -print | wc -l'.format(REMOVE_FILES_OLDER_THAN), pty=False))
            # Each backup contain 4 files: db, git id, 2 blog db.
            # We will try to keep at least 3 backups.
            if count_new > BACKUP_FILES * BACKUPS_TO_KEEP and count_old > 0:
                print yellow('  Backup directory need to be cleaned: will remove {} files older than {} days.'.format(count_old, REMOVE_FILES_OLDER_THAN)),
                run('find . -type f -name "*" -mtime +{} | xargs rm'.format(REMOVE_FILES_OLDER_THAN))
                print yellow('DONE')
            else:
                print yellow("  Nothing to cleanup.")

            # This will remove all empty directories
            run('find . -depth -type d -empty \( ! -name labels \) -prune -exec rmdir {} \;')
            # This will remove all links to non existing directories;
            with cd(os.path.join(env.backup_dir, 'labels')):
                run('find . -type l -xtype l -delete')


def backup(label=None):
    print blue('* Backup')
    now = datetime.datetime.now()
    backup_dir_exact = os.path.join(env.backup_dir, '{}'.format(now.strftime('%Y/%m/%d/%H-%M')))

    def backup_path(filename):
        return os.path.join(backup_dir_exact, filename)

    with hide('stderr'):
        with cd(env.backup_dir):
            run('mkdir -p {}'.format(backup_dir_exact))
            if label:
                run('mkdir -p labels')
                run('ln -s {} labels/{}-{}'.format(backup_dir_exact, label.replace(' ', '-'), now.strftime('%Y-%m-%d-%H%M')))

        with cd(env.project_dir):
            # IMPORTANT: If new files will be added to backup, it is necessary to increase
            # `BACKUP_FILES` constant in `backup_maintenance` function.
            print green("  Git revision... "),
            run('git rev-parse HEAD > {}'.format(backup_path('git.id')))
            print green("DONE")

            print green("  Database... "),
            if env.name == 'production':
                run('pg_dump -O -c {} | gzip -4 > {}'.format(env.db_name, backup_path('database.dump.gz')))
            # elif env.name == 'development':
            #     pass
            else:
                print red("Unknown environment")
            print green("DONE")

    run('ls -lah {}'.format(backup_dir_exact))


def managepy(command):
    """
    Remotely run manage.py command. If command require some options, call is as: fab test managepy:\"collectstatic -l\"
    """
    django(command)


def tailf_log(file='django', grep=None):
    grep = " | grep {}".format(grep) if grep else ""
    with cd(env.project_dir):
        run('tail -f logs/{}.log{}'.format(file, grep))


def tail(file='django', num=40):
    with cd(env.project_dir):
        run('tail -n {} logs/{}.log'.format(file, num))


def __version():
    with lcd(os.path.dirname(env.real_fabfile)):
        current_version = local('cat django/{}/__init__.py'.format(env.project_name), capture=True)
        current_version = current_version.replace("VERSION =", "").replace("(", "").replace(")", "").strip()
        major, minor, patch = [int(x.strip()) for x in current_version.split(",")]
        return major, minor, patch


def version():
    """
    `version` is used to display current version of application.
    """
    major, minor, patch = __version()
    print(green("v{}.{}.{}".format(major, minor, patch)))


def bump(new_version=None):
    """
    `bump` is used to increate current version.

    Next rules are work:

    - you can provide version as argument for command (ex: fab bump:3.1) in this case,
      we will set to zero all not provided bits. So that in example below, we will have version 3.1.0
    - you can not provide any argument in this case if you inside stable or hotfix branches,
      patch bit will be increased. If you inside develop or feature branch, minor bit will be updated.

    After you apply this command you need manually commit file with updated version.
    """
    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        major, minor, patch = __version()
        print(red("v{}.{}.{}".format(major, minor, patch))),
        if new_version is None:
            current_branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
            if current_branch == "develop" or current_branch.startswith('feature/'):
                minor += 1
            elif current_branch == "master" or current_branch.startswith('hotfix/'):
                patch += 1
        else:
            bits = new_version.split(".")
            major, minor, patch = map(lambda i, j: i if i else j, bits, [0, 0, 0])
        new_version_text = "({}, {}, {})".format(major, minor, patch)
        print("->"),
        print(green("v{}.{}.{}".format(major, minor, patch)))
        with lcd(os.path.dirname(env.real_fabfile)):
            local("sed -i -e 's/VERSION = .*/VERSION = {}/' django/{}/__init__.py".format(new_version_text, env.project_name), capture=True)


def _get_param_bool_value(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, basestring):
        value = value.lower()
        if value in ('off', 'false', 'no', '0'):
            return False
        elif value in ('on', 'true', 'yes', '1'):
            return True

    return default


def deploy(is_backup=True, is_collectstatic=True):
    """
    usage examples:
    ./fab dev deploy:is_backup=false - no backup
    ./fab dev deploy:is_backup=no - no backup
    ./fab dev deploy:off - no backup
    ......
    ./fab dev deploy:on - with backup
    ./fab dev deploy - with backup
    .....
    :param is_backup: true, false, on, off, 1, 0, yes, no
    :return: str commands output during deployment
    """
    is_backup = _get_param_bool_value(is_backup)
    is_collectstatic = _get_param_bool_value(is_collectstatic)

    banner(env.name)

    if is_backup:
        backup()

    backup_maintenance(30)
    reset()
    sync()
    sync_requirements()
    syncdb_migrate()

    if is_collectstatic:
        collectstatic()

    restart_all()
    restart_nginx()


def fastdeploy():
    if env.allow_fast_deploy:
        deploy(is_backup=False, is_collectstatic=False)
    else:
        print(red("Only environments with `allow_fast_deploy=True` support fast deployment. That is made for some sense!"))
