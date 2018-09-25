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
