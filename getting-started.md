# Ways to Get Started

Looking for ways to contribute? Here are some great ways to help out!

### Easy

* Write the email for tomorrow. Look up the examples in static/cmc/march/\*/index.html for example. For now, just send me the text and I'll figure out how to send it out.

* Add styling for visited links to the CSS stylesheet so links that you've
  already visited show up in a different color on the website.

* Check that all the links in the email still work, as CMC recently
  redesigned/rearchitected their website

### Medium

* Make the website look good on mobile phones, using [CSS media queries][media].

[media]: http://css-tricks.com/css-media-queries/

* Set up the website to run locally on your computer. There are instructions
[here][install]. This will help you troubleshoot all of the other stuff. Please
email me if you have questions.

[install]: https://github.com/kevinburke/goodmorningcmc/blob/master/INSTALL

* Resurrect the Snack text messages! So, I accidentally deleted the database of 
  phone numbers over the summer, so we'll have to get that set up again. Other stuff
  that needs to get done for this:

    - Check that Bon Appetit still updates the website and the code to grab the
      snack still works
    - Use the libphonenumber library to normalize phone numbers before storing 
      in the database. Right now I am using a really bad regular expression
      that might not be that good.
    - Make sure that numbers get saved to the database correctly
    - Draft an email to send to everyone asking them to re-add their phone
      numbers.
    - Restart the cron script to run every Monday-Thursday and text out the
      snack
    If you are interested email me and I'll give you the SSH keys to
    investigate on the server hosting the code.

* Use Markdown to generate the email. Markdown is a really simple syntax you
  can use to generate HTML. There's more details [here][markdown]. So I made
  a really dumb mistake to use this complex data format called YAML. I should
  have just used Markdown. This would make the email much faster to put
  together and much less error-prone.

* Figure out how to show the current dining hall menus on the website, all the
  time, I have some ideas about how to do this, ping me

* Update the [email generation script][create]. Just read it, it's a giant
mess and there's a ton of stuff that could be done here to make it more
robust/better.

[create]: https://github.com/kevinburke/goodmorningcmc/blob/master/email_create.py

### Hard

* Move all of the Python dependencies inside of the project, so you don't need
  Pip installs.

* Add more API's for school-wide data - for example library due dates,
  availability, etc - make it really easy for other people to program CMC apps
  by making a really great API to get the data out.


[markdown]: http://daringfireball.net/projects/markdown/
