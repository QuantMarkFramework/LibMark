# LibMark2
A simple python package for sending VQE run results to WebMark2

## Using the package

Make sure that the package is somewhere in your PYTHONPATH, then after using
```
from QuantMark import Qresult

qresult = Qresult(optimizer)
```
where "optimizer" is simply a string (name of optimizer used)

Data can be added to the object using
```
qresult.add_run(results, molecule, hamiltonian, ansatz)
```
More info about the fields can be found from the [docstring](https://github.com/quantum-ohtu/LibMark2/blob/main/QuantMark/result_sender.py) of the function.

Data can be sent to [WebMark2](https://github.com/quantum-ohtu/WebMark2), by calling the ```push``` function of ```Qresult```
```
qresult.push()
```

Example usage:

![image](https://github.com/quantum-ohtu/LibMark2/blob/main/images/generic_vqe.png)
