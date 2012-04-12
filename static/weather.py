import urllib2
from BeautifulSoup import BeautifulStoneSoup


weather_url = 'http://www.google.com/ig/api?weather=91711'
weather_url_opened = urllib2.urlopen(weather_url)
weather_xml = BeautifulStoneSoup(weather_url_opened.read()) 
weather_img_url = 'http://www.google.com'

the_day = 'Monday'
br = "<br />"

for day in weather_xml('forecast_conditions'):
    if day.day_of_week['data'] == the_day[:3]:
        low = day('low')[0]['data']
        high = day('high')[0]['data']
        img = weather_img_url + day('icon')[0]['data']
        cond = day('condition')[0]['data']

print "".join(["<img src=\"", img, "\" width=\"48\" height=\"48\" />", cond, ", high ", high, ", low ", low,
              " with a 20% chance that <a href=\"     \">     </a>", br*2])
