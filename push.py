#!/usr/bin/python

import sys
import requests

url = 'http://0.0.0.0:8000/api/'
# url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'

if len(sys.argv) == 2 and len(sys.argv[1]):
    file = open(sys.argv[1], "r")
    struct = file.read()
    response = requests.post(url, json=struct)
    print(response)
else:
    print("You forgot the file!")
