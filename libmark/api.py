import requests
import ast
import json
from .experiment import QleaderExperiment

# Use this (or wherever your local WebMark2 is running) while developing
# url = 'http://localhost:8000/api/'
url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'


def get_distances():
    """Get benchmark distances to include result in smallest variance leaderboards

    return list
    """
    res = requests.get(f'{url}distances/')
    return ast.literal_eval(res.content.decode('UTF-8'))


def get_fci(basis_set):
    """Get FCI values"""
    try:
        res = requests.get(f'{url}fci/{basis_set}/')
        return ast.literal_eval(res.content.decode('UTF-8'))
    except Exception:
        return 'Requested basis set not available.'


def get_data(id, token):
    """Get a dump of all data available about an experiment"""
    headers = {
        'Authorization': f'Token {token}'
    }
    res = requests.get(f'{url}{id}/download/dump/', headers=headers)
    return json.loads(res.content)


def get_experiment(id, token):
    """Get information required to recreate a result
    
    return QleaderExperiment
    """
    headers = {
        'Authorization': f'Token {token}'
    }
    res = requests.get(f'{url}{id}/download/experiment/', headers=headers)
    res_dict = json.loads(res.content)
    for i in range(len(res_dict['ansatz'])):
        res_dict['ansatz'][i] = ast.literal_eval(res_dict['ansatz'][i])
    return QleaderExperiment(**res_dict)
