from django.shortcuts import render
import requests
import json

def indexz(request):
    url = 'http://192.168.1.49/api_jsonrpc.php'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'jsonrpc': '2.0',
        'method': 'host.get',
        'params': {
            'output': ['hostid', 'host', 'status', 'snmp_available']
        },
        'auth': '25dc5f7cf0490320a56e0f234bb8eae8a48647885358126072b2b7cb3197c0d4',
        'id': 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    hosts = data.get('result', [])

    return render(request, 'zabbix/indexz.html', {'hosts': hosts})

def ajouter_hote(request):
    return render(request, 'zabbix/ajouter_hote.html')

def test(request):
    return render(request, 'zabbix/test.html')
