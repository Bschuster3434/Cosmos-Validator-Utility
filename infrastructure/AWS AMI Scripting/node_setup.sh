#Setup Base Install Packages
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y make
sudo apt-get install build-essential software-properties-common -y
sudo apt-get install python -y
sudo apt-get install python-pip -y
sudo apt-get install upstart -y

#Install Python Dependencies
pip install awscli
pip install requests
pip install boto3

#Install Golang
curl -O https://storage.googleapis.com/golang/go1.10.linux-amd64.tar.gz
tar -xvf go1.10.linux-amd64.tar.gz
sudo mv go /usr/local

#Create go directory directory, set GOPATH and put it on PATH
echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.profile

mkdir goApps
echo "export GOPATH=$HOME/goApps" >> ~/.profile
echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.profile

source ~/.profile

#Retrieve Cosmos Project
REPO=github.com/cosmos/cosmos-sdk
go get $REPO
cd $GOPATH/src/$REPO
git checkout master

#Build Cosmos
make get_tools
make get_dev_tools
make get_vendor_deps
make install

#Starting Cosmos Network
gaiad init --name cosmos_network_node
echo "uniquepassword"
moniker = "cosmos_network_node"
mkdir -p $HOME/.gaiad/config
curl https://raw.githubusercontent.com/cosmos/testnets/master/latest/genesis.json > $HOME/.gaiad/config/genesis.json
aws s3 cp s3://cosmos-validator-data/node_config_files/gaiad_config.toml /home/ubuntu/.gaiad/config/config.toml
crontab -e
echo "2"

#Setup Crontab to run Restart Processes
crontab -l | { cat; echo "@reboot /home/ubuntu/goApps/bin/gaiad start"; } | crontab -
crontab -l | { cat; echo "* * * * * /home/ubuntu/goApps/bin/gaiad start"; } | crontab -

#Get Git Repository
cd $HOME
git clone https://github.com/Bschuster3434/Cosmos-Validator-Utility.git
cd Cosmos-Validator-Utility
git checkout -b dev origin/dev
crontab -l | { cat; echo "*/5 * * * * bash /home/ubuntu/Cosmos-Validator-Utility/backend_code/bash_server_scripts/getValidators.sh"; } | crontab -

#Setup Python Services Here
sudo cp /home/ubuntu/Cosmos-Validator-Utility/backend_code/systemd_services/getActiveVoteCountToS3.service /etc/systemd/system/getActiveVoteCountToS3.service
sudo systemctl start getActiveVoteCountToS3.service
sudo systemctl enable getActiveVoteCountToS3.service
sudo cp /home/ubuntu/Cosmos-Validator-Utility/backend_code/systemd_services/getFinalProposalResultsToS3.service /etc/systemd/system/getFinalProposalResultsToS3.service
sudo systemctl start getFinalProposalResultsToS3.service
sudo systemctl enable getFinalProposalResultsToS3.service
sudo cp /home/ubuntu/Cosmos-Validator-Utility/backend_code/systemd_services/getCurrentBlockchainStatusToDynamoDB.service /etc/systemd/system/getCurrentBlockchainStatusToDynamoDB.service
sudo systemctl start getCurrentBlockchainStatusToDynamoDB.service
sudo systemctl enable getCurrentBlockchainStatusToDynamoDB.service
sudo cp /home/ubuntu/Cosmos-Validator-Utility/backend_code/systemd_services/getActiveProposalsToS3.service /etc/systemd/system/getActiveProposalsToS3.service
sudo systemctl start getActiveProposalsToS3.service
sudo systemctl enable getActiveProposalsToS3.service
