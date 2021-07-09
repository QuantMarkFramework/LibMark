from .result_scipy import QuantMarkResultScipy
from .result_nesterov import QuantMarkResultNesterov
from .result import QuantMarkResult
from .tracker import get_tracker

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
