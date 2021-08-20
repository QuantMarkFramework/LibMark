from abc import ABC, abstractmethod
from tequila.circuit.compiler import Compiler
from datetime import datetime
import tequila as tq
import requests
import json


# Use this (or wherever your local WebMark2 is running) while developing
# url = 'http://localhost:8000/api/'
url = 'https://ohtup-staging.cs.helsinki.fi/qleader/api/'

DEFAULT_COMPILER_ARGUMENTS = {
    "multitarget": True,
    "multicontrol": True,
    "trotterized": True,
    "generalized_rotation": True,
    "exponential_pauli": True,
    "controlled_exponential_pauli": True,
    "hadamard_power": True,
    "controlled_power": True,
    "power": True,
    "toffoli": True,
    "controlled_phase": False,
    "phase": True,
    "phase_to_z": False,
    "controlled_rotation": True,
    "swap": True,
    "cc_max": True,
    "ry_gate": False,
    "y_gate": False,
    "ch_gate": True
}


class QleaderResult(ABC):
    def __init__(self, optimizer, token):
        self.compiler = Compiler(**DEFAULT_COMPILER_ARGUMENTS)
        self.token = f'Token {token}'
        self.energies = []
        self.variables = []
        self.histories = []
        self.molecules = []
        self.geometries = []
        self.hamiltonian = []
        self.qubits = []
        self.elementary_depth = []
        self.fermionic_depth = []
        self.ansatz = []
        self.single_qubit = []
        self.double_qubit = []
        self.optimizer = optimizer
        self.tqversion = tq.__version__
        self.basis_set = None
        self.transformation = None

    def get_transformation(self, molecule):
        try:
            t = str(molecule.transformation)
            t_name = t.split('function')[1].split('at')[0].strip()
            return t_name
        except Exception:
            if len(t.split()) == 1:
                return t
            return ' '

    # This operation takes some time to execute
    # TODO extract every run vs. extract all at once afterwards?
    def extract_gates(self, ansatz):
        try:
            circuit = self.compiler(ansatz)
        except Exception:
            circuit = ansatz
            print("Warning: could not extract gates from ansatz, \
                   the experiment will not be automatically reproducible!")
        counts = self.gate_qubit_counts(circuit)

        return (str(circuit).split('\n')[1:-1], circuit.depth, counts[0], counts[1])

    # Same possible problem as above
    def gate_qubit_counts(self, circuit):
        if circuit is not tq.QCircuit:
            pass

        counts = [0, 0]
        for gate in circuit.gates:
            qubits = len(gate.target) + len(gate.control)
            if qubits == 1:
                counts[0] += 1
            elif qubits == 2:
                counts[1] += 2
        return counts

    def add_run(self, run, molecule, hamiltonian, ansatz):
        """Add VQE run to the Results

        Parameters
        ----------
        run:
            object returned by tq.minimize
        molecule : tequila.quantumchemistry.psi4_interface.QuantumChemistryPsi4
            molecule used in the run
        hamiltonian : tequila.hamiltonian.qubit_hamiltonian.QubitHamiltonian
            object returned by molecule.make_hamiltonian()
        ansatz : tequila.circuit.circuit.QCircuit
            object returned by molecule.make_uccsd_ansatz()
        """
        elem_ansatz = self.extract_gates(ansatz)

        self.energies.append(run.energy)
        self.variables.append(str(run.variables).replace('\n', ' '))
        self.histories.append(str(run.history.__dict__))
        self.molecules.append(str(molecule))
        self.geometries.append(molecule.parameters.get_geometry())
        self.hamiltonian.append(str(hamiltonian))
        self.qubits.append(len(hamiltonian.qubits))  # the number of qubits
        self.fermionic_depth.append(ansatz.depth)  # Ansatz gate depth
        self.elementary_depth.append(elem_ansatz[1])
        self.ansatz.append([str(gate) for gate in elem_ansatz[0]])
        self.single_qubit.append(elem_ansatz[2])
        self.double_qubit.append(elem_ansatz[3])
        self.basis_set = molecule.parameters.basis_set
        self.transformation = self.get_transformation(molecule)

    @abstractmethod
    def get_result_dict(self):
        pass

    def push(self):
        """Send Results to server"""
        result = self.get_result_dict()
        headers = {
            'Authorization': self.token
        }
        response = requests.post(
                        url, json=json.dumps(result, indent=4), headers=headers
                    )
        return response

    def save(self, file=""):
        """Save data locally for testing and verification"""
        if not file:
            now = datetime.now()
            file = self.optimizer + " " + \
                self.transformation + " " + str(now) + ".json"
        output = open(file, 'w')
        result = self.get_result_dict()
        output.write(json.dumps(result, indent=4))
        output.close()
        return

    def __str__(self):
        return f"""Collected: {len(self.energies)} results,
            {len(self.hamiltonian)} hamiltonians,
            {len(self.ansatz)} ansatz,
            {len(self.molecules)} molecules,
            with optimizer: {self.optimizer},
            Tequila: {self.tqversion}"""
