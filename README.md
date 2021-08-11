# LibMark2
[![codecov](https://codecov.io/gh/quantum-ohtu/LibMark2/branch/main/graph/badge.svg?token=GSS0W01NXZ)](https://codecov.io/gh/quantum-ohtu/LibMark2)

A simple python package for sending VQE run results to WebMark2

## Getting started

You can check the currently viable guide on how to get started with Libmark from the [quickstart guide](documentation/quickstart.md).

## Using the package

Make sure that the package is somewhere in your PYTHONPATH, then after using
```
from LibMark2.quantmark.tracker import get_tracker

qresult = get_tracker(optimizer)
```
where "optimizer" is simply a string (name of optimizer used). 'get_tracker' returns the correct Result object.

Data can be added to the object using
```
qresult.add_run(results, molecule, hamiltonian, ansatz)
```
Where 'results' is an object returned by tq.minimize. As of 11.7.2021 the three other fields (molecule, hamiltonian, ansatz) can be pretty much anything, since they are just stored as strings in WebMark2.

Data can be sent to [WebMark2](https://github.com/quantum-ohtu/WebMark2), by calling the ```push``` function of any Result object
```
qresult.push()
```
Want to save the data? With a
```
qresult.save()
```
JSON file will be created to the root.

Example usage:

```python
# Generic batch optimize for "any" VQE
def run_vqe(molecules, hamiltonian_function, ansatz_function, optimizer, silent=True, **ansatz_kwargs):
    results = []
    qresult = get_tracker(optimizer, 'TOKEN_HERE') # Start quantmark tracking
    for i, molecule in enumerate(molecules):
        print(str(i+1)+"/"+str(len(molecules)), end="\t")
        print("Creating the Hamiltonian.", end="\t")
        H = hamiltonian_function(molecule)
        n_qubits = len(H.qubits)
        print("Creating ansatz.", end="\t")
        U = ansatz_function(molecule=molecule, n_qubits=n_qubits, **ansatz_kwargs)
        print("Creating objective function")
        E = tq.ExpectationValue(H=H, U=U)
        variables = {k:0.0 for k in U.extract_variables()}
        print("Optimizing.", end="\t")
        result = tq.minimize(objective=E, method=optimizer, initial_values=variables, silent=silent)
        print()
        results.append(result)
        qresult.add_run(result, molecule, H, U) # Adding the intermediate result
    print("Done")
    qresult.push() # Push results to the server
    qresult.save() # Save the data to a JSON file
    return results
```

The token can be aqcuired from the quantmark website.
