#symmetrization code
#
#contact: Sani Harouna-Mayer
#mail: sani.harouna-mayer@uni-hamburg.de
#
#
#this code is derived for a 111 fiber textured fcc structure 3D scattering volume and needs to adapted for
#different texture geometries and different structures
#
#for different fiber texture orientations one can easily change the orientation in line 55 and 73
#for different cubic structures one can easily change the symmetry operation parameters in line 106
#more complex textures or crystal strucutes require more effort to derive appropriate symmetry operations

import numpy as np
import h5py
from scipy.ndimage import rotate
from time import time


def load_data(fname):
    """Load data from fname in h5 datatype"""
    f = h5py.File(fname, 'r')
    data = np.array(f['data'])
    f.close()
    print("loaded: " + fname)
    return data


def save_data(fname, arr):
    """Save data arr as fname in h5 datatype"""
    f = h5py.File(fname, 'w')
    f['data'] = arr
    f.close()
    print("saved: " + fname)
    return


def symm_op(arr, angle, inversion):
    """
    Perform symmetry operations on data set "arr". arr will be inverted about the center voxel and rotated with "angle"
    about the z axis by iterating the 2D planes in the 3D data set arr along the z axis. rotation of the planes in the
    data set is perfomed by scipy.ndimage.rotate. arr might contain nan values which scipy.ndimage.rotate cannot
    operate. therefore the nan values in arr will be converted to float values 0.0 and denoted by 3D array "isnanarr_so".
    :param arr: data set in h5 type
    :param angle: rotate arr angle degrees about the z axis. put False if no rotation is intended.
    :param inversion: Boolian variable if arr is supposed to be inverted about center voxel.
    :return: symmetry operated data set in h5 arr_so and isnanarr_so to denote nan values in previous data set
    for later binning
    """

    if inversion:
        arr = np.flip(arr) #inverts array arr about the center voxel

    if angle:
        arr = np.rot90(arr, k=1, axes=(0, 2)) #rotate arr 90° about axes (0,2) to easily perform rotation about z below

        isnanarr_so = []
        arr_so = []
        isnanarr = np.isnan(arr)
        arr = np.nan_to_num(arr) #scipy.ndimage.rotate cannot operate nan values, thus reasign nan to 0.0

        for plane in isnanarr:
            isnanarr_so.append(
                rotate(plane, angle, axes=(1, 0), reshape=False, mode='constant', cval=True, prefilter=True, order=0)
            )

        for plane in arr:
            arr_so.append(
                rotate(plane, angle, axes=(1, 0), reshape=False, mode='constant', cval=0.0, prefilter=True, order=0)
            )

        isnanarr_so = np.rot90(isnanarr_so, k=-1, axes=(0, 2))
        arr_so = np.rot90(arr_so, k=-1, axes=(0, 2)) #rotate arr -90° about axes (0,2) to initial orientation

    else:
        isnanarr_so = np.isnan(arr)
        arr_so = np.nan_to_num(arr)

    return arr_so, np.invert(isnanarr_so)


def main(arr, symm_op_params):
    """
    Perform symmertry operations specified in symm_op_params and bin together the symmetry operated data sets.
    :param arr: data set in h5 type
    :param symm_op_params: list of tuples with the supposed angle for the rotation in degree and False if no rotation
    is intended and True or False if data set should be inverted or not.
    :return arr: average of all symmetry operated data sets
    """
    holder = np.zeros_like(arr)
    bin = np.zeros_like(arr)
    time0 = time()
    for symm_op_param in symm_op_params:
        arr_so, isnanarr_so = symm_op(arr, *symm_op_param)
        holder += arr_so
        bin += isnanarr_so
        print(round(time()-time0, 2), symm_op_param)
    bin = bin.astype('float')
    bin[bin == 0.0] = 'nan'
    arr = np.array(holder) / np.array(bin)
    print(round(time() - time0, 2))
    return arr


if __name__ == '__main__':
    symm_op_params = [(False, False), #1
                      (120, False), #C3
                      (240, False), #2C3
                      (False, True), #i
                      (120, True), #i + C3
                      (240, True)] #i + 2C3
    cube = load_data('/path2data/data.h5')
    cube = main(cube, symm_op_params)
    save_data('/path2data/data_sa.h5', cube)
