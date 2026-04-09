# hourglass nanopores analysis helper utilities

import os
import subprocess, sys
import numpy as np
import json
from dgutils import colors as colortools
from scipy.interpolate import Akima1DInterpolator
import math


grey = '#4B4B4B'

# -------------------------------------------------------------------------------------------------------------------
def get_path(cmd, hint=''):
    """Get the path to a needed executable. """
    try:
        my_env = os.environ.copy()
        my_env["PATH"] = f"{sys.exec_prefix}/bin:{my_env['PATH']}"
        return os.path.dirname(subprocess.check_output(['which', cmd], env=my_env).decode('ascii').strip())
    except subprocess.CalledProcessError:
        return input(f"Enter path to `{cmd}` executables ({hint}): ")

# -------------------------------------------------------------------------------------------------------------------
def lab(_ΔR):
    """Dictionary key generator. """
    return f'dR_eq_{_ΔR:3.1f}'

# -------------------------------------------------------------------------------------------------------------------
def Tlab(_ΔR,_T):
    """Dictionary key generator. """
    return f"δR = {_ΔR:3.1f}, T = {_T:3.1f}"

# -------------------------------------------------------------------------------------------------------------------
def leg_lab(_ΔR):
    """Return a legend label."""
    return f"$\\delta R = {_ΔR}\\; \\mathrm{{\\AA}}$"

# -------------------------------------------------------------------------------------------------------------------
def base_dir(_ΔR,cylinder=True, raw=False, R=12.0):
    """Generate various directory where data is stored/loaded from.
    
    Our default radius is 12.0 Å
    """
    if raw:
        base = f'{raw_data_dir}/R_eq_{R:04.1f}/w_eq_3.0/{lab(_ΔR)}/OUTPUT/MERGED'
    else:
        base = f'{data_dir}/R_eq_{R:04.1f}/{lab(_ΔR)}'
        
    if cylinder:
        base += '/CYLINDER'
    return base

# -------------------------------------------------------------------------------------------------------------------
def shifted_ave(y,Δy,ȳ,Δȳ):
    """The error in a shifted mean from https://en.wikipedia.org/wiki/Propagation_of_uncertainty"""

    f = y/ȳ - 1.0
    
    # First we compute the error in the numerator y-ȳ
    num = y-ȳ
    Δnum = np.sqrt(Δy**2 + Δȳ**2)

    # now we compute the error in (y-ȳ)/ȳ
    Δf = np.abs(f)*np.sqrt((Δnum/num)**2 + (Δȳ/ȳ)**2) 
    
    return f, Δf

# -------------------------------------------------------------------------------------------------------------------
def plot_ρ_1d(_ax,_x,_ρ,_Δρ,idxs,cΔR,_col,label='_nolegend_', line=True, shift=False, ave_ρ=0.0, Δave_ρ=0.0,alpha='80', interp=False):

    plot_params = PlotParams(color=_col,alpha=alpha)
    
    if shift:
        _ρ,_Δρ = shifted_ave(_ρ,_Δρ,ave_ρ, Δave_ρ)
    
    if line:
        if interp:
            __x = np.linspace(np.min(_x[idxs]),np.max(_x[idxs]),5000)
            __y = Akima1DInterpolator(_x[idxs],_ρ[idxs])(__x)
        else:
            __x,__y = _x[idxs],_ρ[idxs]
            
        _ax.plot(__x,__y, lw=plot_params.get()['linewidth'], color=_col, ls=':')
    
    _ax.errorbar(_x[idxs],_ρ[idxs],yerr=_Δρ[idxs], **plot_params.get(), label=label)
    return _ax

# -------------------------------------------------------------------------------------------------------------------
class PlotParams:
    ''' A helper class that holds all plot parameters. '''
    
    def __init__(self,color=grey, eb=True, alpha='80'):

        alpha_f = int(alpha,16)/255.0
        self.params = {'marker':'o', 'linewidth':0.25, 'color':color, 
              'markerfacecolor':colortools.get_alpha_hex(color,alpha_f)+alpha, 'markersize':3, 
              'markeredgecolor':color, 'linestyle':':', 'markeredgewidth':0.5}
        if eb:
            self.params['ecolor'] = color
            self.params['elinewidth'] = 0.5
            self.params['linestyle'] = 'None'
            self.params['barsabove'] = True

    def get(self):
        return self.params

