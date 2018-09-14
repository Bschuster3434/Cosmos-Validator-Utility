#Setup Base Install Packages
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y make

#Install GoLang
curl -O https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz
tar -xvf go1.9.1.linux-amd64.tar.gz
mv go /usr/local
echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.profile

#Create goApps directory, set GOPATH and put it on PATH
mkdir goApps
echo "export GOPATH=~/goApps" >> ~/.profile
echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.profile
source ~/.profile

REPO=github.com/cosmos/cosmos-sdk
go get $REPO
cd $GOPATH/src/$REPO
