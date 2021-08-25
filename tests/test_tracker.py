from libmark.result_scipy import QleaderResultScipy
from libmark.result_gradient import QleaderResultGradient
import unittest
from libmark.tracker import get_tracker


class TestTracker(unittest.TestCase):

    def test_unsupportedOptimizer(self):
        self.assertRaises(ValueError, get_tracker, "nonexistent", "token")

    def test_scipyOptimizer(self):
        self.assertIsInstance(get_tracker("bfgs", "token"), QleaderResultScipy)  # noqa

    def test_gradientOptimizer(self):
        self.assertIsInstance(get_tracker("nesterov", "token"), QleaderResultGradient)  # noqa

    def test_(self):
        qmrs = get_tracker("nelder-mead", "token")
        self.assertEqual(str.upper(qmrs.optimizer), str.upper('Nelder-Mead'))


if __name__ == '__main__':
    unittest.main()
