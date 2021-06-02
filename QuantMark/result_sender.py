import requests

# Use this (or wherever your local WebMark2 is running) while developing
url = 'http://127.0.0.1:8000/api/'

def push_results(result):
    result_json = {"result":str(result)}
    response = requests.post(url, data=result_json)
    return response