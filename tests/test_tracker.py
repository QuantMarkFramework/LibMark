from quantmark.result_scipy import QuantMarkResultScipy
from quantmark.result_gradient import QuantMarkResultGradient
import unittest
from quantmark.tracker import get_tracker


class TestTracker(unittest.TestCase):

    def test_unsupportedOptimizer(self):
        self.assertRaises(ValueError, get_tracker, "nonexistent", "token")

    def test_scipyOptimizer(self):
        self.assertIsInstance(get_tracker("bfgs", "token"), QuantMarkResultScipy)  # noqa

    def test_gradientOptimizer(self):
        self.assertIsInstance(get_tracker("nesterov", "token"), QuantMarkResultGradient)  # noqa

    def test_(self):
        qmrs = get_tracker("nelder-mead", "token")
        self.assertEqual(str.upper(qmrs.optimizer), str.upper('Nelder-Mead'))


if __name__ == '__main__':
    unittest.main()
