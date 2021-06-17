import requests
import json
import tequila

# Use this (or wherever your local WebMark2 is running) while developing
# url = 'http://0.0.0.0:8000/api/'
url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'


class Qresult:
    """
    A class to capture data from a VQE run.
    ---
    Attributes
    ----------
    results : str[]
        results returned by tq.minimize in str form
    molecules : str[]
        tequila molecule objects in str form
    hamiltonian : str[]
        hamiltonians in str form
    ansatz : str[]
        ansatz in str form

    Methods
    -------
    add_run(result, molecule, hamiltonian, ansatz)
    push()
    """
    def __init__(self, optimizer):
        self.scipy_results = []
        self.energies = []
        self.variables = []
        self.histories = []
        self.molecules = []
        self.hamiltonian = []
        self.ansatz = []
        self.optimizer = optimizer
        self.tqversion = tequila.__version__
        self.distances = []

    def make_history_dict(self, history):
        h_dict = {}
        h_dict['history_energies'] = history.energies
        h_dict['gradients'] = history.gradients
        h_dict['angles'] = str(history.angles)
        h_dict['energies_calls'] = history.energies_calls
        h_dict['gradients_calls'] = history.gradients_calls
        h_dict['angles_calls'] = history.angles_calls
        return h_dict

    def make_scipy_result_dict(self, scipy_result):
        sr_dict = {}
        sr_dict['final_simplex'] = str(scipy_result.final_simplex)
        sr_dict['fun'] = scipy_result.fun
        sr_dict['message'] = str(scipy_result.message)
        sr_dict['nfev'] = scipy_result.nfev
        sr_dict['nit'] = scipy_result.nit
        sr_dict['status'] = scipy_result.status
        sr_dict['success'] = str(scipy_result.success)
        sr_dict['x'] = str(scipy_result.x)
        return sr_dict

    def add_run(self, result, molecule, hamiltonian, ansatz):
        """Add VQE run to the QResult

        Parameters
        ----------
        result : tequila.optimizers.optimizer_scipy.SciPyResults
            object returned by tq.minimize
        molecule : tequila.quantumchemistry.psi4_interface.QuantumChemistryPsi4
            molecule used in the run
        hamiltonian : tequila.hamiltonian.qubit_hamiltonian.QubitHamiltonian
            object returned by molecule.make_hamiltonian()
        ansatz : tequila.circuit.circuit.QCircuit
            object returned by molecule.make_uccsd_ansatz()
        """
        # FIXME calling str(*something*) to make the data JSON serializable
        # is lazy, need to find a more elegant way to do this.
        self.energies.append(result.energy)
        self.variables.append(str(result.variables).replace('\n', ' '))
        self.histories.append(str(self.make_history_dict(result.history)))
        self.scipy_results.append(
            str(self.make_scipy_result_dict(result.scipy_result))
            )
        self.molecules.append(str(molecule))
        self.hamiltonian.append(str(hamiltonian))
        self.ansatz.append(str(ansatz))
        self.distances.append(molecule.parameters.get_geometry()[-1][-1][-1])

    def get_result_dict(self):
        result = {"energies": self.energies,
                  "variables": self.variables,
                  "histories": self.histories,
                  "scipy_results": self.scipy_results,
                  "hamiltonian": self.hamiltonian,
                  "ansatz": self.ansatz,
                  "optimizer": self.optimizer,
                  "molecule": self.molecules,
                  "tqversion": self.tqversion,
                  "distances": self.distances
                  }
        return result

    def push(self):
        """Send Qresult to server"""
        result = self.get_result_dict()
        response = requests.post(url, json=json.dumps(result, indent=4))
        return response

    def __str__(self):
        return f"""Collected: {len(self.energies)} results,
            {len(self.hamiltonian)} hamiltonians,
            {len(self.ansatz)} ansatz,
            {len(self.molecules)} molecules,
            with optimizer: {self.optimizer},
            Tequila: {self.tqversion}"""
