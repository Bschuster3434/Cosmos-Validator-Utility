# Cosmos-Validator-Utility (Testnet 8001)
A Visual and Alerting Tool to Assist Cosmos Validator in Monitoring Governace
Activity through a Simple Dashboard and Email Alert Tool. Available as a
serverless website.

(Note: Service was halted on 10/18/2018, though the website will remain up
  and active.)

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

Python service running directly on the EC2 node operate in 2-30 second intervals to update each of the core data metrics, which include:

- Proposals (Results and Realtime Updates)
- Validator Votes
- Current Network Validator Status
- Vote Alert System

When new results and changes to the validators are detected, process fire immediately to update S3 and DynamoDB, which then gets reflected in the data. This is then visible in the dashboard.

An email alert system is also provided, allowing users to enter their email address. This email is stored in a mailchimp list and accessed through lambda when new email governance proposals are created. Upon creation, an email alert will be sent to each list member, notifying them of a new vote with details on the vote. Emails are not shared and can be unsubscribed from the email at anytime.

For more specific details on these service, please check out the services details document: https://github.com/Bschuster3434/Cosmos-Validator-Utility/blob/master/Services%20Details.md

## Future Improvements

As an MVP, there are many changes that I would like to implement to make this service more robust. Here are some of the changes I would add/improve if the project were to move forward:

- Add block height to the service and calculate time remaining for each 'VotingPeriod' proposal.
- Add datetime for each block and calculate the datatime of each vote start and estimate end time based on average block time.
- Make the VotingPeriod results responsive to changes in the database (currently require a refresh to collect updates on votes)
- Better Search and Location feature for Validators (currently need to scroll through list with no search)
- Learn CSS at some point
- Add separate pages for governance votes and email services
- Create sentry node architecture for nodes in order to protect against DOS attack (not running a full validator, but still need protection to keep node up to date)
- Allow for more specific ordering and searching in the governance result votes

## Developer Note

This was my first front end development project. I specifically picked up VueJS after seeing the Cosmos Network Explorer (https://github.com/cosmos/explorer) used VueJS. Because of this, there are many common features and styles not implemented due to lack of knowledge.
