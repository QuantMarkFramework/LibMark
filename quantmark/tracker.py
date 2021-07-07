from result_scipy import QuantMarkResultScipy
from result_nesterov import QuantMarkResultNesterov

scipy_optimizers = ["NELDER-MEAD", "BFGS", "L-BFGS-B", "COBYLA"]

def get_tracker(optimizer):
    if optimizer.upper() in scipy_optimizers:
        return QuantMarkResultScipy(optimizer)
    elif optimizer.upper() == "NESTEROV":
        return QuantMarkResultNesterov(optimizer)
    else:
        raise ValueError(f"{optimizer.upper()} not supported.")
