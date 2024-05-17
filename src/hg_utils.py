# hourglass nanopores analysis helper utilities

import os

pimc_bin_path = os.environ['HOME'] + '/.conda/envs/pimc/bin'
data_dir = '/lustre/isaac/scratch/agdelma/Projects/HourGlass/w_eq_3.0'
gp = os.environ['HOME'] + '/local/bin/parallel'

def lab(_ΔR):
    return f'dR_eq_{_ΔR:3.1f}'

def base_dir(_ΔR,cylinder=True):
    base = f'{data_dir}/{lab(_ΔR)}/OUTPUT/MERGED'
    if cylinder:
        base += '/CYLINDER'
    return base

def repo_dir(_ΔR,cylinder=True):
    base = f'../data/{lab(_ΔR)}'
    if cylinder:
        base += '/CYLINDER'
    return base