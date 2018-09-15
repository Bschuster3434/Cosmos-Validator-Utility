gaiacli stake validators --output json > files/validators.json
echo "Saved Validators to files/validators.json"
aws s3 cp files/validators.json s3://cosmos-validator-data/data/validators/validators.json
echo "Sent File to S3"
