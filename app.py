import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from forms import InviteForm, InviteListForm, IIDForm, RSVPForm1, RSVPForm2, RSVPForm3, RSVPForm4, RSVPForm5, RSVPForm6
app = Flask(__name__)
app.debug=True
app.config.from_object(Config)

dynamodb = boto3.resource('dynamodb')

def updateTable(iid, attending, partySize):
	print(datetime.utcnow())
	table = dynamodb.Table('invitees-dev')
	return table.update_item(Key={'InviteID':iid},
		UpdateExpression='SET Attending=:val1, Updated=:val2',
		ExpressionAttributeValues={
			':val1':partySize,
			':val2':str(datetime.utcnow())
			}
		)

	


def getIIDInfo(iid):
	table = dynamodb.Table('invitees-dev')
	response = table.get_item(Key={'InviteID':iid})
	try:
		invite = response['Item']
		return invite
	except:
		return False

#@app.route('/', methods=['GET'])
#def home():
#	return render_template('index.html')

#@app.route('/rsvp', methods=['GET'])

@app.route('/godView', methods=['GET'])
def admin():
	inviteListForm = InviteListForm()
	table = dynamodb.Table('invitees-dev')

	#get all invite info
	response = table.scan()
	invites = response['Items']

	return render_template('admin.html', invitees = invites)


@app.route('/', methods=['GET'])
def index():
	form = IIDForm()
	rsvpForm = RSVPForm1()
	invite = False
	return render_template('index.html', form=form)


@app.route('/invitationCode', methods=['POST'])
def invitationCode():
	form = IIDForm()
	rsvpForm = RSVPForm1()
	if form.validate_on_submit():
		iid = form.iid.data
		invite = getIIDInfo(iid)
		if not invite:
			flash('Code not found!')
		else:
			return redirect(url_for('rsvp', iid=iid))
	return render_template('rsvp.html', date=str("test"), form=form, 
		rsvpForm = rsvpForm, invite=invite, completed=False, name='')

@app.route('/rsvp/<iid>', methods=['GET','POST'])
def rsvp(iid):
	form = IIDForm()
	invite = getIIDInfo(iid)
	if not invite:
		flash('Invitation code not found! Please check your email and reenter.')
		return redirect(url_for('index'))
	allowedCount = str(invite['AllowedCount'])
	attendingCount = str(invite['Attending'])
	updated = str(invite['Updated'])
	
	completed = False
	if updated != '0':
		completed = True

	attending = False
	print(attendingCount)
	if attendingCount != '0':
		attending = True

	if allowedCount == '1':
		rsvpForm = RSVPForm1()
	elif allowedCount == '2':
		rsvpForm = RSVPForm2()
	elif allowedCount == '3':
		rsvpForm = RSVPForm3()
	elif allowedCount == '4':
		rsvpForm = RSVPForm4()
	elif allowedCount == '5':
		rsvpForm = RSVPForm5()
	elif allowedCount == '6':
		rsvpForm = RSVPForm6()
	else:
		rsvpForm = RSVPForm1()

	print("hello")
	if rsvpForm.validate_on_submit():
		print("test")
		attending = rsvpForm.isAttending.data
		if attending:
			try:
				partySize = rsvpForm.partySize.data
			except:
				partySize = "1"
			print(invite['GuestName'])
			print("is attending with party="+partySize)
		else:
			partySize = "0"
			print("is not attending")

		completed = updateTable(iid, attending, partySize)
		return redirect(url_for('rsvp', iid=iid)) 


	return render_template('rsvp.html', date=str("test"), form=form, 
		rsvpForm = rsvpForm, invite=invite, completed=completed, 
		partySize = allowedCount, name=invite['GuestName'], iid=iid,
		attending_count=attendingCount, attending=attending)
		

if __name__=='__main__':
	app.run(debug=True)
