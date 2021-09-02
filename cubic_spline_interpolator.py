import numpy as np

from scipy.interpolate import CubicSpline

def initialise_cubic_spline(x, y, ds, bc_type):

    distance = np.concatenate((np.zeros(1), np.cumsum(np.hypot(np.ediff1d(x), np.ediff1d(y)))))
    s = np.arange(0, distance[-1], ds)
    points = np.array([x, y]).T
    cs = CubicSpline(distance, points, bc_type=bc_type, axis=0, extrapolate=False)

    return cs, s

def generate_cubic_spline(x, y, ds=0.05, bc_type='natural'):
    
    cs, s = initialise_cubic_spline(x, y, ds, bc_type)

    # dx = dcs[0],  dy = dcs[1], ddx = ddcs[0],  ddy = ddcs[1]
    dcs = cs.derivative(1)(s).T
    yaw = np.arctan2(dcs[1], dcs[0])

    ddcs = cs.derivative(2)(s).T
    curvature = (ddcs[1]*dcs[0] - ddcs[0]*dcs[1]) / ((dcs[0]*dcs[0] + dcs[1]*dcs[1])**1.5)

    cs_points = cs(s).T

    return cs_points[0], cs_points[1], yaw, curvature

def generate_cubic_path(x, y, ds=0.05, bc_type='natural'):

    cs, s = initialise_cubic_spline(x, y, ds, bc_type)
    cs_points = cs(s).T
    return cs_points[0], cs_points[1]

def calculate_spline_yaw(x, y, ds=0.05, bc_type='natural'):
    
    cs, s = initialise_cubic_spline(x, y, ds, bc_type)
    dcs = cs.derivative(1)(s).T
    return np.arctan2(dcs[1], dcs[0])

def calculate_spline_curvature(x, y, ds=0.05, bc_type='natural'):

    cs, s = initialise_cubic_spline(x, y, ds, bc_type)
    dcs = cs.derivative(1)(s).T
    ddcs = cs.derivative(2)(s).T
    return (ddcs[1]*dcs[0] - ddcs[0]*dcs[1]) / ((dcs[0]*dcs[0] + dcs[1]*dcs[1])**1.5)

def main():
    
    import pandas as pd
    import matplotlib.pyplot as plt

    dir_path = 'waypoints.csv'
    df = pd.read_csv(dir_path)
    x = df['x'].values.tolist()
    y = df['y'].values.tolist()

    px, py = generate_cubic_path(x, y)
    pyaw = calculate_spline_yaw(x, y)
    pk = calculate_spline_curvature(x, y)

    plt.figure(1)
    plt.title("Geometry")
    plt.plot(x, y, '--o')
    plt.plot(px, py)

    plt.figure(2)
    plt.title("Yaw")
    plt.plot(np.rad2deg(pyaw))

    plt.figure(3)
    plt.title("Curvature")
    plt.plot(pk)
    
    plt.show()

if __name__ == '__main__':
    main()