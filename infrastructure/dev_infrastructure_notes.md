# Infrastructure Notes

## Tags

All project objects will be tagged with {'project': 'cosmos-validator-utility'}

## EC2 Instances

### Cosmos Full Node Instance

AMI: Ubuntu Server 16.04 LTS (HVM), SSD Volume Type - ami-04169656fea786776
Instance Type: t2.micro
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

## API Gateway Structure

## Lambda Shells

### dev_cvu_lambda_getFullNodesList
Name: dev_cvu_getFullNodesList
Runtime: Python 2.7
Role: dev_cvu_role_lambdaUtilityRole
Memory: 128 MB
Timeout: 20 secs
