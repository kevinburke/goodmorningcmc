#!~/bin/python
from flask import Flask, g, request
from flask import render_template
from flask import make_response
from flaskext.mail import Mail, Message
from contextlib import closing

from datetime import datetime
import socket
import sqlite3
import os
import yaml

from message_all_users import TwilioMessage

def init_db(app, db_path):
    '''initialize db with the given schema. WARNING: erases all data in db'''

    with closing(connect_db(db_path)) as datab:
        with app.open_resource(os.path.join('database', 'schema.sql')) as schema:
            datab.cursor().executescript(schema.read())
        datab.commit()

def connect_db(db_path):
    '''return a connection to the database'''
    return sqlite3.connect(db_path)

def get_execution_path():
    '''return absolute path to directory containing current file'''
    path_including_filename = os.path.abspath(__file__)
    # get a tuple (folder, filename)
    path_split_folder_name = os.path.split(path_including_filename)
    # we want the folder
    return path_split_folder_name[0]

def get_site_specific_info(db_path, site_name = "cmc"):
    '''load current site from db.

    db contains config info specific to each site, eg pomona scripps cmc.
    '''
    connection = connect_db(db_path)
    # this should be safe, i control the script name
    query = "select * from " + site_name
    cur = connection.execute(query)
    the_site = cur.fetchone()
    cur.close()
    connection.close()
    return the_site

def load_site_config(site_name = "cmc"):
    """Return a dict containing url, call to action, font color, font info, etc

    Load the correct dict from the yaml config file
    """
    (the_site_name, the_site_host, the_site_port) = \
        get_site_specific_info(DB_PATH, site_name)
    yml = yaml.load(open(os.path.join(EXC_PATH, "config", "site.yaml")))

    #name is first field in table
    the_site = yml[ the_site_name ]
    the_site['host'] = the_site_host
    the_site['port'] = the_site_port
    return the_site

APP = Flask(__name__)
EXC_PATH = get_execution_path()
# app.cfg located in goodmorningcmc/config/app.cfg
APP.config.from_pyfile(os.path.join(EXC_PATH, 'config', 'app.cfg'))
MAIL = Mail(APP)
DB_PATH = os.path.join(EXC_PATH, APP.config['DATABASE'][0], APP.config['DATABASE'][1])

# XXX this runs twice, once again when wsgi runs, need to fix
SITE = load_site_config()
SITE['the_date'] = datetime.now().strftime("%A, %B %d")

@APP.before_request
def before_request():
    '''initialize the database before responding to requests'''
    g.db = connect_db(DB_PATH)

@APP.after_request
def after_request(response):
    '''close db connection after request building finishes'''
    g.db.close()
    return response

@APP.route("/")
def index():
    '''serve the homepage'''
    weather = {}
    (weather['none'], weather['image_url'], weather['high'],
    weather['low'], weather['condition']) = \
            g.db.execute('select * from weather').fetchone()

    return render_template('mainpage.html', site=SITE, weather=weather)

@APP.route("/personals/")
def personals():
    """serve the personals page. just update fb settings"""
    SITE['og_title'] = "Personals at " + SITE['title']
    SITE['og_image'] = "firstdate.png"
    SITE['og_url'] = "http://" + SITE['base_url'] + "/personals/"
    SITE['og_description'] = "Dating for college students in Claremont, CA"
    return render_template("personals.html", site=SITE)

@APP.route("/snack/")
def snack():
    """serve the snack page. just update the fb settings"""
    SITE['og_title'] = "What's For Snack"
    SITE['og_image'] = "taquitos.jpg"
    SITE['og_url'] = "http://www.goodmorningcmc.com/snack/"
    SITE['og_description'] = "Get a text message with the snack menu at \
            10:15 every night. It's that easy."
    return render_template("snack.html", site=SITE)

@APP.route("/store/")
def store():
    """think I want to delete this soon"""
    return render_template("store.html", site=SITE)

@APP.route("/advertise/")
def advertise():
    """serve the ads page"""
    return render_template("advertise.html", site=SITE)

@APP.route("/faq/")
def faq():
    """serve the FAQ page"""
    return render_template("faq.html", site=SITE)

@APP.route("/css/<sitename>.css")
def css(sitename):
    """CSS contains some conditional templating based on site (colors etc.)"""
    response = make_response(render_template("style.css", site=SITE))
    response.headers['Content-Type'] = 'text/css'
    return response

