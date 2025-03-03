# Barcode-Admissible-MPM
# pModule Barcode Admissibility Checker
# barcodes collector

This project provides algorithms to handle pModules, focusing on verifying barcode admissibility.

## Copyright

Copyright (c) 2024 Mehdi Nategh  
This code is licensed under the MIT License. See the LICENSE file for details.

## Overview

### pModule
- `pModule` is a dictionary where keys are d-dimensional tuples representing indices (grades) `z = (z_1, z_2, ..., z_d)`. 
- Values are lists containing:
  - The identity matrix of dimension `dim(M_z)`.
  - A list of linear transformations:
    - `M_z -> M_{z + (1, 0, 0, ..., 0)}`
    - `M_z -> M_{z + (0, 1, 0, ..., 0)}`
    - ...
    - `M_z -> M_{z + (0, 0, ..., 0, 1)}`

### Functionality
1. **Mapping Generation**: The function `pModuleMaps()` creates a dictionary where keys are d-dimensional indices and values are matrices `M_{O, z}`.
2. **Barcode Admissibility Check**: The function `is_barcode_admissible()` checks whether a pModule is barcode admissible based on the linear independence of row vectors.
3. **Barcodes Collector**: The function `barcodes` generators a dictionary with keys ranging over `1, 2, .., r` where `r = dim(M_O)` and the values are sets of indices `z` 
                           such that the `i`-th generator survives up to `M_z`, provided the decomposability of   M` is verified by `is_barcode_admissible` function.

### Conditions
- The algorithms work for pModules whose generators are in `M_O`, satisfying the condition:
  - `rank(M_z) <= rank(M_{o,z})`
- If `rank(M_z) > rank(M_{o,z})`, an error is returned indicating that a major condition is not satisfied, preventing determination of barcode admissibility.

## Installation

To use the code, ensure you have Python and NumPy installed. You can install NumPy using pip:

pip install numpy
