import numpy as np
from numpy import loadtxt
from math import log10, floor
from scipy.linalg import svdvals
from tensorflow.linalg import svd
import matplotlib.pyplot as plt
from multiprocessing import Pool


def NeuralNetwork(dep, axx, mat_var, bias_var):
    
    mat_size = 1000

    Weight_array = [np.random.randn(mat_size,mat_size) for _ in range(dep)]

    for i in range(dep):
        Weight_array[i] *= mat_var


    Jacobi = np.identity(mat_size)

    vec = np.random.randn(mat_size)

    for i in range(dep):
        bias_vec = np.random.randn(mat_size) * bias_var
        h = Weight_array[i].dot(vec) + bias_vec
        for j in range(mat_size):
            vec[j] = h[j]
        Jacobi = np.matmul(Jacobi, Weight_array[i])

    sv = svd(Jacobi)[0]

    print(sv)
    sv_no_zeros = np.delete(sv, np.where(sv < 10**(-300)))
    print('Sv no zeros: ', sv_no_zeros)
    sv_min = sv_no_zeros[0]
    sv_len = np.shape(sv_no_zeros)[0]

    for i in range(sv_len):
        if sv_no_zeros[i] < sv_min:
            sv_min = sv_no_zeros[i]

    print('Sv min: ', sv_min)
    sv_max = max(sv)

    btm_bnd = floor(log10(sv_min))

    top_bnd = floor(log10(sv_max))
    print('btm: ', btm_bnd)
    print('top: ', top_bnd)

    # range(..., ...) can be changed
    count = [0 for i in range(abs(btm_bnd - top_bnd)+1)]

    for s in sv:
        if s>0:
            print('value: ', floor(log10(s)))
            count[floor(log10(s)) - btm_bnd] += 1

    #for i in range(21):
        #count[i] /= mat_size

    sv_hist = [floor(log10(sv_no_zeros[i])) for i in range(sv_len)]

    axx.hist(sv_hist, abs(btm_bnd - top_bnd) + 1, (btm_bnd, top_bnd), histtype = 'bar', rwidth = 0.9)

    #axx.plot([i for i in range(btm_bnd, top_bnd + 1)], count, '--')
    axx.set_xlabel('log_10(s)')
    axx.set_ylabel(f'$\sigma = {mat_var}$')
    axx.set_title(f'Depth {dep}')

if __name__ == "__main__":
    fig, axs = plt.subplots(2,2)

    fig.tight_layout(pad=3.0)

    data = loadtxt('linear_critical.csv', delimiter=',')

    data_len = np.shape(data)[0]

    sw_sb = np.random.randint(0,data_len-1)
    NeuralNetwork(10,axs[0,0], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(20,axs[0,1], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(30,axs[1,0], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(50,axs[1,1], data[sw_sb][0], data[sw_sb][1])

    plt.show()
