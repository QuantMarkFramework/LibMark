# LibMark2
A simple python package for sending VQE run results to WebMark2

## Using the package

Make sure that the package is somewhere in your PYTHONPATH, then after using
```
from QuantMark import push_results
```
data can be sent to [WebMark2](https://github.com/quantum-ohtu/WebMark2), using
```
push_results(data)
```
Currently all sorts of data is accepted without restrictions.
