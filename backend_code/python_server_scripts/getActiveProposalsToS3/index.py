import boto3
import shlex, subprocess
import time
import json
import datetime

time_between_checks = 30

#AWS Variables
s3_resource = boto3.resource('s3')
s3_bucket = 'cosmos-validator-data'
s3_key_path = 'data/gov/active_proposals'

def main():
    #Fina all Voting Period proposals

    #In a while loop because this should always be running
    while True:
        #Query Current Votes
        current_proposals = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposals', '--status', 'VotingPeriod']).split('\n')

        #If None, sleep for time_between_no_props
        if current_proposals[0] == "No matching proposals found":
            #Wait 30 Seconds
            print "No proposals found"
            time.sleep(time_between_checks)
            continue

        #For all outstanding proposals, query them and send to s3
        for next_proposal in current_proposals:
            proposal_id = current_proposals[0].split('-')[0].strip()
            current_proposal_results = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposal', '--proposal-id', proposal_id])
            print "Proposal Found!"
            print current_proposal_results

            key_full_path = s3_key_path + '/' + proposal_id + '.json'
            obj = s3_resource.Object(s3_bucket, key_full_path)
            obj.put(Body=current_proposal_results)

        time.sleep(time_between_checks)

main()
