# v2ray-docker-deployment-script

## 自用v2ray + Portainer docker部署脚本

### System Requirement

* Ubuntu 16.04 and higher
* KVM based VPS

### Installation & Usage

```shell
sudo su
apt-get install git
git clone https://github.com/kyloris0660/v2ray-docker-deployment-script.git
cd ./v2ray-docker-deployment-script
chmod +x ./install.sh
./install.sh
```

[Portainer](https://github.com/portainer/portainer) interface can be used by accessing  `YourIP:9000`.

### Others

Since v2ray docker uses host networking, enable the host's TCP-BBR using the command below may be able to improve the network situation.

```shell
echo "net.core.default_qdisc=fq" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

