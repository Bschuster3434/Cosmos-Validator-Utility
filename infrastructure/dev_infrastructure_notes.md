# Infrastructure Notes

## Tags

All project objects will be tagged with {'project': 'cosmos-validator-utility'}

## EC2 Instances

### Cosmos Full Node Instance

AMI: Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-04169656fea786776
Instance Type: t2.small (t2.medium for sync)
HHD: 30GB
Security Group: Cosmos Full Node Setup

## IAM Roles

### dev_cvu_role_lambdaUtilityRole

Name: dev_cvu_role_lambdaUtilityRole
Policies:
-- LambdaFullAccess
-- S3FullAccess
-- DynamoDBFullAccess

### dev_cvu_role_fullCosmosNodeRole

Name: dev_cvu_role_fullCosmosNodeRole
Policies:
-- S3FullAccess
-- DynamoDBFullAccess
-- LambdaFullAccess

## S3 Bucket

- cosmos-validator-data

## DynamoDB Tables

### dev_cvu_dynamodb_fullValidatorList

Name: dev_cvu_dynamodb_fullValidatorList
Key: validatorKey
R/W: Autoscale 2/2

## API Gateway Structure

## Lambda Shells

### dev_cvu_lambda_processValidatorsIntoDynamoDB

Name: dev_cvu_lambda_processValidatorsIntoDynamoDB
Runtime: Python 2.7
Handler: index.handler
(file: backend_code/python_lamdbda_script/dev_cvu_lambda_processValidatorsIntoDynamoDB)
Role: dev_cvu_role_lambdaUtilityRole
Memory: 128 MB
Timeout: 20 secs

Cloudwatch Trigger Event: Cloudwatch Timer
Cloudwatch Expression: Run Once Every 5 Minutes
