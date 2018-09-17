import boto3
import shlex, subprocess
import time
import json
import datetime

time_between_no_props = 30

#AWS Variables
s3_resource = boto3.resource('s3')
s3_bucket = 'cosmos-validator-data'
s3_key_path = 'data/gov/active_votes'

#For Linux: Full path to executable in system
gaiacli_path = 'gaiacli'
aws_path = 'aws'

def main():
    #Find all the VotingPeriod Votes

    #In a While loop because this should always be running
    while True:
        start = time.time()
        #Query Current Votes
        current_votes = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-proposals', '--status', 'VotingPeriod']).split('\n')

        #If None, sleep for time_between_no_props
        if current_votes[0] == "No matching proposals found":
            #Wait 30 Seconds
            print "Nothing to load, Waiting..."
            time.sleep(time_between_no_props)
            continue

        #For all outstanding proposals, query them and send to s3
        for next_proposal in current_votes:
            proposal_id = current_votes[0].split('-')[0].strip()
            current_proposal_votes = subprocess.check_output(['/home/ubuntu/goApps/bin/gaiacli', 'gov', 'query-votes', '--proposal-id', proposal_id])

            #If voting period has lapsed, continue
            if current_proposal_votes.split('.') == 'Proposal not in voting period.':
                print "Proposal Time Lapsed."
                continue

            print "Uploading Proposal Id: " + str(proposal_id)
            #Else, upload the data directly to s3
            key_full_path = s3_key_path + '/' + proposal_id + '.json'
            obj = s3_resource.Object(s3_bucket, key_full_path)
            obj.put(Body=current_proposal_votes)

            print datetime.datetime.now().isoformat()
            print "Uploaded: " + key_full_path

        #Wait 2 seconds and go again
        time.sleep(2)

main()
