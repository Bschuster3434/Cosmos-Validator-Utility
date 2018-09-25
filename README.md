# Cosmos-Validator-Utility (Testnet 8001)
A Visual and Alerting Tool to Assist Cosmos Validator in Monitoring Governace
Activity through a Simple Dashboard and Email Alert Tool. Available as a
serverless website.

View the Website Here: http://vuejscvuwebsitetest.s3-website-us-east-1.amazonaws.com/

## Tool Purpose

The purpose of this tool is to assist Cosmos Testnet users to monitor the
validators on the network. This tools accomplishes this goal in two ways:

1) Provide a tool to allow users to select from a list of active validators and view their record on the testnet.
2) Provide an email address to get updates when new governance votes are available.


## Service Details
All metrics are provided by a AWS serverless service, collecting data directly from a monitored cosmos node. The infrastructure is designed in such a way as to allow for multi nodes to feed data to the infrastructure. The core services used to provide this infrastructure includes:

- S3
- DynamoDB
- API Gateway
- S3 Static Hosting
- Lambda

![alt text](https://github.com/Bschuster3434/Cosmos-Validator-Utility/blob/master/infrastructure/Documents/AWS%20Infrastructure%20Diagram.jpg "AWS Infrastructure (including Cosmos Node)")
