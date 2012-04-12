import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import urllib2

url = 'http://www.mikemaltese.com/5cmenu/'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

print "<table>"
print "<tr>"
print "<td></td><td>Frank</td><td>Oldenborg</td><td>Frary</td><td>Collins</td>" + \
        "<td>Malott (Scripps)</td><td>McConnell (Pitzer)</td><td>Hoch-Shanahan (Harvey Mudd)</td>"
print "</tr>"
print "<tr>"
print "<td>Breakfast</td>"

bfast = soup.find('a', id="breakfast")
nc = bfast.nextSibling
print type(nc)
while nc.__class__ != "BeautifulSoup.NavigableString" or not (nc.has_key('id')) or not (nc['id'] == 'lunch'):
    print type(nc)
    while nc == "\n":
        nc = nc.nextSibling
    print "<td>" + "\n".join([unicode(i) for i in nc('ul')]) + "</td>"
    nc = nc.nextSibling
