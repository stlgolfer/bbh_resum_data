from preprocessing import process_to_h5
import numpy as np
import subprocess
from runner import run_COMPAS
import threading
import concurrent.futures
import argparse

NUM_SIMS = 5
NUM_SYSTEMS_HF = int(1e6)

def spawn_choice(num):
    metallicity = np.random.choice(np.linspace(0.0001,0.03, 1000))
    envelope_eff = np.random.choice(np.linspace(0, 100, 1000))
    sigma_bh = np.random.choice(np.linspace(30,1000, 1000))
    sigma_ns = np.random.choice(np.linspace(30,1000,1000))

    run_COMPAS(
        NUM_SYSTEMS_HF,
        metallicity=metallicity,
        envelope_eff=envelope_eff,
        sigma_bh=sigma_bh,
        sigma_ns=sigma_ns,
        simnumber=num
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='HF runner'
    )

    parser.add_argument(
        '--prefix',
        help='File prefix'
    )
    args = parser.parse_args()

    for sim in range(NUM_SIMS):
        metallicity = np.random.choice(np.linspace(0.0001,0.03, 1000))
        envelope_eff = np.random.choice(np.linspace(0, 100, 1000))
        sigma_bh = np.random.choice(np.linspace(30,1000, 1000))
        sigma_ns = np.random.choice(np.linspace(30,1000,1000))

        run_COMPAS(
            NUM_SYSTEMS_HF,
            metallicity,
            envelope_eff,
            sigma_bh,
            sigma_ns,
            sim,
            file_prefix=args.prefix
        )