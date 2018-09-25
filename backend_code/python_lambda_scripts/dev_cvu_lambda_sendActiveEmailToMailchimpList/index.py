from mailchimp3 import MailChimp
import boto3
import pdb
import json

import sendgrid
from sendgrid.helpers.mail import *

from keys import Keys

#Email Clients
client = MailChimp(mc_api=Keys.MAILCHIMP_API, mc_user='CleverGoose')
sg = sendgrid.SendGridAPIClient(apikey=Keys.SENDGRID_API)

#Set Boto3 Resources
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

#Static Boto3 Elements
status_table_name = 'dev_cvu_dynamodb_latestStatus'

def generateEmailHTML(email_contents):

    base_html = '''
<html>
<head>
<title>Cosmos Network Active Proposal Alert</title>
</head>
<body>
<h2>Cosmos Network New Proposal Alert</h2>
<h3>%(proposal_id)s: %(title)s</h3>
<p>Description: %(description)s</p>
<p>Submitted at Block # %(submit_block)s | Current Block Height: %(current_block_height)s</p>
<p>Current VotingPeriod Proposal Time: 200 blocks</p>
<p>To Unsubscribe, click <a href='https://clevergoose.us18.list-manage.com/unsubscribe?u=be62b97b186d72ef3f3d50331&id=37afc9cdef'>here.</a>
</body>
</html>
    ''' % email_contents

    return base_html

def handler(event, context):
    #Get the current email event from s3
    for next_record in event['Records']:
        bucket_name = next_record['s3']['bucket']['name']
        object_name = next_record['s3']['object']['key']

        obj = s3.get_object(Bucket=bucket_name, Key=object_name)
        obj_body = obj['Body'].read()

        proposal_details = json.loads(obj_body)

        email_contents = {}

        email_contents['proposal_id'] = proposal_details['value']['proposal_id']
        email_contents['submit_block'] = proposal_details['value']['submit_block']
        email_contents['title'] = proposal_details['value']['title']
        email_contents['description'] = proposal_details['value']['description']

        #Get the latest block from the network
        table = dynamodb.Table(status_table_name)
        response = table.scan()
        email_contents['current_block_height'] = response['Items'][0]['block_height']

        html_contents = generateEmailHTML(email_contents)

        #Read all Emails in CleverGoose List named "Active Gov Proposals Subscribers"
        #List Id = 37afc9cdef

        list_members = client.lists.members.all('37afc9cdef', fields="members.email_address,members.id,members.status")['members']

        #For each email, send a sendgrid email
        for next_member in list_members:
            print "Sending Email to: " + next_member['email_address']
            from_email = Email("schuster@clevergoose.io")
            to_email = Email(next_member['email_address'])
            subject = "Cosmos Network New Proposal: # %(proposal_id)s" % email_contents
            content = Content("text/html", html_contents)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
