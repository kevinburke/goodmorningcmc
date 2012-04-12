import xml.etree.ElementTree as etree
import urllib2
from message_all_users import TwilioMessage

def main():
    '''get the snack menu, construct SMS message, call send method'''

    snack_url = 'http://specials.cafebonappetit.com/baXML.asp?cafeid=228'
    opened_url = urllib2.urlopen(snack_url)
    snack_xml = opened_url.read()
    the_tree = etree.fromstring(snack_xml)
    the_snack = the_tree.findall(".//txtTitle")
    the_snack_text = ""
    if the_snack:
        the_snack_element = the_snack[0]
        if hasattr(the_snack_element, 'text'):
            the_snack_text = the_snack_element.text

    if not the_snack_text:
        the_message = "No snack tonight. Sorry :("
    else:
        the_message = """Tonight's snack: %s. Tell your friends:
 http://bit.ly/cmcsnack. Unsub: reply 'u' to this number""" % the_snack_text

    # send the message
    twilio_message = TwilioMessage()
    twilio_message.send_message_to_all_users(the_message)

if __name__ == "__main__":
    main()
