from .result import QleaderResult


class QleaderResultScipy(QleaderResult):
    def __init__(self, optimizer, token):
        super().__init__(optimizer, token)
        self.scipy_results = []

    def make_scipy_result_dict(self, scipy_result):
        scipy_result_dict = {}
        for key in scipy_result.keys():
            scipy_result_dict[key] = str(scipy_result.get(key))
        return scipy_result_dict

    def get_transformation(self, molecule):
        return super().get_transformation(molecule)

    def add_run(self, run, molecule, hamiltonian, ansatz):
        super().add_run(run, molecule, hamiltonian, ansatz)
        self.scipy_results.append(str(
            self.make_scipy_result_dict(run.scipy_result)
        ))

    def get_result_dict(self):
        result = {"energies": self.energies,
                  "variables": self.variables,
                  "histories": self.histories,
                  "scipy_results": self.scipy_results,
                  "hamiltonian": self.hamiltonian,
                  "ansatz": self.ansatz,
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
