import toolbox
import numpy as np
import su

#spherical divergence


#build wavelet
from toolbox import build_wavelet
low = 2. #hz
high = 60. #hz
wavelet = np.convolve(np.ones(3)/3., build_wavelet(low, high)[75:125], mode='same')

