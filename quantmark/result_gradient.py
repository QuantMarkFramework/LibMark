from .result import QleaderResult


class QleaderResultGradient(QleaderResult):
    def __init__(self, optimizer, token):
        super().__init__(optimizer, token)
        self.moments = []

    def get_transformation(self, molecule):
        return super().get_transformation(molecule)

    def add_run(self, run, molecule, hamiltonian, ansatz):
        super().add_run(run, molecule, hamiltonian, ansatz)
        self.moments.append(str(run.moments))

    def get_result_dict(self):
        result = {
            "energies": self.energies,
            "variables": self.variables,
            "histories": self.histories,
            "moments": self.moments,
            "hamiltonian": self.hamiltonian,
            "ansatz": self.ansatz,
            "single_qubit": self.single_qubit,
            "double_qubit": self.double_qubit,
            "optimizer": self.optimizer,
            "qubits": self.qubits,
            "fermionic_depth": self.fermionic_depth,
            "elementary_depth": self.elementary_depth,
            "molecule": self.molecules,
            "tqversion": self.tqversion,
            "geometries": self.geometries,
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
