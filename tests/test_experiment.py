import unittest
import ast, os, sys  # noqa
from quantmark.experiment import QuantMarkExperiment


class testExperiment(unittest.TestCase):

    def setUp(self):
        self.experiment = QuantMarkExperiment(**ast.literal_eval(
            open(os.path.join(sys.path[0], 'tests/test_data.txt'), 'r').read()
        ))

    def test_vqe_run_success(self):
        result = self.experiment.run_experiment()
        self.assertEqual(result[0][0], 0.5)
