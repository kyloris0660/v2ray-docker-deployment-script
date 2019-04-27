import json
import uuid

templete = '''{
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
				"inboundTag": ["tg-in"],
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
if __name__ == '__main__':
    file = json.loads(templete)
    print('============================================')
    port = input('Enter Port (from 0 - 65535): ')
    file['inbounds'][0]['port'] = int(port)
    file['inbounds'][0]['settings']['clients'][0]['id'] = str(uuid.uuid4())
    UUID = file['inbounds'][0]['settings']['clients'][0]['id']
    PORT = file['inbounds'][0]['port']
    ALTERID = file['inbounds'][0]['settings']['clients'][0]['alterId']
    print('============================================')
    print('UUID: \033[0;31m%s\033[0m' % UUID)
    print('PORT: \033[0;31m%s\033[0m' % PORT)
    print('ALTERID: \033[0;31m%s\033[0m' % ALTERID)
    print('============================================')
    with open('config.json', 'w') as f:
        json.dump(file, f, indent=4)
