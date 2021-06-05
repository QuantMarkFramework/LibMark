import requests

# Use this (or wherever your local WebMark2 is running) while developing
url = 'http://0.0.0.0:8000/api/'

def push_results(result, hamiltonian, ansatz, optimizer):
    result_json = {"result":str(result),
     "hamiltonian":str(hamiltonian), 
     "ansatz":str(ansatz), 
     "optimizer":str(optimizer)}
    response = requests.post(url, data=result_json)
    return response