# -------------------------------------------------------------------------------------------------------------------
def plot_single_ρ(ax,_x,_ρ,_Δρ,msk,cΔR,_col, shift=False, ave_ρ=0.0, plot0=False, xaxis=True, Δave_ρ=0.0, line=True, label=None, interp=False):

    if label is None:
        label=leg_lab(cΔR)
        
    # central portion 
    plot_ρ_1d(ax,_x,_ρ,_Δρ,range(msk[0],msk[-1]+1),cΔR,colortools.get_alpha_hex(_col,0.2),
              shift=shift,ave_ρ=ave_ρ, Δave_ρ=Δave_ρ, line=line, interp=interp)
        
    # x < -x_cut
    if msk[0] < int(len(_x)/2):
        plot_ρ_1d(ax,_x,_ρ,_Δρ,range(msk[0]),cΔR,_col,shift=shift,ave_ρ=ave_ρ, Δave_ρ=Δave_ρ, line=line, interp=interp)
        
    # x > -x_cut
    plot_ρ_1d(ax,_x,_ρ,_Δρ,range(msk[-1],len(_x)),cΔR,_col, label=label,shift=shift,ave_ρ=ave_ρ, 
              Δave_ρ=Δave_ρ, line=line, interp=interp)
    
    ax.legend(loc='upper right', borderpad=0)
    
    if shift:
        ax.set_ylabel(r'$\langle \delta \rho(x) \rangle / \rho_0$');
        
    else:    
        ax.set_ylabel(r'$\langle \rho(x) \rangle \; (\rm \AA^{-1})$');
     
    if xaxis:
        ax.set_xlabel(r'$x\; (\rm \AA)$');
    else:
        ax.xaxis.set_ticklabels([])
        ax.set_xlabel('');
    
    return ax

# -------------------------------------------------------------------------------------------------------------------
def format_value_stderr(value, error):
    """
    Format value ± error as value(error), with the uncertainty
    shown in the last digit(s) of the value.

    Example:
        0.05914372 ± 0.00404  ->  "0.059(4)"
    """
    if error <= 0 or not math.isfinite(error):
        raise ValueError("Uncertainty must be positive and finite.")

    # Order of magnitude of the uncertainty
    exponent = math.floor(math.log10(error))

    # Round uncertainty to 1 significant digit
    error_rounded = round(error, -exponent)

    # Determine decimal places needed
    decimals = max(0, -exponent)

    # Round value to same precision
    value_rounded = round(value, decimals)

    # Integer uncertainty shown in parentheses
    uncertainty_int = int(round(error_rounded * 10**decimals))

    fmt = f"{{:.{decimals}f}}"
    return f"{fmt.format(value_rounded)}({uncertainty_int})"

# we load relavent local path information from a file if it exists, if not, we query the user
# -------------------------------------------------------------------------------------------------------------------
try:
    with open('../include/local.json', 'r') as f:
        local = json.load(f)
        pimc_bin_path = local['pimc_bin_path']
        data_dir = local['data_dir']
        gnu_parallel = local['gnu_parallel']
        raw_data_dir = local['raw_data_dir']

except:
    pimc_bin_path = get_path('merge.py',hint='(see e.g. https://github.com/DelMaestroGroup/pimcscripts)')
    gnu_parallel = get_path('parallel', hint='(e.g. ~/local/bin/parallel): ')
    data_dir = input(r"Enter path to merged QMC Data (enter for default ../data): ") or '../data'
    raw_data_dir = input(r"Enter path to raw QMC data (enter for default ../data/qmc: ") or '../data/qmc'
    
    local = {'pimc_bin_path':pimc_bin_path, 'data_dir':data_dir, 'gnu_parallel':gnu_parallel, 
            'raw_data_dir':raw_data_dir}

    # Make sure we strip any extraneous path separators
    for path_name, path in local.items():
        if path.endswith(os.sep):
            local[path_name] = path[:-1]
            
    with open('../include/local.json', 'w') as f:
        json.dump(local, f, ensure_ascii=True, indent=4)
