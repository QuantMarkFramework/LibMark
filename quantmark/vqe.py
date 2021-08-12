import tequila as tq


def run(exp):
    print('Running experiment...')
    print('Creating molecules...')
    molecules = [create_H2(d, exp.basis_set, exp.transformation) for d in exp.distances] # noqa

    results = []
    for i in range(len(exp.distances)):
        print(f'Running... {i+1}/{len(exp.distances)}')
        H = molecules[i].make_hamiltonian()
        U = exp.circuits[i]
        E = tq.ExpectationValue(H=H, U=U)
        variables = {k: 0.0 for k in U.extract_variables()}
        result = tq.minimize(objective=E, method=exp.optimizer, initial_values=variables, silent=True) # noqa
        results.append(result)
    print('Done')
    return list(zip(exp.distances, results))


def create_H2(R, basis_set, transformation):
    geometry = f'H 0.0 0.0 0.0\nH 0.0 0.0 {R}'
    return tq.chemistry.Molecule(geometry=geometry, basis_set=basis_set, transformation=transformation) # noqa
