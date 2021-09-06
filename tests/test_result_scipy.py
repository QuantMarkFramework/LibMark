import unittest
import pathlib as pl
from libmark.tracker import get_tracker


class testResultScipy(unittest.TestCase):

    def setUp(self):
        self.run = mockScipyRun()
        self.H = mockHamiltonian()
        self.U = mockAnsatz()

    def mock_vqe(self, molecules, optimizer):
        runs = get_tracker(optimizer, "token")
        for molecule in molecules:
            runs.add_run(self.run, molecule, self.H, self.U)
        return runs

    def mock_hamiltonian_function(self, molecule):
        return f'hamiltonian_from_{molecule}'

    def mock_ansatz_function(self, molecule):
        return f'ansatz_from_{molecule}'

    def test_number_of_runs_remains(self):
        n = 6
        mol = [mockMolecule() for i in range(n)]
        runs = self.mock_vqe(mol, 'Nelder-Mead')

        self.assertEqual(n, len(runs.energies))
        self.assertEqual(n, len(runs.hamiltonian))
        self.assertEqual(n, len(runs.molecules))

    def test_add_non_compatible_run(self):
        qmrs = get_tracker("nelder-mead", "token")
        mol = mockFaultyMolecule()
        self.assertRaises(TypeError, qmrs.add_run,
                          (self.run, mol, self.H, self.U))

    def test_save(self):
        mol = [mockMolecule()]
        runs = self.mock_vqe(mol, 'Nelder-Mead')
        runs.save("testfile.json")

        with pl.Path("./testfile.json") as f:
            self.assertTrue(f.is_file())
            testStr = f.read_text().split()[1].split("\"")[1]
            self.assertEqual("energies", testStr)
            f.unlink()


'''
Below are mocked classes. They could be
replaced with actual python mocks later.
'''


class mockScipyRun():
    def __init__(self):
        self.energy = 0.616,
        self.variables = 'mock_variables',
        mockH = mockHistory.__init__
        self.history = mockH
        self.scipy_result = {'result1': 'wesult', 'result2': 'yesult'}


class mockHistory():
    def __init__(self):
        self.attributeOne = 1
        self.attributeTwo = 2


class mockMolecule():
    def __init__(self):
        self.parameters = mockParameters()
        self.transformation = 'mockedTrasformation'

    def __str__(self):
        return 'mockMolecule as str'


class mockParameters():

    def __init__(self):
        self.basis_set = 'mockedBasisSet'

    def get_geometry(self):
        return [[[1]]]


class mockFaultyMolecule():
    def __init__(self):
        self.parameters = mockFaultyParameters()
        self.transformation = 'mockedTrasformation'


class mockFaultyParameters():

    def __init__(self):
        self.basis_set = 'mockedBasisSet'

    '''get_geometry includes a purposeful error'''

    def get_geometry(self):
        return [[1], [1]]


class mockHamiltonian():
    def __init__(self):
        self.qubits = [0, 1, 2]

    def __str__(self):
        return "this is a Hamiltonian"


class mockAnsatz():
    def __init__(self):
        self.depth = 5

    def __str__(self):
        return f'Ansatz.depth is {self.depth}'


if __name__ == '__main__':
    unittest.main()
