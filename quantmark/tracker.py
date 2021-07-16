from .result_scipy import QuantMarkResultScipy
from .result_gradient import QuantMarkResultGradient

scipy_optimizers = ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]
gradient_optimizers = [
    "ADAM", "ADAGRAD", "ADAMAX", "NADAM", "SGD", "MOMENTUM",
    "NESTEROV", "RMSPROP", "RMSPROP-NESTEROV", "SPSA"
    ]


def get_tracker(optimizer):
    if optimizer.upper() in scipy_optimizers:
        return QuantMarkResultScipy(optimizer)
    elif optimizer.upper() in gradient_optimizers:
        return QuantMarkResultGradient(optimizer)
    else:
        raise ValueError(f"{optimizer.upper()} not supported.")
