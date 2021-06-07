import requests

# Use this (or wherever your local WebMark2 is running) while developing
url = 'http://0.0.0.0:8000/api/'
# url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'


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
        self.results = []
        self.molecules = []
        self.hamiltonian = []
        self.ansatz = []
        self.optimizer = optimizer

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
        self.results.append(str(result))
        self.molecules.append(str(molecule))
        self.hamiltonian.append(str(hamiltonian))
        self.ansatz.append(str(ansatz))

    def push(self):
        """Send Qresult to server"""
        result_json = {"result": self.results,
                       "hamiltonian": self.hamiltonian,
                       "ansatz": self.ansatz,
                       "optimizer": self.optimizer,
                       "molecule": self.molecules}
        response = requests.post(url, data=result_json)
        return response

    def __str__(self):
        return f"""Collected: {len(self.results)} results,
            {len(self.hamiltonian)} hamiltonians,
            {len(self.ansatz)} ansatz,
            {len(self.molecules)} molecules,
            with optimizer: {self.optimizer}"""
