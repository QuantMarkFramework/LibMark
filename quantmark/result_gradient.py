from .result import QuantMarkResult


class QuantMarkResultGradient(QuantMarkResult):
    def __init__(self, optimizer, token):
        super().__init__(optimizer, token)
        self.moments = []

    def get_transformation(self, molecule):
        return super().get_transformation(molecule)

    def add_run(self, run, molecule, hamiltonian, ansatz):
        super().add_run(run, molecule, hamiltonian, ansatz)
        # Just do lazy appending for now.
        self.moments.append(str(run.moments))

    def get_result_dict(self):
        result = {
            "energies": self.energies,
            "variables": self.variables,
            "histories": self.histories,
            "moments": self.moments,
            "hamiltonian": self.hamiltonian,
            "ansatz": self.ansatz,
            "optimizer": self.optimizer,
            "qubits": self.qubits,
            "depth": self.depth,
            "molecule": self.molecules,
            "tqversion": self.tqversion,
            "distances": self.distances,
            "basis_set": self.basis_set,
            "transformation": self.transformation
        }
        return result

    def push(self):
        return super().push()

    def save(self, file=""):
        return super().save(file)

    def __str__(self):
        return super().__str__()
