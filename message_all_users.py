import sqlite3
import twilio
import os
import sys

class TwilioMessage():

    def __init__(self):

        path = os.path.abspath(__file__)
        while path[-1] != "/":
            path = path[:-1]

        self.path = path

        # load twilio settings from cfg file
        # bitbucket doesn't have twilio config settings, ask kevin for the file
        # it's not tracked because it contains passwords and things
        twilio_cfg_path = self.path + 'config/app.cfg'
        #config.read(twilio_cfg_path)
        execfile(twilio_cfg_path, self.__dict__)

        self.account          = twilio.Account(self.ACCOUNT_SID,
                                               self.ACCOUNT_TOKEN)
        self.outgoing_sms_url = "".join(["/", self.API_VERSION, "/Accounts/",
                                             self.ACCOUNT_SID, "/SMS/Messages"])

    def send_message_to_all_users(self, message):
        '''grab all numbers from the database, and send the selected message.'''

        # sometimes script runs as cron, sometimes manually,
        # want to take care of both cases.
        in_use_db = self.path + "database/goodmorning.db"
        connection = sqlite3.connect(in_use_db)
        cur = connection.execute("select * from phoneno")
        number_list = cur.fetchall()
        cur.close()
        connection.close()

        # hold phone numbers we've already seen
        d = {}

        for pair in number_list:
            number = pair[0]
            if d.has_key(number):
                # we've texted this person already
                continue

            # else send the message
            d[number] = True
            error_if_any = self.send_message_to_one_user(message, number)
            if error_if_any != "Success":
                print error_if_any

    def send_message_to_one_user(self, message, number):
        # build text message
        the_sms = {
            "From" : self.CALLER_ID,
            "To"   : number,
            "Body" : message
        }
        error_if_any = "Success"
        try:
            self.account.request(self.outgoing_sms_url, "POST", the_sms)
        except Exception:
            error_if_any = sys.exc_info()
        return error_if_any
