#!/usr/bin/env python
import xml.etree.ElementTree as etree
import urllib2
import sys
import os
import codecs
import yaml
import time

import my_time

# tab character
t = "\t"

#html line break
br = '<br />'

indent_level = 0
sites = ['cmc', 'pomona', 'scripps']
survey_url = "http://survey.io/survey/5b4c8"

snack_url = 'http://specials.cafebonappetit.com/baXML.asp?cafeid=228'

def main(month, day):
    global indent_level, t, br

    day_int = my_time.get_day_of_week(want_index = True, month = month,
                                      day = day)
    the_day = my_time.get_day_of_week(want_lowercase = False, month = month,
                                      day = day)
    if day_int > 4:
        print "Warning: running Good Morning CMC for weekend " + the_day

    current_day = my_time.get_day_of_month()
    current_month_ind = my_time.get_month(want_index = True)
    wanted_day = my_time.get_day_of_month(day = day)
    wanted_month_ind = my_time.get_month(want_index = True, month = month)

    if current_month_ind > wanted_month_ind or wanted_day > current_day:
        # then
        print "today is " + my_time.get_month(want_lowercase = False) + " " + str(current_day) + \
            ", but you are running email for " + month + " " + str(day)
        print "type ok or enter new day"
        # new month is rare case
        user_input = raw_input()
        print user_input
        if user_input not in ["OK", "ok"]:
            day = int(user_input)

    if current_day < wanted_day or current_month_ind < wanted_month_ind:
        print """Warning: running Good Morning CMC a day (or more) before
        email will run. The snack menu will not be accurate. Wait until after
        midnight for an accurate menu, or add correct snack manually."""
        time.sleep(3)

    #need to store this in a variable
    for site in sites:
        print "Creating email for " + site + "..."
        path_to_index_dir = os.path.join("static", site, month, str(day))
        if not os.path.isdir(path_to_index_dir):
            os.makedirs(path_to_index_dir)

        path_to_create_dir = "create"

        # codecs helps w/ unicode
        with codecs.open(os.path.join(path_to_index_dir, "index.html"),
                         mode='w', encoding="utf-8") as f:

            fw(f, '<html>')
            indent_level += 1
            fw(f, '<head>')
            indent_level += 1
            # set unicode
            fw(f, """<meta http-equiv="Content-Type" Content="text/html;
            charset=UTF-8">""")
            # this css sets the correct width for iphones - if the image is
            # 600px wide, it will zoom out the text
            fw(f, """<style>
            @media only screen and (max-device-width: 480px) {
                #hours{
                    width:300px;
                }
            }
        </style>""")
            indent_level -= 1
            fw(f, '</head>')
            fw(f, '<body>')
            indent_level += 1
            fw(f, "".join(['<title>', the_day, ", ", month.capitalize(), " ", str(day), " - Good Morning " + site.capitalize() + "</title>"]))
            fw(f, '<style>body{font-family:Helvetica, Helvetica Neue, Arial, sans-serif;} #ad a { color: #0000ff; } b {font-family:Helvetica Neue, Helvetica, Arial, sans-serif;}</style>')
            fw(f, '')

            # ad script
            ad_file_name = "".join([site, "_ads", ".html"])
            with codecs.open(os.path.join(path_to_create_dir, ad_file_name),
                             encoding="utf-8", errors='ignore') as ads_file:
                ads = ads_file.read()

            fw(f, '<div id="ad" style="background-color:#ddd; padding:15px; margin-bottom:10px;">' + ads + '<div style="clear:both;"></div></div>')
            fw(f, '')
            fw(f, "".join(['<div id="inbrowser" style="padding-bottom:30px;"><a href="http://goodmorning' + site + '.com/static/', site, "/", month, "/", str(day), "/",
                          '">View this email in your browser</a></div>']))
            fw(f, '<a href="http://www.facebook.com/sharer.php?u=http://goodmorning' + site + '.com&t=Good%20Morning%20' + site.capitalize() + '">Like on Facebook</a>')

            with codecs.open(os.path.join(path_to_create_dir,
                                          site + '_message.html'),
                             encoding="utf-8", errors='ignore') as message_file:
                message = message_file.read()

            if message:
                fw(f, "".join([br*2, message]))

            fw(f, "<h3>Events on campus</h3>")

            #todo:add events parsing from Google Calendar
            #for now, just adding manually
            fw(f, '')
            fw(f, "<ul>")
            with codecs.open(os.path.join(path_to_create_dir , 'events.yaml'),
                             encoding="utf-8", errors='ignore') as events_file:
                events = yaml.load(events_file)

            if events.has_key(site):
                for event in events[site]:
                    fw(f, "<li>" + event + "</li>")

            if events.has_key('5c'):
                for event in events['5c']:
                    fw(f, "<li>" + event + "</li>")

            fw(f, "</ul>\n")

            if events.has_key('saturday'):
                fw(f, "\n<b>Saturday</b><br><br>")
                fw(f, "<ul>")
                for event in events['saturday']:
                    fw(f, "<li>" + event + "</li>")
                fw(f, "</ul>")

            if events.has_key('sunday'):
                fw(f, "\n<b>Sunday</b><br><br>")
                fw(f, "<ul>")
                for event in events['sunday']:
                    fw(f, "<li>" + event + "</li>")
                fw(f, "</ul>")

            with codecs.open(os.path.join(path_to_create_dir, 'talks.yaml'),
                             encoding="utf-8", errors='ignore') as talks_file:
                talks = yaml.load(talks_file)

            if talks:

                fw(f, "<h3>Talks</h3>")

                fw(f, "<ul>")
                if talks.has_key(site):
                    for talk in talks[site]:
                        fw(f, "<li>" + talk + "</li>")

                if talks.has_key('5c'):
                    for talk in talks['5c']:
                        fw(f, "<li>" + talk + "</li>")

                fw(f, "</ul>\n\n")

            with codecs.open(os.path.join(path_to_create_dir, 'deadlines.yaml'),
                             encoding="utf-8", errors='ignore') \
                    as deadlines_file:
                deadlines = yaml.load(deadlines_file)

            # refactor this - shouldn't print deadlines if there are no relevant
            # ones
            if deadlines:
                fw(f, "<h3>Deadlines</h3>")
                fw(f, "<ul>")
                if deadlines.has_key(site):
                    for deadline in deadlines[site]:
                        fw(f, "<li>" + deadline + "</li>")

                if deadlines.has_key('5c'):
                    for deadline in deadlines['5c']:
                        fw(f, "<li>" + deadline + "</li>")

                fw(f, "</ul>")


            if site == 'cmc':
                fw(f, "<h3>Athenaeum</h3>")
                fw(f, '')

                with codecs.open(os.path.join(path_to_create_dir, 'ath.yaml'),
                                 encoding="utf-8", errors='ignore') as ath:
                    ath_data = yaml.load(ath)

                if ath_data:
                    if ath_data.has_key('lunch'):
                        fw(f, "<b>Lunch: </b>" + ath_data['lunch'] + br*2)
                        fw(f, "Lunch begins at 11:30, and the program begins at noon." + br*2)

                    if ath_data.has_key('dinner'):
                        fw(f, "<b>Dinner: </b>" + ath_data['dinner'] + br*2)
                        fw(f, "Ath opens at 5:30; dinner is at 6, and the program begins at 6:45." + br*2)

                fw(f, "".join(['Place reservations <a href="',
                               'http://www.claremontmckenna.edu/mmca/cur_reserve.php">here</a>,',
                               ' or check out the ',
                               '<a href="http://www.claremontmckenna.edu/mmca/cur_spring_11.php">',
                               'full list of speakers for the spring 2011 semester.</a>']))
            fw(f, '')
            # want to load these from file so we're not repeating, but
            # patience for now
            fw(f, "<h3>The world today</h3>")

            with codecs.open(os.path.join(path_to_create_dir, 'links.yaml'),
                             encoding="utf-8", errors='ignore') as links_file:
                links = yaml.load(links_file)

            for link in links['links']:
                if link.has_key("just_text"):
                    fw(f, link["just_text"] + br*2)
                else:
                    link_after = ""
                    if link.has_key('after'):
                        link_after = link['after']
                    fw(f, "".join(["<a href='", link['href'], "'>", link['text'],
                                   "</a> ", link_after, br*2]))
            fw(f, '<a href="http://slatest.slate.com/">The 12 hottest stories around the world right now</a>' + br*2)
            fw(f, "".join(['<a href="http://claremontcurrents.com/feed/">News from around the Claremonts</a> (requires RSS)', br*2]))
            fw(f, '')
            fw(f, "<h3>Weather</h3>")
            fw(f, '')

            weather_url = 'http://www.google.com/ig/api?weather=91711'
            try:
                weather_url_opened = urllib2.urlopen(weather_url)
            except Exception:
                print "could not connect to internet, weather not loaded"
                # should fail here
                return

            weather_img_url = 'http://www.google.com'
            weather_link = links['weather']
	    weather_file_contents = weather_url_opened.read()
            the_tree = etree.fromstring(weather_file_contents)

            for a_day in the_tree.findall(".//forecast_conditions"):
                if a_day.find('day_of_week').get('data') == the_day[:3]:
                    low = a_day.find('low').get('data')
                    high = a_day.find('high').get('data')
                    img_url = weather_img_url + a_day.find('icon').get('data')
                    cond = a_day.find('condition').get('data')

            fw(f, "".join(["<img id='weather_image_url' src=\"", img_url,
                           "\" style=\"float:left; padding-right:10px;\" width=\"48\"\
 height=\"48\" /><span id='weather_cond'>", cond,
                           "</span>, high <span id='weather_high'>", high,
                           "</span>, low <span id='weather_low'>", low,
                          "</span> with a ", str(weather_link['chance']),
                           "% chance that <a href='", weather_link['href'], "'>",
                           weather_link['text'], "</a>", br*2]))

            fw(f, '')
            fw(f, '<a href="http://www.wunderground.com/US/CA/Claremont.html">check out the 5-day forecast</a>')
            fw(f, '')

            flex_filename = 'flexhours.txt'
            #friday flex hours are different
            if the_day == "Friday":
                flex_filename = 'flex_weekend_hours.txt'

            with codecs.open(os.path.join(path_to_create_dir, flex_filename),
                             encoding="utf-8", errors='ignore') as flex_hours:
                fw(f, flex_hours.read())

            fw(f, "<h3>Dining Hall Hours</h3>")
            fw(f, '')

            fw(f, '<img id="hours" src="http://goodmorning' + site + '.com/static/hours.jpg" width="690" height="177" alt="To view, Click \'Always display images\' at the top of your email" />')
            fw(f, '')
            fw(f, "<h3>Dining Hall Menus</h3>")
            if site == 'cmc':
                fw(f, "".join(['<a href="http://www.cafebonappetit.com/collins-cmc/cafes/collins/weekly_menu3.html">Collins (CMC)</a>', br*2]))
                fw(f, "".join(['<a href="http://www.pomona.edu/dining/menus/frary.aspx">Frary (Pomona)</a>', br*2]))
                fw(f, "".join(['<a href="http://www.pomona.edu/dining/menus/frank.aspx">Frank (Pomona)</a>', br*2]))
            elif site == 'pomona':
                fw(f, "".join(['<a href="http://www.pomona.edu/dining/menus/frary.aspx">Frary (Pomona)</a>', br*2]))
                fw(f, "".join(['<a href="http://www.pomona.edu/dining/menus/frank.aspx">Frank (Pomona)</a>', br*2]))
                fw(f, "".join(['<a href="http://www.cafebonappetit.com/collins-cmc/cafes/collins/weekly_menu3.html">Collins (CMC)</a>', br*2]))
            fw(f, "".join(['<a href="http://www.scrippscollege.edu/students/dining-services/">Malott (Scripps)</a>', br*2]))
            fw(f, "".join(['<a href="http://www.hmcdining.com/dining/menus/week_1.html">Hoch-Shanahan (Harvey Mudd)</a>', br*2]))
            fw(f, "".join(['<a href="http://www.cafebonappetit.com/pitzer/mcconnell/">Pitzer</a> (menu unavailable)', br*2]))
            fw(f, '')
            if site == 'cmc':
                opened_url = urllib2.urlopen(snack_url)
                snack_xml = opened_url.read()
                the_tree = etree.fromstring(snack_xml)
                the_snack = the_tree.findall(".//txtTitle")
                if the_snack:
                    the_snack_element = the_snack[0]
                    if hasattr(the_snack_element, 'text'):
                        the_snack_text = the_snack_element.text
                        fw(f, '<h3>Snack</h3>')
                        fw(f, the_snack_text + "<br><br>")
                        fw(f, '<a href="http://goodmorningcmc.com/snack/">Sign up to receive the Snack menu on your phone, ten minutes before Snack</a><br><br>')
            fw(f, '')

            with codecs.open(os.path.join(path_to_create_dir, 'sports.yaml'),
                             encoding="utf-8", errors='ignore') as sports_file:
                sports_data = yaml.load(sports_file)

            # this code is ugly. refactor pronto
            relevant_sports_data = []
            if sports_data:
                fw(f, '<h3>Sports</h3>')
                if site in ['cmc', 'mudd', 'scripps']:
                    if sports_data.has_key('cms'):
                        relevant_sports_data = sports_data['cms']
                else:
                    if sports_data.has_key('pp'):
                        relevant_sports_data = sports_data['pp']

                if relevant_sports_data:
                    if type(relevant_sports_data) is list and \
                        type(relevant_sports_data[0]) is dict:
                        #we have "Last Night," "Tonight," etc
                        for i in relevant_sports_data:
                            fw(f, "<b>" + i.keys()[0] + "</b><br><br>")
                            for j in i.values()[0]:
                                fw(f, j + "<br><br>")

                    elif type(relevant_sports_data) is list:
                        for i in relevant_sports_data:
                            fw(f, i + "<br /><br />")


            imp_links_filename = os.path.join(path_to_create_dir,
                                              'important_links', site + '.txt')
            with codecs.open(imp_links_filename,
                      encoding="utf-8", errors='ignore') as important_links:
                fw(f, important_links.read())

            with codecs.open(os.path.join(path_to_create_dir, 'tagline.txt'),
                      encoding="utf-8", errors='ignore') as tagline_file:
                tagline = tagline_file.read()
            fw(f, "".join(['It\'s ', the_day, '. ', tagline]))
            fw(f, '<br><br><br><br>')
            fw(f, '<a href="' + survey_url + '">take our short survey</a><br><br>')
            fw(f, '<a href="http://goodmorning' + site + '.com/advertise/">Promote your event</a>')
            indent_level -= 1
            fw(f, '</body>')
            indent_level -= 1

            # load mailchimp "Sent to" info.
            # We can't use Mailchimps version because it sets the table width
            # too wide and destroys readability on mobile devices.
            with codecs.open(os.path.join(path_to_create_dir,
                                          'mailchimp_bottom_text.txt'),
                      encoding="utf-8") as mailchimp_file:
                mchimp_text = mailchimp_file.read()
            fw(f, "".join(["\n", mchimp_text, "\n"]))
            fw(f, '</html>')

        #open file for inspection, in a browser and in a text editor

        chromecmd = "open -a \"Google Chrome\" " + path_to_index_dir \
            + "/index.html"
        if (os.name == "nt"):
            chromecmd="start " + path_to_index_dir + "/index.html"
        else:         
            os.system("open -t " + path_to_index_dir + "/index.html")
        os.system(chromecmd)

        # add the new file to the repository
        os.system("hg add static")

def fw(f, text):
    f.write(t*indent_level + text + '\n')

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
