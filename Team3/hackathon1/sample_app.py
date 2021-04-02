#!/usr/bin/env python3

import requests

r = requests.get('http://127.0.0.1:5000')
print(r.status_code,r.content.decode('utf-8'))
r = requests.get('http://127.0.0.1:5000/fetch', params={'id': 1})
print(r.status_code,r.content.decode('utf-8'))
