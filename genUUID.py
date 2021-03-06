import json
import uuid
import base64
import socket

template = '''{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  },
  "inbounds": [
    {
      "port": 0,
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": "Templete",
            "level": 1,
            "alterId": 64
          }
        ]
      },
      "streamSettings": {
        "network": "tcp"
      },
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls"
        ]
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {}
    },
    {
      "protocol": "blackhole",
      "settings": {},
      "tag": "blocked"
    },
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "direct"
    },
    {
      "protocol": "mtproto",
      "settings": {},
      "tag": "tg-out"
    }
  ],
  "dns": {
    "server": [
      "1.1.1.1",
      "1.0.0.1",
      "8.8.8.8",
      "8.8.4.4",
      "localhost"
    ]
  },
  "routing": {
    "domainStrategy": "IPOnDemand",
    "rules": [
      {
        "type": "field",
        "ip": [
          "0.0.0.0/8",
          "10.0.0.0/8",
          "100.64.0.0/10",
          "127.0.0.0/8",
          "169.254.0.0/16",
          "172.16.0.0/12",
          "192.0.0.0/24",
          "192.0.2.0/24",
          "192.168.0.0/16",
          "198.18.0.0/15",
          "198.51.100.0/24",
          "203.0.113.0/24",
          "::1/128",
          "fc00::/7",
          "fe80::/10"
        ],
        "outboundTag": "blocked"
      },
      {
        "type": "field",
        "inboundTag": [
          "tg-in"
        ],
        "outboundTag": "tg-out"
      },
      {
        "type": "field",
        "protocol": [
          "bittorrent"
        ],
        "outboundTag": "blocked"
      }
    ]
  },
  "transport": {
    "kcpSettings": {
      "uplinkCapacity": 100,
      "downlinkCapacity": 100,
      "congestion": true
    },
    "sockopt": {
      "tcpFastOpen": true
    }
  }
}'''


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def process_tcp(template):
    file = json.loads(template)
    print('============================================')
    port = input('Enter Port (from 0 - 65535): ')
    file['inbounds'][0]['port'] = int(port)
    file['inbounds'][0]['settings']['clients'][0]['id'] = str(uuid.uuid4())
    IP = get_ip()
    UUID = file['inbounds'][0]['settings']['clients'][0]['id']
    PORT = file['inbounds'][0]['port']
    ALTERID = file['inbounds'][0]['settings']['clients'][0]['alterId']
    kitsunebi_format_str = 'vmess://' + (base64.b64encode(str.encode(
        'auto:%s@%s:%s' % (UUID, IP, PORT)))).decode(
        "utf-8") + '%3Fnetwork%3Dtcp%26aid%3D64%26tls%3D0%26allowInsecure%3D1%26mux%3D1%26muxConcurrency%3D8'
    qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + kitsunebi_format_str
    print('============================================')
    print('Protocol: \033[0;31m%s\033[0m' % 'TCP')
    print('IP: \033[0;31m%s\033[0m' % IP)
    print('UUID: \033[0;31m%s\033[0m' % UUID)
    print('PORT: \033[0;31m%s\033[0m' % PORT)
    print('ALTERID: \033[0;31m%s\033[0m' % ALTERID)
    print('QRCODE for kitsunebi/v2rayN: \033[0;31m%s\033[0m' % qr_code)
    print('\033[0;32m%s\033[0m' % 'Config File Saved As ./config.txt')
    print('============================================')
    with open('config.json', 'w') as f:
        json.dump(file, f, indent=4)
    with open('config.txt', 'w') as j:
        j.write('UUID: %s\n' % UUID)
        j.write('PORT: %s\n' % PORT)
        j.write('ALTERID: %s\n' % ALTERID)
        j.write('QRCODE for kitsunebi/v2rayN: %s\n' % qr_code)


def process_mkcp(template):
    file = json.loads(template)
    file['inbounds'][0]['streamSettings']['network'] = 'mkcp'
    file['inbounds'][0]['streamSettings']['kcpSettings'] = {}
    file['inbounds'][0]['streamSettings']['kcpSettings']['uplinkCapacity'] = 20
    file['inbounds'][0]['streamSettings']['kcpSettings']['downlinkCapacity'] = 100
    file['inbounds'][0]['streamSettings']['kcpSettings']['congestion'] = True
    file['inbounds'][0]['streamSettings']['kcpSettings']['header'] = {}
    file['inbounds'][0]['streamSettings']['kcpSettings']['header']['type'] = 'none'
    print('============================================')
    port = input('Enter Port (from 0 - 65535): ')
    file['inbounds'][0]['port'] = int(port)
    file['inbounds'][0]['settings']['clients'][0]['id'] = str(uuid.uuid4())
    IP = get_ip()
    UUID = file['inbounds'][0]['settings']['clients'][0]['id']
    PORT = file['inbounds'][0]['port']
    ALTERID = file['inbounds'][0]['settings']['clients'][0]['alterId']
    kitsunebi_format_str = 'vmess://' + (base64.b64encode(str.encode(
        'auto:%s@%s:%s' % (UUID, IP, PORT)))).decode(
        "utf-8") + '%3Fnetwork%3Dkcp%26kcpHeader%3Dnone%26uplinkCapacity' + \
        '%3D20%26downlinkCapacity%3D100%26aid%3D64%26tls%3D0%26allowInsecure%3D1%26mux%3D1%26muxConcurrency%3D8'
    qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + kitsunebi_format_str
    print('============================================')
    print('Protocol: \033[0;31m%s\033[0m' % 'mKCP')
    print('IP: \033[0;31m%s\033[0m' % IP)
    print('UUID: \033[0;31m%s\033[0m' % UUID)
    print('PORT: \033[0;31m%s\033[0m' % PORT)
    print('ALTERID: \033[0;31m%s\033[0m' % ALTERID)
    print('UplinkCapacity: \033[0;31m%s\033[0m' % 20)
    print('DownlinkCapacity: \033[0;31m%s\033[0m' % 100)
    print('Congestion: \033[0;31m%s\033[0m' % 'true')
    print('Header: \033[0;31m%s\033[0m' % 'none')
    print('QRCODE for kitsunebi/v2rayN: \033[0;31m%s\033[0m' % qr_code)
    print('\033[0;32m%s\033[0m' % 'Config File Saved As ./config.txt')
    print('============================================')
    with open('config.json', 'w') as f:
        json.dump(file, f, indent=4)
    with open('config.txt', 'w') as j:
        j.write('UUID: %s\n' % UUID)
        j.write('PORT: %s\n' % PORT)
        j.write('ALTERID: %s\n' % ALTERID)
        j.write('QRCODE for kitsunebi/v2rayN: %s\n' % qr_code)


if __name__ == '__main__':
    print('============================================')
    mode_msg = 'Select the transmission protocol:\n' \
               '1) TCP\n' \
               '2) mKCP'
    print(mode_msg)
    mode = input('(1 / 2 default: 1):  ')
    if mode == '2':
        process_mkcp(template)
    else:
        process_tcp(template)
