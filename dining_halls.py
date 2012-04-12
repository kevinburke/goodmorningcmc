import urllib2
import xml.etree.ElementTree as etree

base_url = 'http://specials.cafebonappetit.com/baXML.asp?cafeid='
cafes = {
'collins_breakfast': '215'
}
#fetch dining hall menus
for name, cafe_id in cafes.items():
    the_xml = urllib2.urlopen(base_url + cafe_id).read()

#parse into readable format

#store in db

if __name__ == "__main__":
    main()
