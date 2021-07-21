#from quantmark.result_scipy import QuantMarkResultScipy
#from quantmark.result_gradient import QuantMarkResultGradient
#from quantmark.result import QuantMarkResult
import unittest
# from quantmark.result import QuantMarkResult
from quantmark.tracker import get_tracker
import random
# from unittest.mock import create_autospec

class testResultScipy(unittest.TestCase):

    def mock_vqe(self, molecules, hamiltonian, ansatz, optimizer):
        runs = get_tracker(optimizer)
        for molecule in molecules:
            H = mockHamiltonian()
            U = mockAnsatz()
            result = mockScipyRun()
            runs.add_run(result, molecule, H, U)
        return runs

    def mock_hamiltonian_function(self, molecule):
        return f'hamiltonian_from_{molecule}'

    def mock_ansatz_function(self, molecule):
        return f'ansatz_from_{molecule}'

    
    def test_number_of_runs_remains(self):
        n = random.randint(0, 10)
        mol = [mockMolecule() for i in range(n)]
        h_func = self.mock_hamiltonian_function
        ansatz_func = self.mock_ansatz_function
        runs = self.mock_vqe(mol, h_func, ansatz_func, 'Nelder-Mead')

        self.assertEqual(n, len(runs.energies))
        self.assertEqual(n, len(runs.hamiltonian))
        self.assertEqual(n, len(runs.molecules))
    

    def test_add_non_compatible_run(self):
        qmrs = get_tracker("nelder-mead")
        mol = mockFaultyMolecule()
        H = mockHamiltonian()
        U = mockAnsatz()
        run = mockScipyRun()
        self.assertRaises(TypeError, qmrs.add_run, (run, mol, H, U))


'''Below are mocked classes. They could be replaced with actual python mocks later.'''
class mockScipyRun():
    def __init__(self):
        self.energy = 0.616,
        self.variables = 'mock_variables',
        mockH = mockHistory.__init__
        self.history = mockH
        self.scipy_result = {'result1': 'wesult', 'result2': 'yesult'}

class mockHistory:
    def __init__(self):
        self.attributeOne = 1
        self.attributeTwo = 2

class mockMolecule:
    def __init__(self):
        self.parameters = mockParameters()
        self.transformation = 'mockedTrasformation'

class mockParameters():
    def get_geometry(self):
        return [[[1]]]
    
    def basis_set(self):
        return 'mockedBasisSet'

class mockFaultyMolecule:
    def __init__(self):
        self.parameters = mockFaultyParameters()
        self.transformation = 'mockedTrasformation'

class mockFaultyParameters():
    '''get_geometry includes a purposeful error'''
    def get_geometry(self):
        return [[1], [1]]
    
    def basis_set(self):
        return 'mockedBasisSet'

class mockHamiltonian():
    def __init__(self):
        self.qubits = [0, 1, 2]
    
    def __str__(self):
        return "this is a Hamiltonian"

class mockAnsatz():
    def __init__(self):
        self.depth = 5


if __name__ == '__main__':
    unittest.main()


'''
class testResultGradient(unittest.TestCase):

    def __init__(self):
        self.qmr = QuantMarkResult

'''