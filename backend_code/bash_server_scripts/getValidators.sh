/home/ubuntu/goApps/bin/gaiacli stake validators --output json > /home/ubuntu/Cosmos-Validator-Utility/backend_code/bash_server_scripts/files/validators.json
echo "Saved Validators to files/validators.json"
/home/ubuntu/.local/bin/aws s3 cp files/validators.json s3://cosmos-validator-data/data/validators/validators.json
echo "Sent File to S3"
