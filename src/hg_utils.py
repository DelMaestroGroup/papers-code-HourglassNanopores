# hourglass nanopores analysis helper utilities

import os
import numpy as np
import json

#pimc_bin_path = os.environ['HOME'] + '/.conda/envs/pimc/bin'
#data_dir = '/lustre/isaac/scratch/agdelma/Projects/HourGlass/w_eq_3.0'
#gp = os.environ['HOME'] + '/local/bin/parallel'

def lab(_ΔR):
    return f'dR_eq_{_ΔR:3.1f}'

def base_dir(_ΔR,cylinder=True, raw=True):
    base = f'{data_dir}/{lab(_ΔR)}'
    if raw:
        base += '/OUTPUT/MERGED'
    if cylinder:
        base += '/CYLINDER'
    return base

def repo_dir(_ΔR,cylinder=True):
    base = f'../data/{lab(_ΔR)}'
    if cylinder:
        base += '/CYLINDER'
    return base

def shifted_ave(y,Δy,ȳ,Δȳ):
    """The error in a shifted mean from https://en.wikipedia.org/wiki/Propagation_of_uncertainty"""

    f = y/ȳ - 1.0
    
    # First we compute the error in the numerator y-ȳ
    num = y-ȳ
    Δnum = np.sqrt(Δy**2 + Δȳ**2)

    # now we computer the error in (y-ȳ)/ȳ
    Δf = np.abs(f)*np.sqrt((Δnum/num)**2 + (Δȳ/ȳ)**2) 
    
    return f, Δf

# we load relavent local path information from a file if it exists, if not, we query the user

try:
    with open('../include/local.json', 'r') as f:
        local = json.load(f)
        pimc_bin_path = local['pimc_bin_path']
        data_dir = local['data_dir']
        gnu_parallel = local['gnu_parallel']

except:
    pimc_bin_path = input("Enter path to `pimcscripts` executables (see e.g. https://github.com/DelMaestroGroup/pimcscripts): ")
    data_dir = input("Enter path to merged QMC Data (e.g. '../data'): ")
    gnu_parallel = input("Enter path to gnu parallel (e.g. '/local/bin/parallel'): ")

    local = {'pimc_bin_path':pimc_bin_path, 'data_dir':data_dir, 'gnu_parallel':gnu_parallel}
    
    with open('../include/local.json', 'w') as f:
        json.dump(local, f, ensure_ascii=True, indent=4)
