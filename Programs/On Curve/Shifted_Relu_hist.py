import numpy as np
from numpy import loadtxt
from math import log10, floor
from scipy.linalg import svdvals
from tensorflow.linalg import svd
from scipy.stats import ortho_group
import matplotlib.pyplot as plt
from multiprocessing import Pool


def srelu(x):
    return -1 if x<-1 else x

def NeuralNetwork(dep, axx, mat_var, bias_var):

    # size of matrices
    mat_size = 1000

    # multiprocessing.cpu_count() = 8
    with Pool(8) as p:
        #Weight_array = p.map(ortho_group.rvs, [1000 for _ in range(dep)])
        Weight_array = p.map(ortho_group.rvs, [mat_size for _ in range(dep)])

    for i in range(dep):
        Weight_array[i] *= mat_var

    D = [np.identity(mat_size) for _ in range(dep)]

    vec = np.random.randn(mat_size)

    for i in range(dep):
        bias_vec = np.random.randn(mat_size)*bias_var
        h = Weight_array[i].dot(vec) + bias_vec
        for j in range(mat_size):
            if h[j]<0:
                D[i][j,j] = 0
                vec[j]=0
            else:
                # phi^\prime = 1 = identity - matrix - entry
                vec[j] = h[j]

    Jacobi = np.identity(mat_size)

    for i in range(dep):
        # J = D_1*W_1 * D_2*W_2 * ... 
        Jacobi = np.matmul(np.matmul(Jacobi, D[i]), Weight_array[i])

    sv = svd(Jacobi)[0]
    print('check')

    print('---------------------------------------------------')
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

if __name__ == '__main__':

    fig, axs = plt.subplots(2,2)

    fig.tight_layout(pad = 3)

    data = loadtxt('srelu_critical.csv', delimiter=',')

    data_len = np.shape(data)[0]

    sw_sb = np.random.randint(0,data_len-1)
    NeuralNetwork(2,axs[0,0], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(8,axs[0,1], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(20,axs[1,0], data[sw_sb][0], data[sw_sb][1])
    NeuralNetwork(50,axs[1,1], data[sw_sb][0], data[sw_sb][1])

    plt.show()
