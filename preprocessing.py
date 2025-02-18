#python libraries
import os, sys
import numpy as np               # for handling arrays
import h5py as h5                # for reading the COMPAS data
import time                      # for finding computation time
import matplotlib.pyplot as plt  #for plotting
import warnings

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

    # write data to new h5 file
    with h5.File(outfile, "w") as file:
        phi_keys = np.array(list(keys)).astype('S26')
        print(phi_keys.dtype)
        phi_labels = file.create_dataset('phi_labels', phi_keys.shape, data=phi_keys)
        Data.close()

        phi_dataset = file.create_dataset('phi', phis.T.shape, data=phis.T)
        target_dataset = file.create_dataset('target', targets.shape, data=targets)
        file.create_dataset('theta', theta.shape, data=theta)
        file.create_dataset('theta_headers', theta_headers.shape, data=theta_headers.astype('S26'))
    # reload new dataset to view
    if reload:
        reloaded_data = h5.File(outfile)
        print(reloaded_data.keys())
        print(reloaded_data['phi'])
        print(reloaded_data['phi_labels'][1])
        print(reloaded_data['theta'][0])
        reloaded_data.close()
    return outfile

if __name__ == '__main__':
    process_to_h5('./COMPAS_Output_12/COMPAS_Output.h5', reload=True)


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