import boto3
import shlex, subprocess
import time
import json
import datetime
import pdb

time_between_check = 30

#AWS Variables
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
s3_bucket = 'cosmos-validator-data'
s3_key_path = 'data/gov/finished_results'

#For Linux: Full path to executable in system
gaiacli_path = 'gaiacli'
aws_path = 'aws'

def main():
    while True:
        # Getting current Proposal Ids in S3 Bucket
        tracked_proposal_results = []
        response = s3_client.list_objects(Bucket = s3_bucket, Prefix = s3_key_path)
        objects = response['Contents']

        for next_obj in objects:
            if next_obj['Key'] == s3_key_path:
                continue
            else:
                tracked_proposal_results.append(next_obj['Key'].split('/')[-1].split('.')[0])

        #Must Search Passed and Rejected to get the whole set
        rejected_proposals = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposals', '--status', 'Passed']).strip().split('\n')
        passed_proposals = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposals', '--status', 'Rejected']).strip().split('\n')
        all_completed_proposals = rejected_proposals + passed_proposals

        print "Retrieved All proposals"

        for next_proposal in all_completed_proposals:
            #Getting Proposal ID
            proposal_id = next_proposal.split('-')[0].strip()

            #Now Check if the proposal id is in the tracked proposals
            if proposal_id not in tracked_proposal_results:
                #If not, add the proposal result to S3
                proposal_result = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposal', '--proposal-id', proposal_id])

                print "Uploading Proposal Id: " + str(proposal_id)
                #Else, upload the data directly to s3
                key_full_path = s3_key_path + '/' + proposal_id + '.json'
                obj = s3_resource.Object(s3_bucket, key_full_path)
                obj.put(Body=proposal_result)
        print "Now Sleeping"
        time.sleep(time_between_check)

main()
