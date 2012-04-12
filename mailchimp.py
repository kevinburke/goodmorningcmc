from build.mailsnake.mailsnake import MailSnake
import run
import os
import my_time
import sys

API_KEY = run.APP.config['MAILCHIMP_API_KEY']

# might want to put this in config file
GMSCRIPPS_ID = "906a4c0ae2"
GMPOMONA_ID  = "472e3695b1"
GMCMC_ID     = "2f72f64ad3"

list_name_to_site = {'Good Morning Scripps' : 'scripps',
                     'Good Morning CMC'     : 'cmc',
                     'Good Morning Pomona'  : 'pomona'}

def main(month, day):

    ms = MailSnake(API_KEY)
    lists = ms.lists()

    print "What is the subject line?"
    subject_line = raw_input()

    send_ids = {}

    for li in lists['data']:
        email_name = li['name']
        site = list_name_to_site[email_name]
        options = {'list_id'        : li['id'],
                    'subject'       : subject_line,
                    'title'         : month + "_" + str(day) + "_" + site,
                    'auto_footer'   : False,
                    'generate_text' : True,
                    'auto_tweet'    : True,
                    'from_email'    : li['default_from_email'],
                    'from_name'     : li['default_from_name']
                   }
        path_to_html_email = os.path.join("static", site, month,
                                          str(day), 'index.html')
        with open(path_to_html_email) as html_file:
            html_cont = html_file.read()

        content = {'html' : html_cont}
        camp_id = ms.campaignCreate(apikey = API_KEY, type = "regular",
                                    options = options, content = content)

        send_ids[site] = camp_id
        print "Created campaign for " + site + "..."

    # want to send or schedule
    # if current time is later than 7:15 am on scheduled day:
    today          = my_time.get_day_of_month()
    the_curr_month = my_time.get_month()
    hour           = my_time.get_hour()
    minute         = my_time.get_minute()
    # is today greater than 7:15 on send day?
    if (today >= day or the_curr_month != month) and \
       (hour > 7 or (hour == 7 and minute > 15)):
        # want to send now
        print "Send email now? Type yes"
        response = raw_input()
        if response != "yes":
            print "Ok - go to mailchimp.com and schedule manually"
            return
        else:
            print "Sending all emails..."
            all_successful = True
            for campaign_id in send_ids.values():
                all_successful = all_successful and \
                    ms.campaignSendNow(apikey = API_KEY, cid = campaign_id)
            if not all_successful:
                print "Uhoh, there were some errors in email sends."
            else:
                print "Campaigns sent successfully!"
    else:
        # ask to schedule
        # XXX handle daylight savings time soon.
        print "".join(["Schedule email for 7:15 PST (14:15 GMT) on ", month, " ",
                       str(day), "? Type yes"])
        response = raw_input()
        if response != "yes":
            print "Ok - aborting, go to mailchimp.com and schedule manually"
            return
        else:
            print "".join(["Scheduling all emails for 7:15 PST (14:15 GMT) on ",
                           month, " ", str(day)])
            all_successful = True
            # time needs to be in YYYY-MM-DD HH:II:SS format
            year = my_time.get_year()
            the_month = my_time.get_month(need_2digit = True, month = month)
            the_day = my_time.get_day_of_month(day, need_2digit = True)
            optimal_send_time = "14:15:00"
            the_time = "".join([str(year), "-", str(the_month), "-",
                                str(the_day), " ", optimal_send_time])
            for campaign_id in send_ids.values():
                all_successful = all_successful and \
                ms.campaignSchedule(apikey = API_KEY, cid = campaign_id,
                                    schedule_time = the_time)
            if not all_successful:
                print "Uhoh, there were some errors in scheduling emails."
            else:
                print "Campaigns scheduled successfully!"

# copied from create_email
# to do: add flags for specific sites, other html files
# or maybe they're rare enough that it's not worth it
if __name__ == "__main__":
    # check sys.argv to make sure array access is valid
    if len(sys.argv) > 1:
        month = sys.argv[1]
        day = int(sys.argv[2])
    else:
        print "Enter month (currently " + \
                    my_time.get_month() + "):"
        month = raw_input()
        print "Enter day (currently " + str(my_time.get_day_of_month()) + "):"
        day = int(raw_input())
    main(month, day)
