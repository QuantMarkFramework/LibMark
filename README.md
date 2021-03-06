# LibMark2
[![codecov](https://codecov.io/gh/quantum-ohtu/LibMark2/branch/main/graph/badge.svg?token=GSS0W01NXZ)](https://codecov.io/gh/quantum-ohtu/LibMark2)

A simple python package for sending and pulling VQE run results to/from WebMark2

## Getting started

You can check the currently viable guide on how to get started with Libmark from the [quickstart guide](documentation/quickstart.md).

There is also an example [notebook](https://github.com/quantum-ohtu/QuantMark/blob/main/QuantMark_demo.ipynb) available which showcases the functionality.

## Using the package

Make sure that the package is somewhere in your PYTHONPATH, then after using
```
from LibMark2.quantmark.tracker import get_tracker

qresult = get_tracker(optimizer, 'TOKEN')
```
where "optimizer" is simply a string (name of optimizer used). The token can be acquired from the Quantmark website.
'get_tracker' returns the correct Result object.

Data can be added to the object using
```
qresult.add_run(results, molecule, hamiltonian, ansatz)
```
Where 'results' is an object returned by tq.minimize.

Data can be sent to [WebMark2](https://github.com/quantum-ohtu/WebMark2), by calling the ```push``` function of any Result object
```
qresult.push()
```
Want to save the data?
```
qresult.save()
```
will save a JSON file to the root.

### Pushing

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

### Pulling

You can pull any public result (or your own result) from WebMark:
```python
from LibMark2.quantmark.api import get_experiment, get_data

data = get_data(id, 'TOKEN_HERE') # Download all available information as a dict
experiment = get_experiment(id, 'TOKEN_HERE') # Download experiment
results = experiment.run_experiment() # Run the experiment
```

"results" will contain a list of tuples (distance, results)


