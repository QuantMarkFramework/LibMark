# QuantMark Library (LibMark)
The QuantMark library can be used to analyze VQE-algorithms. The functionalities of the library buildon top of [tequila](https://github.com/aspuru-guzik-group/tequila).

## Installation
> Currently this library supports only python 3.7

Before installing the library it is recommended to install psi4 if you want to use molecules. It is recommended to use conda for easy installation (
[instructions](#Setting-up-conda-environment)).

```
git clone https://github.com/ohtu2021-kvantti/LibMark.git
cd LibMark
pip install .
```

You also need to install the quantum backends that you intend to use. In the example below qulacs is used.
```
pip install qulacs
```

### Setting up conda environment
```shell
conda create -n envname python=3.7 # Create environment.

conda activate envname # Activate to environment.

conda install psi4 -c psi4 # Install psi4.

# Clone LibMark and move into the created folder.

pip install . # Install quantmark.

pip install qulacs # Install qulacs (and or any other quantum backend).
```

## Usage
LibMark is relying stongly on [tequila](https://github.com/aspuru-guzik-group/tequila).
```python
import quantmark as qm
import tequila as tq

# Define optimizer.
optimizer = qm.QMOptimizer(module="scipy", method="BFGS")

# Define backend.
backend = qm.QMBackend(backend='qulacs')

# Make tequila molecule object.
molecule = tq.chemistry.Molecule(
    geometry='H 0.0 0.0 0.0\nH 0.0 0.0 1.6',
    basis_set='sto-3g'
)

# Make tequila circuit.
circuit = molecule.make_uccsd_ansatz(trotter_steps=1)

# Run the benchmark.
algorithm = qm.VQEAlgorithm(
    molecule=molecule,
    circuit=circuit,
    optimizer=optimizer,
    backend=backend,
    repetitions=10
)

# Analyze the algorithm.
print(algorithm.analyze())

# Analyze only circuit (Does not run the algorithm).
print(algorithm.analyze_circuit())
```
```python
# Changing parts between analyzing (can change one or multiple).
algorithm.molecule = new_molecule
algorithm.circuit = new_circuit
algorithm.optimizer = new_optimizer
algorithm.backend = new_backend

print(algorithm.analyze())
```
## Contributing
You can add an issue or add code with the usual fork(or branch), do, pull request system.

### Setting up development environment
The same as normal installation, but in editable mode.
```python
pip install -e .
```
Also it is recommended to install the testing and linting libraries.
```python
pip install pytest
pip install flake8
```
### Testing
To run tests use the command `pytest` in the project root folder.

### Linting
To run linter use the command `flake8` in the project root folder. Flake8 does not give an error when using spaces for indentation, but please use tabs.
