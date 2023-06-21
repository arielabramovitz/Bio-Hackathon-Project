import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

kT = 1.0  # Boltzmann constant kT at room temperature


# General comments:
# ==================
# Equation of Brownian dynamics for each indepndent degree of freedom
# per time step dt:
# dx = dt * D/kT * nabla(U(x)) + sqrt(2D*dt)*N(0,1)

# Please prepare a Brownian dynamics simulation of two particles that
# interact via a harmonic potential. The particles are confined to a
# 2D box of size 10x10. The particles are initialized at positions
# (0,0) and (1,0). The particles have a diffusion coefficient of 1 um^2/s.
# The harmonic potential is given by U = 0.5*k*(r-r0)^2, where k=1 kt/A^2
def harmonic_potential(r, r0, k):
    '''
    computes the harmonic potential where k=1 kt/A^2.
    @param r - the position of the particle
    @param r0 - the equilibrium position of the particle (rest length)
    @param k - the spring constant
    '''
    return 0.5 * k * (r - r0) ** 2


def harmonic_potential_derivative(r, r0, k): # TODO: linear interpolation of the force towards the zero after half the way between drest and r
    '''
    computes the derivative of the harmonic potential where k=1 kT/A^2.
    @param r - the position of the particle
    @param r0 - the equilibrium position of the particle (rest length)
    @param k - the spring constant
    '''
    return k * (r - r0)


def brownian_dynamics_2_particles(dt, k, r0, D, T, N_steps):
    '''
    :param dt: the time step
    :param k: the spring constant
    :param r0: the equilibrium position of the particle (rest length)
    :param D: the diffusion coefficient
    :param T: the temperature
    :param N_steps: the number of steps
    :return: a tuple [T, X] where T is the time vector and X is the position
            matrix of the two particles, with dimensions (N_steps, 4), where
            the particle coordinates are stacked.
    '''
    # initialize the positions of the two particles
    x1 = np.array([0, 0])
    x2 = np.array([1, 0])
    # initialize the time vector
    T = np.arange(0, N_steps * dt, dt)
    # initialize the position matrix
    X = np.zeros((N_steps, 4))
    X[0, :] = np.hstack((x1, x2))  # TODO: make sure hstack is correct
    # initialize the random number generator
    rng = np.random.default_rng()
    # iterate over the time steps
    for i in range(1, N_steps):
        # compute the force on each particle
        r = np.linalg.norm(X[i - 1, 0:2] - X[i - 1, 2:4])
        F_magnitude = harmonic_potential_derivative(r, r0, k)  # units of kT/A
        F1 = -F_magnitude * (X[i - 1, 0:2] - X[i - 1, 2:4]) / r
        F2 = -F_magnitude * (X[i - 1, 2:4] - X[i - 1, 0:2]) / r
        # compute the random forces
        R1 = rng.normal(0, 1, 2)
        R2 = rng.normal(0, 1, 2)
        # compute the new positions
        dx1 = dt * D / kT * F1 + np.sqrt(2 * D * dt) * R1  # TODO verify BD equation
        dx2 = dt * D / kT * F2 + np.sqrt(2 * D * dt) * R2
        X[i, :] = X[i - 1, :] + np.hstack((dx1, dx2))
    return T, X


# Please plot the trajectories of the two particles.
# Please plot the distance between the two particles as a function of time.
# Please plot the potential energy of the system as a function of time.
# Please plot the probability distribution of the distance between the two
# particles at the end of the simulation.
# Please plot the probability distribution of the angle between the two
# particles at the end of the simulation.
# Please plot the probability distribution of the angle between the two
# particles at the end of the simulation, conditioned on the distance between
# the two particles being 1 um.
# Please plot the probability distribution of the angle between the two
# particles at the end of the simulation, conditioned on the distance between
# the two particles being 2 um.
def plot_trajectories(T, X, complicated=False):
    '''
    plots the trajectories of the two particles.
    @param T - the time vector
    @param X - the position matrix
    '''
    import matplotlib.pyplot as plt
    plt.figure()
    if complicated:
        # plot both series on the same plot
        # use a gradient of colors to show the time evolution
        for i in range(X.shape[0]):
            plt.plot(X[i, 0], X[i, 1], 'o', color=plt.cm.Blues(i / X.shape[0]))
            plt.plot(X[i, 2], X[i, 3], 'o', color=plt.cm.Reds(i / X.shape[0]))
    else:
        # plot both series on the same plot
        plt.plot(X[:, 0], X[:, 1], label='particle 1')
        plt.plot(X[:, 2], X[:, 3], label='particle 2')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()


# Please plot the MSD (mean squared displacement) of the two particles as a
# function of time.
def plot_MSD(T, X):
    '''
    plots the MSD (mean squared displacement) of the two particles as a
    function of time.
    @param T - the time vector
    @param X - the position matrix
    '''
    import matplotlib.pyplot as plt
    MSD1 = np.mean((X[:, 0:2] - X[0, 0:2]) ** 2, axis=1)
    MSD2 = np.mean((X[:, 2:4] - X[0, 2:4]) ** 2, axis=1)
    plt.figure()
    # plot both series on the same plot
    plt.plot(T, MSD1, label='particle 1')
    plt.plot(T, MSD2, label='particle 2')
    plt.legend()
    plt.xlabel('time [s]')
    plt.ylabel('MSD [um^2]')


# plot the distance between x1 and x2 as a function of time
def plot_distance(T, X):
    '''
    plots the distance between x1 and x2 as a function of time
    @param T - the time vector
    @param X - the position matrix
    '''
    import matplotlib.pyplot as plt
    plt.figure()
    r = np.linalg.norm(X[:, 0:2] - X[:, 2:4], axis=1)
    plt.plot(T, r)
    plt.xlabel('time [s]')
    plt.ylabel('distance [um]')


# plot histogram of distance over time
def plot_distance_histogram(T, X):
    '''
    plots the histogram of distance between the two particles
    @param T - the time vector
    @param X - the position matrix
    '''
    import matplotlib.pyplot as plt
    plt.figure()
    r = np.linalg.norm(X[:, 0:2] - X[:, 2:4], axis=1)
    plt.hist(r, bins=100)
    plt.xlabel('distance [um]')
    plt.ylabel('count')


def low_pass_filter(X, alpha):
    '''
    apply a Gaussian low-pass filter to the trajectories
    @param X - the position matrix
    @param alpha - the filter parameter
    '''
    # apply the filter to each particle separately
    X_low = np.zeros(X.shape)
    X_low[:, 0:2] = ndimage.gaussian_filter(X[:, 0:2], sigma=alpha)
    X_low[:, 2:4] = ndimage.gaussian_filter(X[:, 2:4], sigma=alpha)
    return X_low


# write a main function that generates 10000 frames of the simulation and
# plots the results
def main():
    # set the parameters
    dt = 0.001
    k = 0.2
    r0 = 5
    D = 1
    T = kT
    N_steps = 100000
    # run the simulation
    T, X = brownian_dynamics_2_particles(dt, k, r0, D, T, N_steps)
    # apply low-pass filter to the trajectories
    for alpha in [0.1, 0.5, 1.0, 2.0, 5.0]:
        X_low = low_pass_filter(X, alpha)
        # plot the results
        plot_trajectories(T, X_low, complicated=False)
        plt.title('alpha = ' + str(alpha))
        plot_distance(T, X_low)
        plot_distance_histogram(T, X_low)
        plt.title('alpha = ' + str(alpha))
        plt.show()
    plot_MSD(T, X)


if __name__ == '__main__':
    main()
