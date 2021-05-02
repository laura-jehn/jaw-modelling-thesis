import numpy as np
from sympy import *
import matplotlib.pyplot as plt
from scipy import optimize

inc_init = np.array([79.4085, 0, -37.8728, 1]) # lower incisors at teeth occlusion
mp1 = [0, -51.7785, 0, 1] # right condyle at teeth occlusion
mp2 = [0, 51.7785, 0, 1] # left condyle at teeth occlusion

# condylar slopes
slope_wen = (lambda x: 0.0052*x**3-0.072*x**2-0.387*x) # taken from paper by Wen et. al, 2016
slope_artisynth = (lambda x: -3e-04*x**3+0.0247*x**2-6.981e-01*x) # taken from the ArtiSynth model

# slope being used
slope = slope_artisynth

optimization_initial_q = [0, 0, 0, 0, 0, 0]

### helper method for setting initial q for optimization from another file
def set_q_init(q):
    global optimization_initial_q
    optimization_initial_q = q

### given model parameters q forces_to_torques() computes the torques
### that have to be applied in the three rotational joints
### to produce force F at the lower incisors
### params: alpha, beta, gamma in degrees if degrees=true, else in radians
### F = (fx, fy, fz) force in world (mandible) coordinates
def forces_to_torques(alpha, beta, gamma, fx, fy, fz, degrees=False):
    if degrees:
        mTi = forward_kinematics_6DOF(0, 0, 0, np.radians(alpha), np.radians(beta), np.radians(gamma))[0]
    else:
        mTi = forward_kinematics_6DOF(0, 0, 0, alpha, beta, gamma)[0]
    mTiX = mTi.dot(inc_init)
    f = np.array([fx, fy, fz])
    # transform F to instantaneous frame coordinates
    f_i = np.linalg.inv(mTi)[0:3, 0:3].dot(f)
    return np.cross(inc_init[0:3], f_i)


### determines IP position given instantaneous x, y, beta and gamma
### parameters: x, y, beta (rad), gamma (rad)
### returns origin of instantaneous frame and incisor position (IP = mTi*inc_init)
def forward_kinematics_4DOF(x_i, y_i, beta_i, gamma_i):
    mTi = compute_correlated_params(x_i, y_i, beta_i, gamma_i)[0]
    return mTi[:,3], mTi.dot(inc_init)

### determines alpha and z given x, y beta and gamma using sympy solver
### parameters: x, y, beta (rad), gamma (rad)
### returns transformation matrix mTi, alpha (rad), z
def compute_correlated_params(x_i, y_i, beta_i, gamma_i):

    mP1 = Matrix(mp1) # right condyle
    mP2 = Matrix(mp1) # left condyle

    alpha_i, z_i = symbols("alpha, z_i")

    ca = cos(alpha_i)
    cb = cos(beta_i)
    cg = cos(gamma_i)
    sa = sin(alpha_i)
    sb = sin(beta_i)
    sg = sin(gamma_i)

    mTi = Matrix([[cg*cb, -sg*ca + cg*sb*sa, sg*sa+cg*sb*ca, x_i],
                [sg*cb, cg*ca + sg*sb*sa, -cg*sa+sg*sb*ca, y_i],
                [-sb, cb*sa, cb*ca, z_i],
                [0, 0, 0, 1]])

    mTi_func = lambdify((alpha_i, z_i), mTi, modules="numpy")

    iP1 = mTi*mP1 # x1 y1 z1
    x1 = iP1[0]
    z1 = iP1[2]
    iP2 = mTi*mP2 # x2 y2 z2
    x2 = iP2[0]
    z2 = iP2[2]
    Oi = 0.5 * (iP1 + iP2) # Oi is midpoint of condylar axis
    Oiz = Oi[2]

    res = nsolve((slope(x1)-z1, slope(x2)-z2, Oiz-z_i), (alpha_i, z_i), (0, 0), check=True)
    alpha = float(res[0])
    z = res[1]
    return mTi_func(alpha, z), alpha, z

