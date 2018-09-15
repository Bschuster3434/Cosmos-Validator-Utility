import boto3
import json
import datetime

#Set Boto3 Resources
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    #S3 Values
    bucket_name = "cosmos-validator-data"
    key_name = "data/validators/validators.json"

    #DynamoDB Values
    table_name = "dev_cvu_dynamodb_fullValidatorList"

    #Read S3 File
    s3_object = s3.Object(bucket_name, key_name)
    data = s3_object.get()['Body'].read()

    validators_list = json.loads(data)

    #Process Each Validator's data and grab the relevant details
    dynamodb_validator_items = []
    for validator in validators_list:
        next_val_dict = {}
        next_val_dict['validatorKey'] = validator['owner']
        next_val_dict['revoked'] = validator['revoked']
        next_val_dict['moniker'] = validator['description']['moniker']
        if validator['description']['website'] != '':
            next_val_dict['website'] = validator['description']['website']
        if validator['description']['details'] != '':
            next_val_dict['details'] = validator['description']['details']
        next_val_dict['bond_height'] = validator['bond_height']
        next_val_dict['tokens'] = validator['tokens']
        next_val_dict['pub_key_type'] = validator['pub_key']['type']
        next_val_dict['pub_key'] = validator['pub_key']['value']
        next_val_dict['deligator_shares'] = validator.get('deligator_shares',0)
        dynamodb_validator_items.append(next_val_dict)

    #Batch Write to the Dynamodb Table
    table = dynamodb.Table(table_name)

    with table.batch_writer(overwrite_by_pkeys=['validatorKey']) as batch:
        for n, next_validator in enumerate(dynamodb_validator_items):
            next_validator['time_inserted'] = datetime.datetime.now().isoformat()
            batch.put_item(Item = next_validator)

    return "Successfully added " + str(len(dynamodb_validator_items)) + " updated validator items"
