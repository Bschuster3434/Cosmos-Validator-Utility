# Infrastructure Notes

## Tags

All project objects will be tagged with {'project': 'cosmos-validator-utility'}

## EC2 Instances

### Cosmos Full Node Instance

AMI: Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-04169656fea786776
Instance Type: c5.large
HHD: 30GB
Security Group: Cosmos Full Node Setup

## IAM Roles

### dev_cvu_role_lambdaUtilityRole

Name: dev_cvu_role_lambdaUtilityRole
Service: Lambda
Policies:
-- LambdaFullAccess
-- S3FullAccess
-- DynamoDBFullAccess

### dev_cvu_role_fullCosmosNodeRole

Name: dev_cvu_role_fullCosmosNodeRole
Service: EC2
Policies:
-- S3FullAccess
-- DynamoDBFullAccess
-- LambdaFullAccess

### dev_cvu_role_APIGatewayExecute

Name: dev_cvu_role_APIGatewayExecute
Service: API Gateway
Policies:
-- DynamoDBRead
-- LambdaExecute

## S3 Bucket

- cosmos-validator-data

/data
/data/gov
/data/gov/active_votes
Active Voting Activity on the Network
/data/gov/active_proposals
Proposal Details for Email Service
/data/gov/finished_votes
Archive of Finished Voting Activity on the Network
data/gov/finished_results
Aggregate Results of Voting Activity on the Network
/data/validators
List of Validators on the Network, updated every five minutes

## DynamoDB Tables

### dev_cvu_dynamodb_fullValidatorList

Name: dev_cvu_dynamodb_fullValidatorList
Key: validatorKey
R/W: Autoscale 2/2 (5/5)

### dev_cvu_dynamodb_ProposalResultsAggregateFinal
Name: dev_cvu_dynamodb_ProposalResultsAggregateFinal
Key: proposalId
R/W: Autoscale 2/2 (25/10)

### dev_cvu_dynamodb_ValidatorProposalVote
Name: dev_cvu_dynamodb_ValidatorProposalVote
Key: validatorKey
Sort: proposalId
R/W: Autoscale 3/3 (25/25)

### dev_cvu_dynamodb_latestStatus
Name: dev_cvu_dynamodb_latestStatus
Key: id
R/W: Autoscale 1/1 (25/25)

## API Gateway Structure

Full Details Here: https://github.com/Bschuster3434/Cosmos-Validator-Utility/blob/master/infrastructure/API%20Gateway/dev_cvu_api_applicationAPI-dev-swagger.yaml

## Lambda Shells

### dev_cvu_lambda_processValidatorsIntoDynamoDB

Name: dev_cvu_lambda_processValidatorsIntoDynamoDB
Runtime: Python 2.7
Handler: index.handler
(file: backend_code/python_lamdbda_script/dev_cvu_lambda_processValidatorsIntoDynamoDB.py)
Role: dev_cvu_role_lambdaUtilityRole
Memory: 128 MB
Timeout: 20 secs

Cloudwatch Event Trigger: Cloudwatch CRON
Cloudwatch Input: Rate(5 minute)

### dev_cvu_lambda_processProposalResultsIntoDynamoDB

Name: dev_cvu_lambda_processProposalResultsIntoDynamoDB
Runtime: Python 2.7
Handler: index.handler
(file: backend_code/python_lamdbda_script/dev_cvu_lambda_processProposalResultsIntoDynamoDB.py)
Role: dev_cvu_role_lambdaUtilityRole
Memory: 128 MB
Timeout: 60 secs

Cloudwatch Event Trigger: S3
Cloudwatch Bucket: cosmos-validator-data
Cloudwatch Key Prefix: data/gov/finished_results
Cloudwatch Key Suffix: .json

### dev_cvu_lambda_processVotesForAllValidators

Name: dev_cvu_lambda_processVotesForAllValidators
Runtime: Python 2.7
Handler: index.handler
(file: backend_code/python_lamdbda_script/dev_cvu_lambda_processProposalVotesForAllValidators.py)
Role: dev_cvu_role_lambdaUtilityRole
Memory: 128 MB
Timeout: 60 secs

Cloudwatch Event Trigger: Cloudwatch CRON
Cloudwatch Input: Rate(1 minute)

### dev_cvu_lambda_sendActiveEmailToMailchimpList

Name: dev_cvu_lambda_sendActiveEmailToMailchimpList
Runtime: Python 2.7
Handler: index.handler
(file: backend_code/python_lamdbda_script/dev_cvu_lambda_sendActiveEmailToMailchimpList.py)
Role: dev_cvu_role_lambdaUtilityRole
Memory: 512 MB
Timeout: 60 secs

Cloudwatch Event Trigger: S3
Cloudwatch Event: New Puts to bucket cosmos-validator-data/data/gov/active_proposals

## Python Server Functions

### getActiveVoteCountToS3

Service Name: getActiveVoteCountToS3.service
Purpose: Send Active Votes to S3 every two seconds for latest vote.

### getFinalProposalResultsToS3

Service Name: getFinalProposalResultsToS3.service
Purpose: Get all of the proposal results to S3 every 30 seconds.

### getCurrentBlockchainStatusToDynamoDB

Service Name: getCurrentBlockchainStatusToDynamoDB.service
Purpose: Get the network status every two seconds and upload to DynamoDB.

### getActiveProposalsToS3

Service Name: getActiveProposalsToS3.service
Purpose: Get the latest active proposals to S3
