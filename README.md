# QuantMark Library (LibMark)

## Installation
> Currently this library supports only python 3.7

Before installing the library it is recommended to install ps4 if you want to use molecules. It is recommended to use conda for easy installation.
```
conda install psi4 -c psi4
```

Install in editable mode (remove -e for normal mode).
```
git clone https://github.com/ohtu2021-kvantti/LibMark.git
cd LibMark
pip install -e .
```

You also need to install the quantum backends that you intend to use. In the example below qulacs is used.
```
pip install qulacs
```

## Example
```python
import quantmark as qm
import tequila as tq

# Define optimizer
optimizer = qm.QMOptimizer(module="scipy", method="BFGS")

# Define backend
backend = qm.QMBackend(backend='qulacs')

# Make tequila molecule object.
active_orbitals = {'A1':[1], 'B1':[0]}
molecule = tq.chemistry.Molecule(
	geometry='H 0.0 0.0 0.0\nLi 0.0 0.0 1.6',
	basis_set='sto-3g',
	active_orbitals=active_orbitals
)

# Make tequila circuit.
circuit = tq.gates.Ry(angle='a', target=0) + tq.gates.X(target=[2,3])
circuit += tq.gates.X(target=1, control=0)
circuit += tq.gates.X(target=2, control=0)
circuit += tq.gates.X(target=3, control=1)

# Run the benchmark
algorithm = qm.VQEAlgorithm(
	molecule=molecule,
	circuit=circuit,
	optimizer=optimizer,
	backend=backend,
	repetitions=100
)

# Print result
print(algorithm.analyze())
```

The circuit and molecule used are originally from [tequila-tutorials](https://github.com/aspuru-guzik-group/tequila-tutorials/blob/main/Chemistry.ipynb).

# Changing parts between analyzing
```python
algorithm.molecule = new_molecule
algorithm.circuit = new_circuit
algorithm.optimizer = new_optimizer
algorithm.backend = new_backend
```

# Setting up conda environment
```shell
# Create environment with python 3.7, change 'envname' to preferred name
conda create -n envname python=3.7

# Activate to environment
conda activate envname

# Install psi4
conda install psi4 -c psi4

# Move into the LibMark folder

# Install quantmark
pip install -e .

# Install qulacs (and or any other quantum backend)
pip install qulacs
```
