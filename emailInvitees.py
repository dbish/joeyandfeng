import boto3
from boto3.dynamodb.conditions import Key
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dynamodb = boto3.resource('dynamodb')

def createRSVPEmailBody(name, inviteID):
	rsvpURL = "www.joeyandfeng.com/rsvp/"+inviteID
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>%s<br>
	       We are formally inviting you to the Jubie-Zhao Wedding.<br>
	       Please use this link to <a href="%s">rsvp</a> by June 30th 2018.
	       You can also enter the invite code: <b>%s</b> directly at www.joeyandfeng.com/#rsvp.
	    <br>
		Thanks! We hope you can make it.
	    <br>
		Sincerely, <br>Joey Jubie & Feng Zhao
	    </p>
	  </body>
	</html>
	"""%(name, rsvpURL, inviteID)	
	return html

def sendRSVPEmail(name, inviteID, emailAddress):
	# me == my email address
	# you == recipient's email address
	me = "invites@joeyandfeng.com"
	you = emailAddress

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Feng and Joey Wedding RSVP' 
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	html = createRSVPEmailBody(name, inviteID)

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	#msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.login('diamondbishop', 'rx5rz8dk')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()


table = dynamodb.Table('invitees-dev')
response = table.scan()
invites = response['Items']

for invite in invites:
	if invite['EmailSent'] == "None":
		sendRSVPEmail(invite['GuestName'], invite['InviteID'], invite['EmailAddress'])
		
		#update table to show we sent an rsvp email
		table.update_item(Key={'InviteID':invite['InviteID']},
                UpdateExpression='SET EmailSent=:val1',
                ExpressionAttributeValues={
                        ':val1':'RSVP',
                        }
                )

