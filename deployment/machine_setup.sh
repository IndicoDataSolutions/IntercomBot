#!/bin/bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-get install -y git tmux

# Requests SSL
sudo apt-get install -y libffi-dev
sudo pip install 'requests[security]'

# Docker installation
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo mkdir -p /etc/apt/sources.list.d/
sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee -a /etc/apt/sources.list.d/docker.list
sudo apt-get update && sudo apt-get purge lxc-docker && sudo apt-cache policy docker-engine

sudo apt-get install -y linux-image-extra-$(uname -r)
sudo apt-get install -y apparmor docker-engine
sudo service docker start

# Have GITHUB ACCESS TOKEN in environment variable
git clone https://$GITHUB_ACCESS_TOKEN@github.com/IndicoDataSolutions/IntercomBot.git
