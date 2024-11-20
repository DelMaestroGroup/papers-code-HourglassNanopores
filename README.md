[![Paper](https://img.shields.io/badge/paper-arXiv%3AXXXX.YYYYY-B31B1B.svg)](https://arxiv.org/abs/XXXX.YYYYY)
[![DOI](https://zenodo.org/badge/636411186.svg)](https://zenodo.org/doi/10.5281/zenodo.13832054)

# Friedel oscillations in one-dimensional <sup>4</sup>He

Bernd Rosenow and Adrian Del Maestro

[arXiv:XXXX.YYYYY](https://arxiv.org/abs/XXXX.YYYYY)

### Abstract
One-dimensional bosonic systems, such as helium confined to nanopores, exhibit Luttinger liquid behavior characterized by density waves as collective excitations. We investigate the impact of hourglass-shaped constrictions, found in real experimental nanopores, on a low dimensional quantum liquid.  We consider a microscopic model of <sup>4</sup>He inside a perturbed nanopore with a localized constriction, and employ quantum Monte Carlo simulations to analyze the density of the core within an effective low-energy framework. Our results reveal the emergence of Friedel oscillations in a bosonic quantum liquid without a Fermi surface. Furthermore, we utilize the Luttinger liquid model to predict experimentally observable signatures of this pinning phenomena in elastic scattering and via the temperature and pressure dependence of mass transport through the deformed nanopore.

### Description
This repository includes links, code, scripts, and data to generate the figures in a paper.

### Requirements
The data in this project was generated via quantum Monte Carlo simulations with the worm algorithm.

Raw simulation data set is available online at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13743089.svg)](https://doi.org/10.5281/zenodo.13743089).

1. A minimal environment to execute these notebooks can be installed via `pip install -r requirements.txt`
2. All quantum Monte Carlo data was generated with our [open source path integral software](https://code.delmaestro.org) also available on [github](https://github.com/delmaestrogroup/pimc)

### Support
This work was performed with support from the U.S. Department of Energy, Office of Science, Office of Basic Energy Sciences, under Award Number DE-SC0024333.

### Figures

#### Figure 01: Particle Density Inside the Pore
<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/pore_adsorption_details_dR_eq_4.0.svg" width="400px">

#### Figure 02: Hourglass Potential
<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/hourglass_potential.svg" width="400px">

#### Figure 03: Friedel Oscillations
<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/combined_fit_friedel_dR_eq_4.0_reversed_no_inset.svg" width="400px">

#### Figure 04: Luttinger Liquid Transport
<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/LL_transport.svg" width="400px">

#### Supplemental Figure 01: Potential Cuts

<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/hourglass_U.svg" width="400px">

#### Supplemental Figure 02: Estimators in the Core

<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/seed_distributions.svg" width="400px">

#### Supplemental Figure 02: Density inside the Core

<img src="https://github.com/DelMaestroGroup/papers-code-HourglassNanopores/blob/main/figures/rho_vs_x_seeds.svg" width="400px">
