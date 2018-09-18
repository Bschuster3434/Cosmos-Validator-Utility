import boto3
import json
import datetime
import pdb

#Set Boto3 Resources
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

#S3 Variables
bucket_name = "cosmos-validator-data"
target_key_prefix = "data/gov/active_votes/"
destination_key_prefix = "data/gov/finished_votes/"

#DynamoDB Variables
validator_table_name = 'dev_cvu_dynamodb_fullValidatorList'
proposal_vote_table_name = 'dev_cvu_dynamodb_ValidatorProposalVote'

def handler(event, context):
    validator_table = dynamodb.Table(validator_table_name)

    response = validator_table.scan()
    validators = response['Items']

    active_validators = [i for i in validators if i['revoked'] == False]

    #Read S3 bucket for outstanding JSON Files
    response = s3_client.list_objects(Bucket = bucket_name, Prefix = target_key_prefix)
    vote_files = response['Contents']

    #Iterate Over the List of S3 Bucket Objects
    for next_vote_file in vote_files:
        #Eliminate the Empty Key
        if next_vote_file['Key'] == target_key_prefix:
            continue

        #Read the file
        obj = s3_resource.Object(bucket_name, next_vote_file['Key'])
        votes = json.loads(obj.get()['Body'].read())

        #Iterate over the list of Validators
        validator_votes = []
        for next_validator in active_validators:
            #Iterate over the list of votes
            for next_vote in votes:
                validator_vote_record = {}

                #If a Vote is found, insert that data
                if next_validator['validatorKey'] == next_vote['voter']:
                    ##Logic for Validator Data
                    validator_vote_record['validatorKey'] = next_vote['voter']
                    validator_vote_record['proposalId'] = int(next_vote['proposal_id'])
                    validator_vote_record['castVoteFor'] = next_vote['option']
                    break

            #If no Vote is found, insert empty list
            if validator_vote_record == {}:
                validator_vote_record['validatorKey'] = next_validator['validatorKey']
                validator_vote_record['proposalId'] = int(next_vote_file['Key'].split('/')[-1].split('.')[0])
                validator_vote_record['castVoteFor'] = 'Void'

            validator_votes.append(validator_vote_record)

        #Batch Write Votes to the vote table
        proposal_vote_table = dynamodb.Table(proposal_vote_table_name)

        with proposal_vote_table.batch_writer(overwrite_by_pkeys=['validatorKey']) as batch:
            for next_vote in validator_votes:
                next_vote['time_inserted'] = datetime.datetime.now().isoformat()
                batch.put_item(Item = next_vote)

        #After all validators are accounted for, move
        #the file from the s3 bucket (insert and delete)

        destination_key = destination_key_prefix + next_vote_file['Key'].split('/')[-1]

        target_source = {'Bucket': bucket_name,'Key': next_vote_file['Key']}
        s3_client.copy_object( CopySource=target_source, Bucket= bucket_name, Key=destination_key)

        #Delete From S3
        s3_resource.Object(bucket_name, next_vote_file['Key']).delete()
