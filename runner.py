from preprocessing import process_to_h5
import numpy as np
import subprocess

NUM_SIMS = 1000
DEBUG = True
NUM_SYSTEMS_LF = 1000 # 1000 LF
NUM_SYSTEMS_HF =  2 if DEBUG else 1000*NUM_SYSTEMS_LF #1M
HF_RUNS = 4 # n high fidelities with some parameters
# n low fidelities with same parameters are HF

def run_COMPAS(systems, metallicity, envelope_eff,sigma_bh,sigma_ns, simnumber):
    run_name = f'./run/COMPAS_{systems}_{simnumber}'
    result = subprocess.run([
        'bash',
        'run_compas.sh',
        str(systems),
        str(int(5)),
        str(int(150)),
        str(metallicity),
        str(envelope_eff),
        run_name,
        str(sigma_bh),
        str(sigma_ns)
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
            metallicity,
            envelope_eff,
            sigma_bh,
            sigma_ns
        ]),
        theta_headers=np.array([
            'metallicity',
            'envelope_eff_alpha',
            'sigma_bh',
            'sigma_ns'
        ]),
        outfile=f'{run_name}_resum.h5',
        reload= True if sim==1 else False
    )

# in this script we want to be able to run a simulation
# get it's theta parameters (of interest)
# and pre process the simulation to an h5 file
if __name__ == '__main__':
    for sim in range(NUM_SIMS):
        # if DEBUG and sim >= HF_RUNS:
        #     break
        metallicity = np.random.choice(np.linspace(0.0001,0.03, 1000))
        envelope_eff = np.random.choice(np.linspace(0, 100, 1000))
        sigma_bh = np.random.choice(np.linspace(30,1000, 1000))
        sigma_ns = np.random.choice(np.linspace(30,1000,1000))

        if DEBUG:
            run_COMPAS(
                1000,
                metallicity,
                envelope_eff,
                sigma_bh,
                sigma_ns,
                sim
            )
            break

        if sim < HF_RUNS:
            run_COMPAS(
                NUM_SYSTEMS_HF,
                metallicity,
                envelope_eff,
                sigma_bh,
                sigma_ns,
                sim
            )
            run_COMPAS(
                NUM_SYSTEMS_LF,
                metallicity,
                envelope_eff,
                sigma_bh,
                sigma_ns,
                sim
            )
        else:
            run_COMPAS(
                NUM_SYSTEMS_LF,
                metallicity,
                envelope_eff,
                sigma_bh,
                sigma_ns,
                sim
            )
        # initial_mass1 = np.random.choice(
        #     np.linspace(0.1,150,1000)
        # )
        # initial_mass2 = np.random.choice(np.linspace(0.1,150,1000))
        # want to use and vary the parameters
        # --initial-mass-function [ -i ]
        # --initial-mass-max
        # --initial-mass-min
        # summarize phi labels
        
