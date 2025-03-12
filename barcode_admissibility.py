"""
(I) pModule is a dictionary where keys are d-dimensional tuples representing indices (grades) 
    z = (z_1, z_2, ... , z_d) and values are lists containing the identity matrix of dimension dim(M_z) and a list of linear transformations M_z -> M_{z + (1, 0, 0 ..., 0)},
                                   M_z -> M_{z + (0, 1, 0, .., 0)},
                                   .
                                   .
                                   M_z -> M_{z + (0, 0, ..., 0, 1)}.

              z : [an identity matrix of dimension M_z, [ M_{z, z+ e_i} for i in range(d)]]
(II) This algotihms works for pmodules whose generators are in M_O. This condition is satisfies if
                                   rank(M_z) <= rank(M_{o,z}).            (*)
    Provided rank(M_z) > rank(M_{o,z}), it returns an error indicating that a major condition is not satisfied
    hence, it is unable to determine barcode admissibility of the module. 

(III) In the case of decomposability verified with `is_barcode_admissible`, the last function    `barcode_collector` returns a dictionary 
              `i : an array of all indices z for which the generator e_i survives up to M_z`
 where `i=1, 2, ..., r`, `r = dim(M_O)`. 

(IV) There is another algotihms to detect barcode admissibility of a pmodule regardless of the condition (*).
"""

import numpy as np
import sys

# moduleMaps() creates a dictionary whose keys are d-dimensional indices and the values are matrices M_{O, z}

def pModuleMaps(p_Module):
    maps_dictionary = {}
    index_list = []
    keys = p_Module.keys()
    first_key = next(iter(p_Module))
    d = len(first_key)
    
    for key in keys:
        next_key = first_key
        matrix = p_Module[next_key][0]
        for coord in range(d):
            for i in range(key[coord]):
                next_key = next_key[:coord] + (i,) + next_key[coord + 1:]
                next_matrix = p_Module[next_key][1][coord]
                matrix = np.matmul(next_matrix, matrix)
                index_list.append(matrix)
            next_key = next_key[:coord] + (key[coord],) + next_key[coord + 1:]
        maps_dictionary.update({key : matrix})
            
    return maps_dictionary


# is_barcode_admissible() creates a set P of row vectors of all matrices M_{O,z} 
# pmodule is barcode admissible if and only if P is a set of linearly independent vectors.

def is_barcode_admissible(p_Module):
    maps = pModuleMaps(p_Module)
    d = len(next(iter(p_Module)))
    all_row_vectors = []

    for key in maps.keys():
        matrix_rank = np.linalg.matrix_rank(maps[key])
        dim_key = np.linalg.matrix_rank(p_Module[key][0])
        
        # Check if the condition (*) holds, i.e., rank(M_z) <= rank(M_{o,z}) 
        if dim_key > matrix_rank:
            print(f'Error: Rank of p_Module[{key}][0] is strictly greater than matrix rank.')
            sys.exit()

        if matrix_rank == dim_key:
            if matrix_rank != d:
                for i in range(len(maps[key])):
                    vector = maps[key][i]
                    if np.any(vector != 0) and not any(np.array_equal(vector, v) for v in all_row_vectors):
                        all_row_vectors.append(vector)

    if len(all_row_vectors) == 0:
        print('The module is not barcode admissible due to lack of non-zero row vectors.')
    else:
        rank = np.linalg.matrix_rank(all_row_vectors)
        if len(all_row_vectors) == rank:
            print('The module is barcode admissible.')
            print(f'P_S: {all_row_vectors}')
        else:
            print('The module is not barcode admissible.')
            print(f'P_S: {all_row_vectors}')


def barcodes(pModule, d):
    barcode_indices = {}
    indices = np.array(list(pModule.keys()))
    maps = pModuleMaps(pModule)
    dimension = len(pModule[tuple(np.zeros(d))][0])
    for i in range(dimension):
        barcode_indices[i] = []
        for z in indices:
            map = maps[tuple(z)]
            if np.any(map[:, i] != 0):
              barcode_indices[i].append(z)            
    return barcode_indices



# Example 0
p_Module = {}
p_Module.update({(0, 0): [np.eye(3,3), [np.eye(3, 3), np.eye(3, 3)]]})
p_Module.update({(1, 0): [np.eye(3,3), [np.eye(1,3), np.array([[1, 0, 0], [0, 0, 1]])]]})
p_Module.update({(2, 0): [np.eye(1,1), [np.zeros((1,1)), np.eye(1,1)]]})
p_Module.update({(0, 1): [np.eye(3,3), [np.array([[1, 0, 0], [0, 0, 1]]), np.array([[1, 0, 0], [0, 0, 1]])]]})
p_Module.update({(0, 2): [np.eye(2,2), [np.array([[0, 1]]), np.zeros((1,2))]]})
p_Module.update({(1, 1): [np.eye(2,2), [np.array([[1, 0]]), np.array([[0, 1]])]]})
p_Module.update({(1, 2): [np.eye(1,1), [np.zeros((1,1)), np.zeros((1,1))]]})
p_Module.update({(2, 2): [np.zeros((1,1)), [np.zeros((1,1)), np.zeros((1,1))]]})
p_Module.update({(2, 1): [np.eye(1,1), [np.zeros((1,1)), np.zeros((1,1))]]})

is_barcode_admissible(p_Module)
print(barcodes(p_Module, 2))
