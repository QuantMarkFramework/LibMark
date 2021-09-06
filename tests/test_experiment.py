import unittest
import ast, os, sys  # noqa
from libmark.experiment import QleaderExperiment


class testExperiment(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(sys.path[0], 'tests/test_data.txt'), 'r') as file: # noqa
            self.experiment = QleaderExperiment(**ast.literal_eval(file.read())) # noqa

    def test_vqe_run_success(self):
        result = self.experiment.run_experiment()
        self.assertEqual(result[0][0], 0.5)
        self.assertEqual(round(result[0][1].energy, 3), 1.058)
