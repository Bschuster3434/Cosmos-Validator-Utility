import boto3
import json
import datetime
import pdb

#Set Boto3 Resources
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = "cosmos-validator-data"
target_key_prefix = "data/gov/active_votes/"
destination_key_prefix = "data/gov/finished_votes/"

def handler(event, context):
    #Read the DynamodDB table for Current Validators
    validator_table_name = 'dev_cvu_dynamodb_fullValidatorList'
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

        else:
        #Read the file
            obj = s3_resource.Object(bucket_name, next_vote_file['Key'])
            votes = obj.get()['Body'].read()

            #Iterate over the list of Validators
            for next_validator in active_validators:
                #If a Vote is found, insert that data
                pass
                #If no Vote is found, insert empty list

        #After all validators are accounted for, move
        #the file from the s3 bucket (insert and delete)

handler(0,0)
