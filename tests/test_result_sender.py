import unittest
from quantmark.result_sender import Qresult
import random


class TestResultSender(unittest.TestCase):

    def mock_vqe(self, molecules, hamiltonian, ansatz, optimizer):
        qresult = Qresult(optimizer)
        for molecule in molecules:
            H = hamiltonian(molecule)
            U = ansatz(molecule)
            result = mockResult()
            qresult.add_run(result, molecule, H, U)
        return qresult

    def mock_hamiltonian_function(self, molecule):
        return f'hamiltonian_from_{molecule}'

    def mock_ansatz_function(self, molecule):
        return f'ansatz_from_{molecule}'

    def test_data_collection(self):
        """Make sure that at least the correct amount of data is collected"""
        n = random.randint(0, 10)
        mol = [f'mol{i}' for i in range(n)]
        h_func = self.mock_hamiltonian_function
        ansatz_func = self.mock_ansatz_function
        qresult = self.mock_vqe(mol, h_func, ansatz_func, 'Nelder-Mead')
        print(qresult.get_result_dict())

        self.assertEqual(n, len(qresult.energies))
        self.assertEqual(n, len(qresult.hamiltonian))
        self.assertEqual(n, len(qresult.molecules))

    def test_optimizer_is_correct(self):
        qresult = Qresult('Nelder-Mead')
        self.assertEqual(qresult.optimizer, 'Nelder-Mead')


class mockResult:
    def __init__(self):
        self.energy = 2,
        self.variables = 'mock_variables',
        self.history = 'mock_history',
        self.scipy_result = 'mock_scipy_results'


if __name__ == '__main__':
    unittest.main()
