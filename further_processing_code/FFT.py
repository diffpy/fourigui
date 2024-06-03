import numpy as np
import h5py


def fourier_transformation(fftholder):
    data_size = list(fftholder.shape)
    fftholder = np.nan_to_num(fftholder)
    fftholder = np.fft.ifftshift(fftholder)
    fftholder = np.fft.fftn(fftholder, s=data_size, norm="ortho")
    fftholder = np.fft.fftshift(fftholder)
    fftholder = fftholder.real
    return fftholder


f = h5py.File("../../../columbia/reconstruction/reconstruction_cuir2s4.h5")
data = np.array(f["data"])
f.close()

data_fft = fourier_transformation(data)
