#python libraries
import os, sys
import numpy as np               # for handling arrays
import h5py as h5                # for reading the COMPAS data
import time                      # for finding computation time
import matplotlib.pyplot as plt  #for plotting
import warnings
from compas_python_utils.cosmic_integration.ClassCOMPAS import COMPASData

# Import COMPAS specific scripts
# compasRootDir = os.environ['COMPAS_ROOT_DIR']
# sys.path.append(compasRootDir + 'postProcessing/PythonScripts')
# from compas_python_utils import printCompasDetails, getEventHistory, getEventStrings

# Choose an output hdf5 file to work with
def process_to_h5(pathToData, theta, theta_headers, outfile='test.h5', reload=False):
# pathToData = './COMPAS_Output_8/COMPAS_Output.h5'
    if len(theta) == 0:
        warnings.warn("EMPTY theta. Did you mean to do that?")
    Data = h5.File(pathToData)
    print(np.array(list(Data.keys())).dtype)
    print(Data['BSE_System_Parameters']['SEED'])
    print(len(Data['BSE_System_Parameters']['SEED']))

    phis = np.zeros((len(Data['BSE_System_Parameters'].keys()), len(Data['BSE_System_Parameters']['SEED'])))
    targets = np.zeros(len(Data['BSE_System_Parameters']['SEED']))
    bbh_targets = np.zeros(len(Data['BSE_System_Parameters']['SEED']))
    # print(phis.shape)
    keys = Data['BSE_System_Parameters'].keys()
    # there is a key in BSE_Double_Compact_Objects called hubble time
    # that can make it more strict. if it is in a hubble time, we can 
    # say that it would be observable
    print(keys)
    seed_index = np.where(np.array(list(keys)) == "SEED")[0][0]
    # print(seed_index)
    for row, key in enumerate(keys):
        # print(key)
        # print(Data['BSE_System_Parameters'][key][:])
        phis[row] = Data['BSE_System_Parameters'][key][:]
    # extract seeds of all systems from phis
    seeds = phis[seed_index]
    if 'BSE_Double_Compact_Objects' in Data:
        print(f'Expected number of dcos {len(set(Data['BSE_Double_Compact_Objects']['SEED']))}')
        dco_seeds = set(Data['BSE_Double_Compact_Objects']['SEED'])
        for i in range(len(targets)):
            targets[i] = 1 if seeds[i] in dco_seeds else 0
        print(f'Inferrred number of dcos: {np.sum(targets)}')
        assert int(len(set(Data['BSE_Double_Compact_Objects']['SEED']))) == int(np.sum(targets)), "Expected number of DCOs from simulation did not equal inferred number"
    else:
        print('No DCOs formed')
        for i in range(len(targets)):
            targets[i] = 0
    # need to put extra flag on DCO for the various things inside there. it's not just dco
    # we want the bbh which is slightly more rigorously defined

    bbhs = COMPASData(pathToData)
    bbhs.setCOMPASDCOmask(types='BBH', withinHubbleTime=True, pessimistic=True)
    bbh_failure = False
    try:
        bbhs.setCOMPASData()
        bbh_seeds = set(bbhs.seedsDCO)
        # similar to before, iterate through every seed in the table and see if that seed is a bbh
        for i in range(len(bbh_targets)):
            bbh_targets[i] = 1 if seeds[i] in bbh_seeds else 0
        print(f'Found {np.sum(bbh_targets)} bbhs')
        assert int(np.sum(bbh_targets)) <= int(np.sum(targets)), "BBH targets should be less than total DCOs..."
    except Exception:
        # there is an issue with the backend code for masking. if there is only 1 seed that fits the mask, it will fail
        # since we can't really fix this issue, we will skip writing such files
        # raise NotImplementedError("Backend error with BBHs masking")
        warnings.warn("BBH backend issue, will not write this file")
        bbh_failure = True

    if not bbh_failure:
        # write data to new h5 file
        with h5.File(outfile, "w") as file:
            phi_keys = np.array(list(keys)).astype('S26')
            print(phi_keys.dtype)
            phi_labels = file.create_dataset('phi_labels', phi_keys.shape, data=phi_keys)
            Data.close()
            file.create_dataset('phi', phis.T.shape, data=phis.T)
            # stack target columns
            all_targets = np.vstack((targets, bbh_targets)).T
            file.create_dataset('target', all_targets.shape, data=all_targets)
            target_headers = np.array(["DCOs","BBH Events"])
            file.create_dataset('target_headers', target_headers.shape, data=target_headers.astype('S26'))
            file.create_dataset('theta', theta.shape, data=theta)
            file.create_dataset('theta_headers', theta_headers.shape, data=theta_headers.astype('S26'))
            # want a header that says "target" that is a column vector
            # then another column that has rows that are the values of that target
            # want some phis to be in separate column that are labeled as "phi fixed"
            # since they may not actually be set to vary
        # reload new dataset to view
        if reload:
            reloaded_data = h5.File(outfile)
            print('---h5 file reload---')
            print(reloaded_data.keys())
            print(reloaded_data['phi'])
            print(reloaded_data['phi_labels'][1])
            print(reloaded_data['theta'][0])
            print(f'Target: {reloaded_data['target'].shape}')
            for theta_name in reloaded_data['target_headers']:
                print(theta_name)
            # print(reloaded_data['formed_bh']) # modify this to have an explicit label
            reloaded_data.close()
        return outfile
    else:
        return ""

if __name__ == '__main__':
    process_to_h5('/home/amigala/projects/bbh_resum/run/COMPAS_1000_0/COMPAS_Output/COMPAS_Output.h5', np.array([0]), np.array(['test']), reload=True)


# so, let's first make a script that contains a function that loads a compas file
# this is since we will ahve anotehr script that generates the theta information when we run the simulation
# we want this function to return an h5 file since this could be very larget to traverse
# def process(filename, theta, theta_headers, out_name="processed.h5"):
#     # theta is the data, where columns are labeled by theta_headers

#     # iterate over all the keys
#     Data = h5.file(filename)
#     with h5.File(out_name, "w") as file:
#         theta_dataset = file.create_dataset('theta', theta)
#         theta_dataset.attrs['headers'] = theta_headers
#     #
#     Data.close()