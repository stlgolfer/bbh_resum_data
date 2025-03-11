from compas_python_utils.cosmic_integration.ClassCOMPAS import COMPASData

data_path = '/home/amigala/projects/bbh_resum/run/COMPAS_1000_0/COMPAS_Output/COMPAS_Output.h5'

dcos = COMPASData(data_path)  # you can also pass a list of keys here to slice the data (i.e. only systems between Mlower, Mupper)

# If you are using stroopwafel, you will need to set the name of the weights column for your COMPAS output
# (The data I'm loading here was not produced with stroopwafel so I'm not setting anything)
# DCOs.set_sw_weights('mixture_weights')

# Set the mask
# dcos.setCOMPASData()
dcos.setCOMPASDCOmask(types='BBH', withinHubbleTime=True, pessimistic=True)  # set the mask to only include DCOs of type BBH, within the Hubble time, and with pessimistic metallicity

dcos.setCOMPASData()
print(dcos.DCOmask)
print(dcos.seedsDCO)
  # this must be called to properly access the data using the COMPASData class after setting the mask
print(dcos)