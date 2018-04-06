from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, StringField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class IIDForm(FlaskForm):
	iid = StringField('InviteCode', validators=[DataRequired()])
	submit = SubmitField('Get RSVP')

class RSVPForm1(FlaskForm):
	isAttending = BooleanField('Attending?')
	submit = SubmitField('Finalize RSVP')

class RSVPForm2(FlaskForm):
	isAttending = BooleanField('Attending?')
	partySize = SelectField(
		'Party size (including you)',
		choices = [('1','1'), ('2','2')])
	submit = SubmitField('Finalize RSVP')

class RSVPForm3(FlaskForm):
	isAttending = BooleanField('Attending?')
	partySize = SelectField(
		'Party size (including you)',
		choices = [('1','1'), ('2','2'), ('3', '3')])
	submit = SubmitField('Finalize RSVP')

class RSVPForm4(FlaskForm):
	isAttending = BooleanField('Attending?')
	partySize = SelectField(
		'Party size (including you)',
		choices = [('1','1'), ('2','2'), ('3', '3'), ('4', '4')])
	submit = SubmitField('Finalize RSVP')

class RSVPForm5(FlaskForm):
	isAttending = BooleanField('Attending?')
	partySize = SelectField(
		'Party size (including you)',
		choices = [('1','1'), ('2','2'), ('3', '3'), ('4', '4'), ('5', '5')])
	submit = SubmitField('Finalize RSVP')

class RSVPForm6(FlaskForm):
	isAttending = BooleanField('Attending?')
	partySize = SelectField(
		'Party size (including you)',
		choices = [('1','1'), ('2','2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')])
	submit = SubmitField('Finalize RSVP')

class InviteForm(FlaskForm):
	inviteID = StringField('Invite Code', validators= [DataRequired()])
	guestName = StringField('Name', validators = [DataRequired()])
	allocated = IntegerField('Allocated', validators=[DataRequired()])
	attending = IntegerField('Attending', validators=[DataRequired()])
	rsvpd = StringField('RSVPd')

class InviteListForm(FlaskForm):
	invitees = FieldList(FormField(InviteForm))

