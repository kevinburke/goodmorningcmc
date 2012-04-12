"""Deploy the site to the server. To run, type 'fab prod deploy'
from anywhere in the Terminal. You need to have Fabric installed - try
either 'port install fabric' or 'pip install fabric'."""
from fabric.api import run, env, local, require, put, cd
import os
from datetime import datetime
import subprocess
from fabric.context_managers import show

REMOTE_HG_PATH = "/home/kevinburke/bin/hg"

#get mercurial root dir
#returns mercurial root dir with a newline at end
LOCAL_HG_PATH  = os.popen("hg root").read()[:-1]

def prod():
    '''set target to production.

    will be more useful when i have a test app, haha
    '''
    with show('everything', 'debug'):
        env.hosts                     = ['kevinburke.webfactional.com']
        env.user                      = 'kevinburke'
        if os.name == "nt":
            env.key_filename          = ["C:\Users\Orlan Davies\My Dropbox\Work\goodmorningcmc\priv.ppk"]
        env.remote_5c_dir             = '~/webapps/goodmorning5c'

def deploy():
    '''deploy the site.
    '''
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']
    today = datetime.today()
    the_month = months[today.month - 1]

    print "Update latest? If yes enter date (today is " + the_month + " " + \
            str(today.day) + "):"
    date = raw_input().split()
    if date[0] != 'no':
        # we're trying to update the file. let's check that the file actually is
        # in the repo.
        # we're lazy and check only if cmc. likely that if it's updated, others
        # are also updated
        file_path = os.path.join('static', 'cmc', date[0], date[1], 'index.html')
        pipe = subprocess.Popen(
            ['hg', 'st', file_path],
            stdout=subprocess.PIPE
        )
        response = pipe.stdout.read()
        if response:
            if response[0] == 'A':
                print "You need to add " + file_path + " to the repository." + \
                    " Try typing \n\n hg add static\nhg ci -m 'add index.html file for may 4'"
            else:
                print "The HTML file isn't tracked, or it's been modified. " + \
                        "Try \n\nhg ci -m \"made small change\"" + \
                        "\n\nat the command line."
            return

    os.system("hg push")

    require('hosts'              , provided_by=[prod])
    require('remote_5c_dir'      , provided_by=[prod])

    with cd(env.remote_5c_dir):
        run("hg pull && hg update")
        if date[0] != "no":
            # XXX this needs to be fixed - need to copy in three copies of
            # the file, one for cmc,
            # XXX same statement three times - should really be in a for
            # loop
            run("rm -f templates/latest_cmc.html")
            run("cp -v static/%s/%s/%s/index.html templates/latest_cmc.html" %
                ("cmc", date[0], date[1]))
            run("cp -v static/%s/%s/%s/index.html templates/latest_pomona.html" %
                ("pomona", date[0], date[1]))
            run("cp -v static/%s/%s/%s/index.html templates/latest_scripps.html" %
                ("scripps", date[0], date[1]))
        run ("apache/bin/apachectl -k restart")

