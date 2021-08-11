# LibMark quickstart guide (for Linux)

For creating a virtual environment in which to run LibMark, you should start by [getting Miniconda](https://docs.conda.io/en/latest/miniconda.html) (A good little resource for the use of Conda is the [Conda cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf))

Some of Tequila's dependencies require Python 3.7, so the virtual environment should be set to use that. The command to create environments is

```
conda create --name [environment name] python=3.7
```

where the [environment name] is of your choosing. To use the environment:

```
conda activate [environment name]
```

LibMark is currently dependent on [Tequila](https://github.com/aspuru-guzik-group/tequila), so naturally it should be installed:

```
pip install tequila-basic
```

Tequila supports various quantum backends that are not automatically installed with Tequila. They are listed on [Tequila's project page](https://github.com/aspuru-guzik-group/tequila#quantum-backends), and you might need at least some of them at some time. At the moment of writing, all of these backends can be installed with pip.

What is not installable through pip, but is currently essential for the use of Tequila with LibMark, is [psi4](https://github.com/psi4/psi4). It can be installed with:

```
conda install psi4 -c psi4
```

More about psi4 and quantum chemistry packages in [Tequila's readme](https://github.com/aspuru-guzik-group/tequila#quantumchemistry).
