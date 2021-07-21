from quantmark.result_scipy import QuantMarkResultScipy
from quantmark.result_gradient import QuantMarkResultGradient
import unittest
from quantmark.tracker import get_tracker


class TestTracker(unittest.TestCase):

    def test_unsupportedOptimizer(self):
        self.assertRaises(ValueError, get_tracker, ("nonexistent"))

    def test_scipyOptimizer(self):
        self.assertIsInstance(get_tracker("bfgs"), QuantMarkResultScipy)
    
    def test_gradientOptimizer(self):
        self.assertIsInstance(get_tracker("nesterov"), QuantMarkResultGradient)


if __name__ == '__main__':
    unittest.main()
