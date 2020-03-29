#!/bin/bash

red='\e[91m'
green='\e[92m'
yellow='\e[93m'
magenta='\e[95m'
cyan='\e[96m'
none='\e[0m'

TPUT_RESET="$(tput sgr 0)"
TPUT_YELLOW="$(tput setaf 3)"
TPUT_WHITE="$(tput setaf 7)"
TPUT_BGRED="$(tput setab 1)"
TPUT_BGGREEN="$(tput setab 2)"
TPUT_BOLD="$(tput bold)"
TPUT_DIM="$(tput dim)"

# install docker ce for Ubuntu
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    python3 \
    gnupg-agent \
    software-properties-common
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}components installed.${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to install components.${none}"
    exit 1
fi
curl -fsSL https://download.docker.com/linux/ubuntu/gpg |  apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}Docker installed.${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to install Docker.${none}"
    exit 1
fi
curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}Docker Compose installed.${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to install Docker Compose.${none}"
    exit 1
fi

# set up v2ray docker
docker pull v2ray/official
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}v2ray image ready.${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to pull v2ray image.${none}"
    exit 1
fi
python3 ./genUUID.py
chmod +r ./config.json
mkdir /etc/v2ray
mkdir /var/log/v2ray
cp ./config.json /etc/v2ray/config.json
docker run --restart always --network host -d --name v2ray -v /etc/v2ray:/etc/v2ray -v /var/log/v2ray/:/var/log/v2ray/ v2ray/official  v2ray -config=/etc/v2ray/config.json
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}v2ray online.${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to setup v2ray docker.${none}"
    exit 1
fi

# set up portainer
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
if [ $? -eq 0 ]; then
    printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
    echo -e "${green}portainer online (localhost:9000).${none}"
else
    printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} ABORTED ${TPUT_RESET} ${*} \t"
    echo -e "${red}failed to setup portainer docker.${none}"
fi
printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} ${*} \t"
echo -e "${green}Installation Complete.${none}"
