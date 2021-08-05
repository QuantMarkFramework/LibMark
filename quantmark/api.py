import requests
import ast

# Use this (or wherever your local WebMark2 is running) while developing
url = 'http://localhost:8000/api/'
# url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'


def get_distances():
    """Get benchmark distances to include result in smallest variance leaderboards

    return list
    """
    res = requests.get(f'{url}distances/')
    return ast.literal_eval(res.content.decode('UTF-8'))


def get_experiment(id, token):
    """Get a dump of all data available about an experiment"""
    headers = {
            'Authorization': f'Token {token}'
        }
    res = requests.get(f'{url}{id}/download', headers=headers)
    return ast.literal_eval(res.content.decode('UTF-8'))
