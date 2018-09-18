import boto3
import json
import datetime

#Set Boto3 Resources
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

#s3 Bucket Variables
bucket_name = "cosmos-validator-data"
key_prefix = "data/gov/finished_results/"

#DynamoDB Variables
table_name = "dev_cvu_dynamodb_ProposalResultsAggregateFinal"

def insertDynamoDBResult(results):
    #Create DynamoDB Object
    table_insert = {}
    table_insert['proposalId'] = int(results['value']['proposal_id'])
    table_insert['votingStartBlock'] = int(results['value']['voting_start_block'])
    table_insert['proposalStatus'] = results['value']['proposal_status']
    table_insert['title'] = results['value']['title']
    table_insert['description'] = results['value']['description']
    table_insert['totalDeposit'] = results['value']['total_deposit'][0]['amount']
    table_insert['totalDepositDenom'] = results['value']['total_deposit'][0]['denom']
    table_insert['voted_yes'] = results['value']['tally_result']['yes']
    table_insert['voted_no'] = results['value']['tally_result']['no']
    table_insert['voted_no_with_veto'] = results['value']['tally_result']['no_with_veto']
    table_insert['voted_abstain'] = results['value']['tally_result']['abstain']

    #Creating an abstraction based on votes
    #Total Voting Power

    total_votes = [0,0]

    #Tally Yes Votes
    if '/' in results['value']['tally_result']['yes']:
        next_result = results['value']['tally_result']['yes'].split('/')
    else:
        next_result = [results['value']['tally_result']['yes'],'0']

    total_votes[0] += int(next_result[0])
    total_votes[1] += int(next_result[1])

    #Tally No Resuts
    if '/' in results['value']['tally_result']['no']:
        next_result = results['value']['tally_result']['no'].split('/')
    else:
        next_result = [results['value']['tally_result']['no'],'0']

    total_votes[0] += int(next_result[0])
    total_votes[1] += int(next_result[1])

    #Tally No with Veto Results
    if '/' in results['value']['tally_result']['no_with_veto']:
        next_result = results['value']['tally_result']['no_with_veto'].split('/')
    else:
        next_result = [results['value']['tally_result']['no_with_veto'],'0']

    total_votes[0] += int(next_result[0])
    total_votes[1] += int(next_result[1])

    #Tally Abstain Results
    if '/' in results['value']['tally_result']['abstain']:
        next_result = results['value']['tally_result']['abstain'].split('/')
    else:
        next_result = [results['value']['tally_result']['abstain'],'0']

    total_votes[0] += int(next_result[0])
    total_votes[1] += int(next_result[1])

    total_votes[0] = str(total_votes[0])
    total_votes[1] = str(total_votes[1])

    table_insert['total_votes'] = '/'.join(total_votes)

    #Insert Into Table
    table = dynamodb.Table(table_name)
    response = table.put_item(
       Item=table_insert
    )

def handler(event, context):
    #'bulk_insert' is the key I will append for a
    #one time insert event in DynamoDB
    if 'bulk_insert' in event:
        #Expects a list of strings with the proposalId
        records_to_process = event['records']

        #Retrieve Obj
        for proposalId in records_to_process:
            key_name = key_prefix + proposalId + '.json'
            s3_object = s3.Object(bucket_name, key_name)
            data = s3_object.get()['Body'].read()

            proposal_results = json.loads(data)
            insertDynamoDBResult(proposal_results)

    else:
        #Otherwise, expect the normal Records List
        for objects in event["Records"]:
            key_name = objects['s3']['object']['key']
            s3_object = s3.Object(bucket_name, key_name)
            data = s3_object.get()['Body'].read()

            proposal_results = json.loads(data)
            insertDynamoDBResult(proposal_results)