### returns the transformation matrix from the mandible origin to instantaneous frame
### rz1, rz2 describe how far the position of the condyles deviates from the condylar slope
### they have to be minimized for finding alpha and z
### alpha, beta, gamma in radians
### x, y, z translations
def forward_kinematics_6DOF(x_i, y_i, z_i, alpha_i, beta_i, gamma_i):

    mP1 = np.array(mp1) # right condyle
    mP2 = np.array(mp2) # left condyle

    ca = np.cos(alpha_i)
    cb = np.cos(beta_i)
    cg = np.cos(gamma_i)
    sa = np.sin(alpha_i)
    sb = np.sin(beta_i)
    sg = np.sin(gamma_i)

    mTi = np.array([[cg*cb, -sg*ca + cg*sb*sa, sg*sa+cg*sb*ca, x_i],
                [sg*cb, cg*ca + sg*sb*sa, -cg*sa+sg*sb*ca, y_i],
                [-sb, cb*sa, cb*ca, z_i],
                [0, 0, 0, 1]])

    # instantaneous positions of condyles
    iP1 = mTi.dot(mP1)
    iP2 = mTi.dot(mP2)
    # condylar slope
    rz1 = slope(iP1[0])-iP1[2]
    rz2 = slope(iP2[0])-iP2[2]
    return mTi, rz1, rz2

# returns angles in degrees
def inverse_kinematics(inc_target):
    # if inc_target is given in 3d,
    # transform inc_target to homogenous notation
    if(len(inc_target) == 3):
        inc_target.append(1)
    # inc_target = mTi(q)*inc_init
    # <=> mTi(q)*inc_init - inc_target = 0
    def fw_kin(q):
        mTi, rz1, rz2 = forward_kinematics_6DOF(q[0], q[1], q[2], np.radians(q[3]), np.radians(q[4]), np.radians(q[5]))
        mTiX = mTi.dot(inc_init)
        v = mTiX - inc_target
        return np.linalg.norm(np.array([rz1, rz2]))**2 + np.linalg.norm(np.array([v[0], v[1], v[2]]))

    sol = optimize.minimize(fw_kin, optimization_initial_q, method="SLSQP",
        bounds=([0, 15], [-5, 5], [-7, 0], [-4, 4], [0, 35], [-10, 10]))

    q = sol.x
    mTi, _, _ = forward_kinematics_6DOF(q[0], q[1], q[2], np.radians(q[3]), np.radians(q[4]), np.radians(q[5]))

    assert(np.linalg.norm(mTi.dot(inc_init) - inc_target) < 1.5) # 1.5mm error margin
    return sol.x


### inverse kinematics ###

inc_target = np.array([70.00, 0, -66.67, 1])
q = inverse_kinematics(inc_target)
#print(q)

## test forces_to_torques at initial position of instantaneous frame ##

# test 1: torques cannot create 1N force in incisor direction, therefore result has to be 0
length = np.linalg.norm(inc_init)
ip_pos = [x/length for x in inc_init]
res = forces_to_torques(0, 0, 0, ip_pos[0], ip_pos[1], ip_pos[2])
np.testing.assert_almost_equal(res, np.zeros(3))

# test 2: 1N in z-direction should produce torque t=F*l=1*l around y axis
# with l=inc_init[0], i.e. the x-distance of the incisors
res = forces_to_torques(0, 0, 0, 0, 0, 1)
np.testing.assert_almost_equal(res, np.array([0, -inc_init[0], 0]))

res = forces_to_torques(0, 0, 0, 0, 1, 0)
np.testing.assert_almost_equal(res, np.array([-inc_init[2], 0, inc_init[0]]))

res = forces_to_torques(0, 0, 0, 1, 0, 0)
np.testing.assert_almost_equal(res, np.array([0, inc_init[2], 0]))
