import typing
import tequila as tq
from dataclasses import dataclass
from tequila.circuit.circuit import QCircuit
from .vqe import run

# Heavily inspired by:
# https://github.com/ohtu2021-kvantti/LibMark/blob/main/quantmark/circuit.py


@dataclass
class Gate:
    name: str
    target: typing.List[str]
    control: typing.List[str] = None
    parameter: typing.Union[str, float] = None


class QleaderExperiment():
    """ An object which can be used to recreate a VQE result from the Quantmark website.

    ...

    Methods
    -------
    run_experiment()
        Runs the experiment and returns the results
    build_circuits()
        Builds a tequila.circuit.circuit.QCircuit objects and returns them
    """
    
    def __init__(self, **kwargs):
        self.distances = kwargs['distances']
        self.ansatz = kwargs['ansatz']
        self.transformation = kwargs['transformation']
        self.basis_set = kwargs['basis_set']
        self.optimizer = kwargs['optimizer']
        self.circuits = None

    def build_circuits(self):
        """Builds QCircuit object from 'self.ansatz'"""

        n = len(self.distances)
        circuits = [QCircuit()]*n
        for i in range(n):
            for j in range(len(self.ansatz[i])):
                gate = self.__create_gate(self.ansatz[i][j])
                circuits[i] += self.__create_tq_gate(gate)
        self.circuits = circuits
        return circuits

    def __create_gate(self, gate: str) -> Gate:
        name = gate.split('(', 1)[0]

        # Get target values
        target_values = gate.split('target=(', 1)[1].split(')')[0]
        parts = target_values.split(',')
        # If last element is not int but ''
        if not parts[-1]:
            parts = parts[:-1]
        target = [int(n) for n in parts]

        # Get control values if available
        control = None
        if 'control' in gate:
            control_values = gate.split('control=(', 1)[1].split(')')[0]
            parts = control_values.split(',')
            if not parts[-1]:
                parts = parts[:-1]
            control = [int(n) for n in parts]

        # Get parameter if available
        parameter = None
        if 'parameter' in gate:
            param_str = gate.split("parameter=", 1)[1].split(')')[0]
            try:
                parameter = float(param_str)
            except ValueError:
                parameter = param_str

        return Gate(name=name,
                    target=target,
                    control=control,
                    parameter=parameter)

    def __create_tq_gate(self, gate: Gate) -> QCircuit:
        if gate.name in ['X', 'Y', 'Z', 'H']:
            gate_method = getattr(tq.gates, gate.name)
            return gate_method(target=gate.target, control=gate.control) # noqa
        if gate.name in ['Rx', 'Ry', 'Rz']:
            gate_method = getattr(tq.gates, gate.name)
            return gate_method(gate.parameter, target=gate.target, control=gate.control) # noqa
        if gate.name in ['Phase']:
            return tq.gates.Phase(phi=gate.parameter, target=gate.target, control=gate.control) # noqa
        if gate.name in ['SWAP']:
            first, second = gate.target
            return tq.gates.SWAP(first=first, second=second, control=gate.control) # noqa
        raise ValueError(f'Gate of type {gate.name} is not supported.')

    def run_experiment(self):
        """
        Run experiment

        Returns
        ----------
        A list of tuples, (int, results)
            int - distance
            results - result object returned by tq.minimize
        """
        if self.circuits is None:
            self.build_circuits()
        return run(self)
