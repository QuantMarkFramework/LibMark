import requests

# Use this (or wherever your local WebMark2 is running) while developing
url = 'http://0.0.0.0:8000/api/'
#url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'

class Qresult:
    def __init__(self, optimizer):
        self.results = []
        self.molecules = []
        self.hamiltonian = []
        self.ansatz = []
        self.optimizer = optimizer

    def add_run(self, result, molecule, hamiltonian, ansatz):
        self.results.append(result)
        self.molecules.append(str(molecule))
        self.hamiltonian.append(hamiltonian)
        self.ansatz.append(ansatz)

    def push(self):
        result_json = {"result":str(self.results),
            "hamiltonian":str(self.hamiltonian),
            "ansatz":str(self.ansatz),
            "optimizer":str(self.optimizer),
            "molecule":str(self.molecules)}
        response = requests.post(url, data=result_json)
        return response

    def __str__(self):
        return f"""Collected: {len(self.results)} results,
            {len(self.hamiltonian)} hamiltonians,
            {len(self.ansatz)} ansatz,
            {len(self.molecules)} molecules,
            with optimizer: {self.optimizer}""" 