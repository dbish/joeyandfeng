# joeyandfeng
To run this site locally, there are packages running with python 2.7 that need to be installed (pip install <package>). 
See the .py files to know what is imported. You can also look at my requirements.txt file list below if you use virtualenv but it covers more then you'd have to manually install.
Ruy "python app.py" to start the local server.

argcomplete==1.9.2
base58==0.2.4
boto3==1.6.16
botocore==1.9.16
certifi==2018.1.18
cfn-flip==1.0.3
chardet==3.0.4
click==6.7
docutils==0.14
durationpy==0.5
Flask==0.12.2
Flask-WTF==0.14.2
future==0.16.0
futures==3.1.1
hjson==3.0.1
idna==2.6
itsdangerous==0.24
Jinja2==2.10
jmespath==0.9.3
kappa==0.6.0
lambda-packages==0.19.0
MarkupSafe==1.0
placebo==0.8.1
python-dateutil==2.6.1
python-slugify==1.2.4
PyYAML==3.12
requests==2.18.4
s3transfer==0.1.13
six==1.11.0
toml==0.9.4
tqdm==4.19.1
troposphere==2.2.1
Unidecode==1.0.22
urllib3==1.22
Werkzeug==0.14.1
wheel==0.30.0
wsgi-request-logger==0.4.6
WTForms==2.1
zappa==0.45.1


To run this site on lambda there are a few expectations
1. You're using zappa (zappa.io) to use lambda and api gateway through AWS
2. There is a dyanamodb table accessible to your lambda called invitees-dev whith items that have the following keys:
- AllowedCount
- Attending
- GuestName
- InviteID
- Name
- Updated


