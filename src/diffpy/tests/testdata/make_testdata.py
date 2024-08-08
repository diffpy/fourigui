import h5py
import numpy as np


def cutcube(fname_uncut_cube, fname_cut_cube, qmin, qmax):

    cube = h5py.File(fname_uncut_cube, "r")["data"]

    X, Y, Z = cube.shape
    sphere = np.ones((X, Y, Z))
    r2_inner = qmin**2
    r2_outer = qmax**2
    XS, YS, ZS = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z))
    R2 = (XS - X // 2) ** 2 + (YS - Y // 2) ** 2 + (ZS - Z // 2) ** 2
    mask = (R2 <= r2_inner) | (R2 >= r2_outer)
    sphere[mask] = np.nan

    f = h5py.File(fname_cut_cube, "w")
    f.create_dataset("data", data=cube * sphere)
    f.close()


def fftcube(fname_reci, fname_real):

    fftholder = h5py.File(fname_reci, "r")["data"]

    fftholder = np.nan_to_num(fftholder)
    size = list(fftholder.shape)
    fftholder = np.fft.ifftshift(fftholder)
    fftholder = np.fft.fftn(fftholder, s=size, norm="ortho")
    fftholder = np.fft.fftshift(fftholder)
    fftholder = fftholder.real

    f = h5py.File(fname_real, "w")
    f.create_dataset("data", data=fftholder)
    f.close()


def dummydata(fname="dummydata.h5"):
    dummydata = np.ones((3, 3, 3))

    f = h5py.File(fname, "w")
    f.create_dataset("data", data=dummydata)
    f.close()


# cutcube("sofq.h5", "sofq_cut_10to40px.h5", 10, 40)
# cutcube("sofq.h5", "sofq_cut_15to35px.h5", 15, 35)
# fftcube("sofq.h5", "gofr.h5")
# fftcube("sofq_cut_10to40px.h5", "gofr_from_sofq_cut_10to40px.h5")
# fftcube("sofq_cut_15to35px.h5", "gofr_from_sofq_cut_15to35px.h5")
dummydata()