@APP.route("/phoneno/", methods=["POST"])
def storephone():
    """phone number posted from snack. store it in db, send confirmation msg"""
    if SITE['name'] != "cmc":
        return render_template('404.html', site=SITE), 404
    elif request.method == "POST":
        phoneno = request.form['phone']
        connection = connect_db(DB_PATH)
        cur = connection.execute("insert into phoneno (phoneno) values (:no)",
                                 {"no": phoneno})
        cur.close()
        #commit the changes
        connection.commit()
        connection.close()
        msg = """Thanks for signing up for What's for Snack. Share with
 friends: http://bit.ly/cmcsnack. Unsub: reply 'u' to this number.
 - Kevin"""

        twimsg = TwilioMessage()
        error_if_any = twimsg.send_message_to_one_user(msg, phoneno)
        response = make_response(u'<html><body>'+ error_if_any
                                 + '</body></html>')
        return response

@APP.route("/twilio/sms/", methods=["POST"])
def recvsms():
    """if it's an unsubscribe message, delete name from db, else email text
    to me"""
    if SITE['name'] != "cmc":
        return render_template('404.html', site=SITE), 404
    user_number = request.form['From']
    the_text_content = request.form['Body']
    the_response = u'<html><body>Hire me please! <a \
            href="http://kburke.org/projects">Here\'s some cool stuff \
            I\'m working on.</a></body></html>'
    if the_text_content == "u" or the_text_content == "U" or \
        the_text_content == "'u'":

        #assume USA and strip leading plus and 1
        user_number = user_number[2:]
        import re
        phone_regex = str("(\()?" + user_number[:3] + '(\))?[ -]?' + \
                      user_number[3:6] + "[- ]?" + user_number[6:10] + "$")

        #pull all #s from db
        connection = connect_db(DB_PATH)
        number_list = connection.execute("select * from phoneno").fetchall()

        # don't send "Unsubscribed" message twice
        already_sent = False

        # pull all matching numbers and delete them from the db
        for pair in number_list:
            number = str(pair[0])

            # user could have entered their number in any one of a number of
            # formats
            if re.match(phone_regex, number):
                connection.execute("delete from phoneno where phoneno = :no",
                            {"no" : number} )
                msg = "Unsubscribed. Sorry to see you go - Kevin"
                if not already_sent:
                    #text message user
                    twimsg = TwilioMessage()
                    twimsg.send_message_to_one_user(msg, user_number)
                    already_sent = True

        connection.commit()
        connection.close()

        response = make_response(the_response)
        return response

    else:
        #want to email me the text contents
        recipients = ['kevin@goodmorning' + SITE['name'] + '.com']
        subject = "You got a text message about Snack"
        msg_body = "".join(["From: ", user_number, "\n", "Message: ",
                            the_text_content])
        sender = ("Kevin Burke", "kev@inburke.com")
        msg = Message(subject, recipients=recipients, body=msg_body,
                      sender=sender)
        MAIL.send(msg)
        response = make_response(the_response)
        return response

@APP.route("/googlea201d0fca52f349c.html")
def google_webmaster_tool():
    """for google webmaster tools site verification, leave it"""
    return render_template('googlea201d0fca52f349c.html')

@APP.route("/mail.php", methods=["POST"])
def mailphp():
    """handle event creation, email me"""
    if request.method == 'POST':
        name      = request.form['name']
        date      = request.form['date']
        the_event = request.form['the_event']
        msg_body = "".join(["New event created!\n\n", "Contact Name: ", name,
                            "\n\n", "Date: ", date, "\n\n",
                            "Event Description: ", "\n\n", the_event])
        the_subject = "New event for Good Morning " + \
                            SITE['name'].capitalize()
        recipients = ['kevin@goodmorning' + SITE['name'] + '.com',
                      'akakkar14@cmc.edu', 'sdavies13@cmc.edu']
        sender = ("Kevin Burke", "kev@inburke.com")
        msg = Message(the_subject, recipients=recipients, body=msg_body,
                      sender=sender)
        MAIL.send(msg)
        response = make_response(u'<html><body>Success</body></html>')
        return response

@APP.errorhandler(404)
def page_not_found(error_code):
    """serve 404"""
    print "serving 404..."
    return render_template('404.html', site=SITE), 404

if __name__ == "__main__":
    try:
        APP.run(host = SITE['host'], port = SITE['port'])
    except socket.error:
        print "An instance is already running on the port. Quitting."
