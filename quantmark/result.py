from abc import ABC, abstractmethod
import tequila
import requests
import json

# Use this (or wherever your local WebMark2 is running) while developing
# url = 'http://0.0.0.0:8000/api/'
url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'


class QuantMarkResult(ABC):
    def __init__(self, optimizer):
        self.energies = []
        self.variables = []
        self.histories = []
        self.molecules = []
        self.hamiltonian = []
        self.ansatz = []
        self.optimizer = optimizer
        self.tqversion = tequila.__version__
        self.basis_set = None
        self.transformation = None
        self.distances = []

    def get_transformation(self, molecule):
        # Parsing the transformation name is a bit of a hassle
        # try-except so that it doesn't cause the whole collection to fail
        try:
            t = str(molecule.transformation)
            t_name = t.split('function')[1].split('at')[0].strip()
            return t_name
        except Exception:
            if len(t.split()) == 1:
                return t
            return ' '

    def add_run(self, run, molecule, hamiltonian, ansatz):
        """Add VQE run to the Results

        Parameters
        ----------
        result:
            object returned by tq.minimize
        molecule : tequila.quantumchemistry.psi4_interface.QuantumChemistryPsi4
            molecule used in the run
        hamiltonian : tequila.hamiltonian.qubit_hamiltonian.QubitHamiltonian
            object returned by molecule.make_hamiltonian()
        ansatz : tequila.circuit.circuit.QCircuit
            object returned by molecule.make_uccsd_ansatz()
        """
        self.energies.append(run.energy)
        self.variables.append(str(run.variables).replace('\n', ' '))
        self.histories.append(str(run.history.__dict__))
        self.molecules.append(str(molecule))
        self.hamiltonian.append(str(hamiltonian))
        self.ansatz.append(str(ansatz))
        self.distances.append(molecule.parameters.get_geometry()[-1][-1][-1])
        self.basis_set = molecule.parameters.basis_set
        self.transformation = self.get_transformation(molecule)
        pass

    @abstractmethod
    def get_result_dict(self):
        pass

    def push(self):
        """Send Results to server"""
        result = self.get_result_dict()
        response = requests.post(url, json=json.dumps(result, indent=4))
        return response

    def save(self, file=""):
        """Save data locally for testing and verification"""
        if not file:
            from datetime import datetime
            now = datetime.now()
            file = self.optimizer + " " + str(now) + ".json"     # There is a space in 'now' already
        output = open(file, 'w')
        result = self.get_result_dict()
        output.write(json.dumps(result, indent=4))
        return

    def __str__(self):
        return f"""Collected: {len(self.energies)} results,
            {len(self.hamiltonian)} hamiltonians,
            {len(self.ansatz)} ansatz,
            {len(self.molecules)} molecules,
            with optimizer: {self.optimizer},
            Tequila: {self.tqversion}"""
