from preprocessing import process_to_h5
import numpy as np
import subprocess

# in this script we want to be able to run a simulation
# get it's theta parameters (of interest)
# and pre process the simulation to an h5 file
if __name__ == '__main__':
    NUM_SIMS = 1
    NUM_SYSTEMS = 500

    for sim in range(NUM_SIMS):
        metallicity = np.random.choice(np.linspace(0.0001,0.03, 1000))
        envelope_eff = np.random.choice(np.linspace(0, 100, 1000))
        initial_mass1 = np.random.choice(
            np.linspace(8,150,1000)
        )
        initial_mass2 = np.random.choice(np.linspace(0.1,initial_mass1,1000))
        run_name = f'./run/COMPAS_{NUM_SIMS}_{sim}'
        result = subprocess.run([
            'bash',
            'run_compas.sh',
            str(NUM_SYSTEMS),
            str(initial_mass1),
            str(initial_mass2),
            str(metallicity),
            str(envelope_eff),
            run_name
            ],capture_output=True,text=True
        )
        with open(f'{run_name}_log.txt', 'w') as file:
            file.write(result.stdout)
            file.close()
        print(result.stdout)
        # now we need to post-process the data and inject theta
        process_to_h5(
            f'{run_name}/COMPAS_Output/COMPAS_Output.h5',
            theta=np.array([
                initial_mass1,
                initial_mass2,
                metallicity,
                envelope_eff
            ]),
            theta_headers=np.array([
                'initial_mass1',
                'initial_mass2',
                'metallicity',
                'envelope_eff_alpha'
            ]),
            outfile=f'{run_name}_resum.h5',
            reload= True if sim==1 else False
        )