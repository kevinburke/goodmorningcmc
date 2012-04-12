from datetime import date
import sqlite3
import calendar
import urllib2
from BeautifulSoup import BeautifulStoneSoup
import os
import sys


weather_url = 'http://www.google.com/ig/api?weather=91711'
weather_url_opened = urllib2.urlopen(weather_url)
weather_xml = BeautifulStoneSoup(weather_url_opened.read())
weather_img_url = 'http://www.google.com'

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday']
today = date.today()
day_int = calendar.weekday(today.year, today.month, today.day)
the_day = days[day_int]

for day in weather_xml('forecast_conditions'):
    if day.day_of_week['data'] == the_day[:3]:
        low = day('low')[0]['data']
        high = day('high')[0]['data']
        img = weather_img_url + day('icon')[0]['data']
        print img
        cond = day('condition')[0]['data']
        print cond

path = os.path.abspath(os.path.dirname(sys.argv[0]))
db_name = path + "/database/goodmorning.db"
con = sqlite3.connect(db_name)
con.execute("delete from weather")
con.execute("insert into weather(image_url, high, low, condition) values(?,?,?,?)",  (img, high, low, cond))
con.commit()
con.close()
print "high was " + high
print "completed"
