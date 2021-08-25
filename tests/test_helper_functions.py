import unittest
from libmark.result_scipy import QleaderResultScipy as qr_scipy
import tequila as tq


class testHelperFuntions(unittest.TestCase):

    def setUp(self):
        geometry = f'H 0.0 0.0 0.0\nH 0.0 0.0 {0.5}'
        mole = tq.chemistry.Molecule(geometry=geometry,
                                     basis_set="sto-3g",
                                     transformation="Jordan-Wigner")
        self.ansatz = mole.make_uccsd_ansatz(trotter_steps=2)

    def test_ansatz(self):
        result = qr_scipy("Nelder-Mead", "mock_token")
        ansatz = result.extract_gates(self.ansatz)
        # Ansatz is list
        self.assertIsInstance(ansatz[0], list)
        # Gate depth is correct
        self.assertEqual(ansatz[1], 145)
        # Single qubit gate count is correct
        self.assertEqual(ansatz[2], 146)
        # Double qubit gate count is correct
        self.assertEqual(ansatz[3], 96)
