from result_scipy import QuantMarkResultScipy
from result_nesterov import QuantMarkResultNesterov

scipy_optimizers = ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]
nesterov = "NESTEROV"


def get_tracker(optimizer):
    if optimizer.upper() in scipy_optimizers:
        return QuantMarkResultScipy(optimizer)
    elif optimizer.upper() is nesterov:
        return QuantMarkResultNesterov(optimizer)
    else:
        raise ValueError("Optimizer not supported.")
