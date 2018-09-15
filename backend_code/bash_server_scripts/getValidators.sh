gaiacli stake validators --output json > files/validators.json
aws s3 cp files/validators.json s3://cosmos-validator-data/data/validators.json
