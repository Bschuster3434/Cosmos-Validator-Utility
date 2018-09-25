# Services Details

This document will detail the various backend services and how they are utilized by the network. In this section, I will discuss the following service abstractions:

- AWS Infrastructure Needs
- Validators
- Validator Votes
- Proposal Results
- New Vote Alerts
- Web Application

## AWS Infrastructure Needs

For Full Details on the AWS Infrastructure Needs, please check the following file:
https://github.com/Bschuster3434/Cosmos-Validator-Utility/blob/master/infrastructure/dev_infrastructure_notes.md

## Validators Service

### Related Services
Bash Server Scripts
- backend_code/bash_server_scripts/getValidators.sh (processed as executable CRON Job)
S3 File Location
- Key = '/data/validators/validators.json'
Lambda Python Script
- File: backend_code/python_lambda_scripts/dev_cvu_lambda_processValidatorIntoDynamoDB/index.py
DynamoDB Table
- Name: dev_cvu_dynamodb_fullValidatorList
API Gateway Entry Point
- Resource: /validators/getallvalidators
- Method: get

### Details

The Bash Script for the validators runs as a CRON job on the server. This script just pulls all of the known validators on the network and sends that file to S3, saving the latest file locally as well. The CRON job currently runs every five minutes.

Once the file is uploaded, the lambda function, running with a cloudwatch event to trigger every five minutes. The results are then parsed and uploaded to dynamoDB.

The application can then access the API gateway endpoint to get the validators to populate the application.

## Validator Vote Services

### Related Services
Python Server Scripts
-Script: backend_code/python_server_scripts/getActiveVoteCountToS3/index.py
- Service: backend_code/systemd_services/getActiveVoteCountToS3.service
S3 File Location
- Target Key = '/data/gov/active_votes/{proposal_id}.json'
- Discard Key = '/data/gov/finished_vote/{proposal_id}.json'
Lambda Python Script
- File: backend_code/python_lambda_scripts/dev_cvu_lambda_processVotesForAllValidators/index.py
DynamoDB Table
- Name: dev_cvu_dynamodb_ValidatorProposalVote
API Gateway Entry Point
- Resource: /gov/validatorvotes/{validatorkey}
- Method: get

### Details

The backend python script works to actively collect votes as they happen. It runs as a python script on the node, running command line functions to grab the proposals in 'VotingPeriod'. If no VotingPeriod proposals are found, the script sleeps for 30 seconds. If a vote is found, then the results are queried and immediately sent to S3. The process then sleeps for 2 seconds before collecting the next set of votes. This continues until the VotingPeriod time has lapsed (200 blocks as of Testing 8001).

Once the S3 results are inserted, a python script tied to an S3 process triggers and processes the results into 'ValidatorProposalVote'. The S3 file is then moved to '/data/gov/finished_votes' to ensure the results can be retrieved in the future.

Once inside dynamoDB, API gateway is able to access these results through the endpoint /gov/validatorvotes/{validatorkey} to display the voting record of each validator.

### Notes On Service Design

As of Testnet 8001, getting individual validator results from proposals is tricky. While it's possible to collect aggregate results from the network at anytime, it is only possible to query the validator results during the 'VotingPeriod' phase of the proposal. In order to collect validator votes, this service was designed to continually pass results in VotingPeriod to be processed. Once the vote ended, the final result that was found was used to judge if a validator voted (and the result of that vote).

Because of this, actual results from validators may be different if there was a last minute vote change that the service did not pick up on. In addition, it may be possible that votes are designed not to be accessible after VotingPeriod to protect validator voting records. However, given how bound delegators are to validator decisions (both financially and ethically), my personal belief is that records should be publicly available to allow for delegators and 3rd parties to make decisions.

## Proposal Results Services

### Related Services
Python Server Scripts
-Script: backend_code/python_server_scripts/getFinalProposalResultsToS3/index.py
- Service: backend_code/systemd_services/getFinalProposalResultsToS3.service
S3 File Location
- Target Key = '/data/gov/finished_results/{proposal_id}.json'
Lambda Python Script
- File: backend_code/python_lambda_scripts/dev_cvu_lambda_processProposalResultsIntoDynamoDB/index.py
DynamoDB Table
- Name: dev_cvu_dynamodb_ProposalResultsAggregateFinal
API Gateway Entry Point
- Resource: /gov/results/
- Method: get

- Resource: /gov/results/{proposalid}
- Method: get

### Details

The backend python script works to collect results that have yet to be processed. It runs as a python script on the node, running command line functions to grab the proposals in every stage of voting. As results persist on the server at all times, the script only runs every 30 seconds to get the latest results. It will only process results that do no exist in the S3 bucket directory "/data/gov/finished_results/". If the result does not exist, the proposal is queried from the server and sent to S3.

Once the S3 results are inserted, a python script tied to an S3 process triggers and processes the results into 'ProposalResultsAggregateFinal'. If the file is in 'VotingPeriod' at the time of processing, the file is then deleted from S3 to allow for it to be re-triggered and processed as new results come in.

Once inside dynamoDB, API gateway is able to access these results through the endpoint /gov/results/{proposalid} to display the voting record of each validator.

## New Vote Services

### Related Services
Python Server Scripts
-Script: backend_code/python_server_scripts/getActiveProposalsToS3/index.py
- Service: backend_code/systemd_services/getActiveProposalsToS3.service
S3 File Location
- Target Key = '/data/gov/active_proposals/{proposal_id}.json'
Lambda Python Script
- File: backend_code/python_lambda_scripts/dev_cvu_lambda_sendActiveEmailToMailchimpList/index.py

### Details

The backend python script works to find the first time a 'VotingPeriod' proposal has been found. It runs as a python script on the node, running command line functions to grab the proposals in the 'VotingPeriod' stage. The script checks every 30 seconds for results and then inserts them into S3 once they are found.

Once the S3 results are inserted, a python script tied to an S3 process trigger will activate, sending an email to the "New Proposal" mailing list on the website. S3 only triggers on the new inserts, so the email will only be sent once, right at the vote has been identified. This service is integrated with SendGrid to send out these messages.

## Web Application

The web application was built utilizing VueJS. It is served as a static website via S3 and runs fully within the user's browser.
