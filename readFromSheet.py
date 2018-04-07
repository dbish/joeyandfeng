
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import boto3
from boto3.dynamodb.conditions import Key

import uuid
from collections import namedtuple
Person = namedtuple('Person', 'name num_invites email')

dynamodb = boto3.resource('dynamodb')


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def updateTable(inviteList):
	#connect to dynamo
	table = dynamodb.Table('invitees-dev')
        
	
	for person in inviteList:
		if person.email != '':
			#look up person in table
			response = table.query(
				IndexName='EmailAddress-index',
				KeyConditionExpression=Key('EmailAddress').eq(person.email)
				)
			#if in table, update with fields from spreadsheet
			if len(response['Items']) > 0:
				print(response['Items'][0])	
				uid = response['Items'][0]['InviteID']
				attending = response['Items'][0]['Attending']
				updated = response['Items'][0]['Updated']
			else:
				#if not in table, create a UID and new entry
				uid = str(uuid.uuid4())
				attending = '0'
				updated = '0'

			response = table.put_item(
			   Item={
				'InviteID':uid,
				'EmailAddress':person.email,
				'GuestName':person.name,
				'AllowedCount':person.num_invites,
				'Attending': attending,
				'Updated':updated
				
			   }
			)	
			print(uid)
			

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    #rangeName = 'Class Data!A2:E'
    spreadsheetId = '1B0ySroC6J1LzNZLqjscU2_0MO_HyJz-95wauMdp4Pd4'
    rangeName = 'Guest List!A2:F'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
	inviteList = []
        for row in values[:-1]:
		print(row)
		if len(row) > 5:
		    inviteList.append(Person(row[2], row[3], row[5]))
		else:
		    inviteList.append(Person(row[2], row[3], ''))
		# Print columns A and E, which correspond to indices 0 and 4.
		print('%s, %s' % (row[0], row[4]))

	updateTable(inviteList)

if __name__ == '__main__':
    main()


