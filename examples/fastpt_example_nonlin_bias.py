"""An example script to run FASTPT
Initializes and calculates all quantities supported by FASTPT
Makes a plot for P_22 + P_13
"""
from time import time

import numpy as np
import matplotlib.pyplot as plt

import fastpt as fpt
from fastpt import FASTPT

#Version check
print('This is FAST-PT version', fpt.__version__)

# load the data file

d=np.loadtxt('Pk_test.dat')
# declare k and the power spectrum
k=d[:,0]; P=d[:,1]

# set the parameters for the power spectrum window and
# Fourier coefficient window
#P_window=np.array([.2,.2])
C_window=.75
P_window=None
#document this better in the user manual

# padding length
n_pad=int(0.5*len(k))
to_do=['dd_bias']

# initialize the FASTPT class
# including extrapolation to higher and lower k
# time the operation
t1=time()
fastpt=FASTPT(k,to_do=to_do,low_extrap=-5,high_extrap=3,n_pad=n_pad)
t2=time()

# calculate 1loop SPT including bias terms
#P_spt=fastpt.one_loop_dd(P,C_window=C_window)

Growth = 1.0 #placeholder for Growth factor.


bias_fpt = fastpt.one_loop_dd_bias(P, P_window=P_window, C_window=C_window)
Pkz = Growth**2*P
Plinfpt = Growth**2*bias_fpt[1]
one_loopkz = Growth**4 * bias_fpt[0]
Pd1d2 = Growth**4 * bias_fpt[2]
Pd2d2 = Growth**4 * bias_fpt[3]
Pd1s2 = Growth**4 * bias_fpt[4]
Pd2s2 = Growth**4 * bias_fpt[5]
Ps2s2 = Growth**4 * bias_fpt[6]
#sigma^4 factor required to remove constant low-k contribution
sig4kz = Growth**4 * bias_fpt[7] * np.ones_like(bias_fpt[0])
#sig4=fastpt.sig4(P, P_window=P_window, C_window=C_window) #standalone function for sig4

t3=time()
print('initialization time for', to_do, "%10.3f" %(t2-t1), 's')
print('one_loop_dd recurring time', "%10.3f" %(t3-t2), 's')

# somewhat representative bias values
b1 = 2.0
b2 = 0.9*(b1-1)**2-0.5 #(this is a numerical fit to simulation data, but a relationship of this form is motivated in the spherical collapse picture
bs = (-4./7)*(b1-1)

Pggsub = (b1 ** 2 * (Pkz+one_loopkz) + b1 * b2 * Pd1d2 + (1. / 4) * b2 * b2 * (Pd2d2 - 2. * sig4kz) + b1 * bs * Pd1s2 +
                  (1. / 2) * b2 * bs * (Pd2s2 - 4. / 3 * sig4kz) + (1. / 4) * bs * bs * (Ps2s2 - 8. / 9 * sig4kz))

Pgg = (b1 ** 2 * (Pkz+one_loopkz) + b1 * b2 * Pd1d2 + (1. / 4) * b2 * b2 * (Pd2d2) + b1 * bs * Pd1s2 +
               (1. / 2) * b2 * bs * (Pd2s2) + (1. / 4) * bs * bs * (Ps2s2))

Pmg = b1 * (Pkz+one_loopkz) + (1. / 2) * b2 * Pd1d2 + (1. / 2) * bs * Pd1s2

# make a plot of 1loop SPT results

ax=plt.subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(r'$P(k)$', size=30)
ax.set_xlabel(r'$k$', size=30)

ax.plot(k,P,label='linear')
ax.plot(k,one_loopkz, label=r'$P_{22}(k) + P_{13}(k)$' )
ax.plot(k,Pggsub,label='gg')
ax.plot(k,Pmg,label='mg')

plt.legend(loc=3)
plt.grid()
plt.show()
