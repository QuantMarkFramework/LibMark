# LibMark2
A simple python package for sending VQE run results to WebMark2

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

![image](https://github.com/quantum-ohtu/LibMark2/blob/main/images/vqe.png)
