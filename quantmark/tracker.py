from .result_scipy import QleaderResultScipy
from .result_gradient import QleaderResultGradient

scipy_optimizers = ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]
gradient_optimizers = [
    "ADAM", "ADAGRAD", "ADAMAX", "NADAM", "SGD", "MOMENTUM",
    "NESTEROV", "RMSPROP", "RMSPROP-NESTEROV", "SPSA"
    ]


def get_tracker(optimizer, token):
    if optimizer.upper() in scipy_optimizers:
        return QleaderResultScipy(optimizer, token)
    elif optimizer.upper() in gradient_optimizers:
        return QleaderResultGradient(optimizer, token)
    else:
        raise ValueError(f"{optimizer.upper()} not supported.")
