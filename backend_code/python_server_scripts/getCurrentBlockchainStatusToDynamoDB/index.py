import boto3
import pdb
import json
import datetime
import subprocess

time_between_check = 2 #Seconds

#AWS Variables
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#DynamoDB variables
table_name = "dev_cvu_dynamodb_latestStatus"

def main():
    while True:
        #Make a call to the network for the status
        response = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'status'])
        network_status = json.loads(response)

        #translate into a dynamodb object
        dynamo_dict = {}

        dynamo_dict['id'] = '1' #only one object in table
        dynamo_dict['block_height'] = network_status['sync_info']['latest_block_height']
        dynamo_dict['catching_up'] = network_status['sync_info']['catching_up']
        dynamo_dict['latest_block_time'] = network_status['sync_info']['latest_block_time']

        #send to dynamodb, with id object
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item=dynamo_dict
        )
        #Repeat

        time.sleep(time_between_check)

main()
