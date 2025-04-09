from runner import run_COMPAS
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='bbh_resum CLI',
        description='Single runner for bbh_resum'
    )
    parser.add_argument(
        '--num_systems',
        help='Number of systems in the COMPAS simulation'
        )
    parser.add_argument(
        '--metallicity'
    )
    parser.add_argument(
        '--envelope_eff'
    )
    parser.add_argument(
        '--sigma_bh'
    )
    parser.add_argument(
        '--sigma_ns'
    )
    args = parser.parse_args()
    run_COMPAS(
        int(args.num_systems),
        float(args.metallicity),
        float(args.envelope_eff),
        float(args.sigma_bh),
        float(args.sigma_ns),
        simnumber=1
    )