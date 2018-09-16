# CLI (gaiacli) research for Cosmos

## Documents

Rest API YAML: https://github.com/cosmos/cosmos-sdk/blob/develop/docs/clients/lcd-rest-api.yaml

## Gov Proposals

### DataTypes

- proposal_status
-- VotingPeriod
-- Passed
-- Rejected

### CLI Interface List
- Retrieve list of all proposals
-- gaiacli gov query-proposals
-- curl 'localhost:1317/gov/proposals'
- Retrieve list of VotingPeriod proposals
-- gaiacli gov query-proposals --status VotingPeriod
- Query Specific Proposal
-- gaiacli gov query-proposal --proposal-id <id>
-- curl 'localhost:1317/gov/proposals/<id>'
- Retrieve list of Passed proposals
-- gaiacli gov query-proposals --status Passed
- Retrieve list of Rejected proposals
-- gaiacli gov query-proposals --status Rejected
- Find Time Remaining for active proposals
-- Not in json, must calculate as 200 blocks away from the current
- Find Voting Record for active proposal
-- gaiacli gov query-votes --proposal-id <id>
