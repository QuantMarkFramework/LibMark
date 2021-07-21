import unittest
from quantmark.result_sender import Results
import random


class TestResultSender(unittest.TestCase):

    def mock_vqe(self, molecules, hamiltonian, ansatz, optimizer):
        results = Results(optimizer)
        for molecule in molecules:
            H = hamiltonian(molecule)
            U = ansatz(molecule)
            result = mockResult()
            results.add_run(result, molecule, H, U)
        return results

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
        results = self.mock_vqe(mol, h_func, ansatz_func, 'Nelder-Mead')
        print(results.get_result_dict())

        self.assertEqual(n, len(results.energies))
        self.assertEqual(n, len(results.hamiltonian))
        self.assertEqual(n, len(results.molecules))

    def test_optimizer_is_correct(self):
        results = Results('Nelder-Mead')
        self.assertEqual(results.optimizer, 'Nelder-Mead')


class mockResult:
    def __init__(self):
        self.energy = 2,
        self.variables = 'mock_variables',
        self.history = 'mock_history',
        self.scipy_result = 'mock_scipy_results'


if __name__ == '__main__':
    unittest.main()
