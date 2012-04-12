import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import urllib2

collins_breakfast_url = 'http://www.cafebonappetit.com/collins-cmc/cafes/collins/weekly_menu.html'
collins_lunch_url = 'http://www.cafebonappetit.com/collins-cmc/cafes/collins/weekly_menu2.html'
collins_dinner_url = 'http://www.cafebonappetit.com/collins-cmc/cafes/collins/weekly_menu3.html'

print "<table>"
print "<tr>"
print "<td></td><td>Collins</td>"
print "</tr>"
print "<tr>"
print "<td>Breakfast</td>"

collins_breakfast_open = urllib2.urlopen(collins_breakfast_url)
cbfast = BeautifulSoup(collins_breakfast_open)
the_day = "Monday"
allstrong = cbfast.findAll('strong')
for day in allstrong:
    if the_day in day.text:
        next_element = day.next
        while not hasattr(next_element, 'text') or "Tuesday" not in next_element.text:
            print next_element
            next_element = next_element.next
