import json


def throw_port_json(port):
    port = {'port': port,
            'port2': port +1,
            'port3': port + 2}

    with open('port.json', 'w', encoding='UTF-8') as f:
        json.dump(port, f)