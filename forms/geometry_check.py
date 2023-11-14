import numpy as np


def y_s(C1, R1, R2, wall_angle, r, H):
    ys = R1 - (1 - R2 / R1) * (R1 ** 2 - x_d(C1, R1, R2, wall_angle, r, H) ** 2) ** 0.5
    return ys

def y_c(C1, R1, R2, wall_angle, r, H):
    theta = wall_angle * np.pi / 180
    yc = y_s(C1, R1, R2, wall_angle, r, H) - R2 * np.sin(theta)
    return yc

def x_s(C1, R1, R2, wall_angle, r, H):
    xs = x_d(C1, R1, R2, wall_angle, r, H) * (1 - R2 / R1)
    return xs

def x_c(C1, R1, R2, wall_angle, r, H):
    theta = wall_angle * np.pi / 180
    xc = x_d(C1, R1, R2, wall_angle, r, H) * (1 - (R2 / R1)) + R2 * np.cos(theta)
    return xc

def x_d(C1, R1, R2, wall_angle, r, H):
    theta = wall_angle * np.pi / 180
    if R1 > R2:
        xd = (R1 / (R1 - R2)) * (M(C1, R1, R2, theta, r, H) * (np.cos(theta)) ** 2 - np.sin(theta) * (
                (R1 - R2) ** 2 - (M(C1, R1, R2, theta, r, H) * np.cos(theta)) ** 2) ** 0.5)
        return xd
    elif R1 < R2:
        xd = (R1 / (R1 - R2)) * (M(C1, R1, R2, theta, r, H) * (np.cos(theta)) ** 2 + np.sin(theta) * (
                (R1 - R2) ** 2 - (M(C1, R1, R2, theta, r, H) * np.cos(theta)) ** 2) ** 0.5)
        return xd

    return

def x_b(C1, r, wall_angle):
    theta = wall_angle * np.pi / 180
    xb = C1 / 2 - r * np.cos(theta)
    return xb

def M(C1, R1, R2, theta, r, H):
    m_f = C1 / 2 - (R2 + r) * np.cos(theta) - np.tan(theta) * (H - R1 - r + R2 * np.sin(theta) + r * np.sin(theta))
    return m_f

def profile_1_and_3_y_from_zero_to_xd(x, R1):
    y = R1 - (R1 ** 2 - x ** 2) ** 0.5
    return y

def profile_1_and_3_y_from_zero_to_xd_prime(x, R1):
    dy_dx = x / ((R1 ** 2 - x ** 2) ** 0.5)
    return dy_dx

def profile_1_and_3_y_from_xd_to_xc(x, C1, R1, R2, wall_angle, r, H):
    y = y_s(C1, R1, R2, wall_angle, r, H) - (R2 ** 2 - (x - x_s(C1, R1, R2, wall_angle, r, H)) ** 2) ** 0.5
    return y

def profile_1_and_3_y_from_xd_to_xc_prime(x, C1, R1, R2, wall_angle, r, H):
    dy_dx = -(x_s(C1, R1, R2, wall_angle, r, H) - x) / (
            (R2 ** 2 - (x - x_s(C1, R1, R2, wall_angle, r, H)) ** 2) ** 0.5)
    return dy_dx

def y_from_xc_to_xb(x, C1, wall_angle, r, H):
    theta = wall_angle * np.pi / 180
    y = H - r + r * np.sin(theta) + (x - C1 / 2 + r * np.cos(theta)) * (1 / np.tan(theta))
    return y

def y_from_xc_to_xb_prime(wall_angle):
    theta = wall_angle * np.pi / 180
    dy_dx = 1 / np.tan(theta)
    return dy_dx

def y_from_xb_to_xa(x, C1, r, H):
    y = H - r + (r ** 2 - (x - (C1 / 2)) ** 2) ** 0.5
    return y

def profile2_y_from_xd_to_xc(x, R, flat):
    y = R - ((R ** 2 - (x - flat / 2) ** 2) ** 0.5)
    return y

def profile2_y_from_xd_to_xc_prime(x, R, flat):
    dy_dx = -(-x + flat / 2) / ((-x ** 2 + 2 * (flat / 2) * x + R ** 2 - (flat / 2) ** 2) ** 0.5)
    return dy_dx

def profile2_y_from_xb_to_xa(x, C1, r, H):
    y = H - r + (r ** 2 - (x - C1 / 2) ** 2) ** 0.5
    return y

def calc_long_from_short(W, r, wall_angle):  
    C1 = W + 2. * r * np.tan(np.pi / 4. - 0.5 * wall_angle * np.pi / 180.)
    return C1

def calc_short_from_long(C1, r, wall_angle): 
    W = C1 - 2. * r * np.tan(np.pi / 4. - 0.5 * wall_angle * np.pi / 180.)
    return W

def calc_R2(W, wall_angle):  
    R2 = W / 10 - wall_angle / 20 
    return R2 

def calc_Rc(C1, wall_angle, depth,
            r): 
    Rc = (0.5 * C1 * np.cos(wall_angle * np.pi / 180.) - (depth - r) * np.sin(
        wall_angle * np.pi / 180.) - r) / (1. - np.sin(wall_angle * np.pi / 180.))
    return Rc

def calc_R(C1, wall_angle, depth, r):
    R_correct = (0.5 * C1 * np.cos(wall_angle * np.pi / 180.) - (depth - r) * np.sin(
        wall_angle * np.pi / 180.) - r) / (1. - np.sin(wall_angle * np.pi / 180.))
    return R_correct

def valid_profile1(R_b, wall_angle, C1, depth, r, err):
    R_correct = calc_R(C1, wall_angle, depth, r)
    xc = R_correct * np.cos(wall_angle * np.pi / 180)

    if R_correct - (R_correct ** 2 - xc ** 2) ** 0.5 > y_from_xb_to_xa(
            x_b(C1, r, wall_angle), C1, r, depth):
        return False

    if (1 - err) * R_correct < R_b < (
            1 + err) * R_correct:
        return True
    else:
        return False

def valid_profile2(C1, R_f, wall_angle, r, depth):
    theta = wall_angle * np.pi/180 
    flat = get_profile2_flat(theta, R_f, depth, r, C1)
   
    if flat < 0:
        return False
    elif profile2_y_from_xd_to_xc(flat / 2 + R_f * np.cos(theta), R_f, flat) > profile2_y_from_xb_to_xa(
            C1 / 2 - r * np.cos(theta), C1, r, depth):
        return False
    else:
        return True
    
def get_profile2_flat(theta, R_f, depth, r, C1):
    return 2 * (np.tan(theta) * (R_f - R_f * np.sin(theta) - depth + r - r * np.sin(theta)) - R_f * np.cos(
        theta) + C1 / 2 - r * np.cos(theta))

def valid_profile3(R_b, R_f, wall_angle, C1, depth, r):
    Rc = calc_Rc(C1, wall_angle, depth, r)
    if R_b < Rc:
        return False
    elif R_f > Rc:
        return False
    elif profile_1_and_3_y_from_xd_to_xc(x_c(C1, R_b, R_f, wall_angle, r, depth), C1, R_b, R_f,
                                         wall_angle, r, depth) > y_from_xb_to_xa(
        x_b(C1, r, wall_angle), C1, r, depth):
        return False
    else:
        return True


def sketch_geometry(prof, C1_sketch, Rb_sketch, Rf_sketch, wall_angle_sketch, r_sketch, H_sketch, shape, C2):
   
    theta_sketch = angle_to_theta(wall_angle_sketch)
    if prof == 'profile1':
        x_all, y_all = sketch_profile1(C1_sketch, Rb_sketch, wall_angle_sketch, r_sketch, H_sketch)
    elif prof == 'profile2':
        flat_sketch = get_profile2_flat(theta_sketch, Rf_sketch, H_sketch, r_sketch, C1_sketch)
        x_all, y_all = sketch_profile2(C1_sketch, H_sketch, theta_sketch, Rf_sketch, flat_sketch, r_sketch)
    else:
        x_all, y_all = sketch_profile3(C1_sketch, Rb_sketch, Rf_sketch, wall_angle_sketch, r_sketch, H_sketch,)
    
    round_x = np.append(-np.flip(x_all),x_all)
    round_y = np.append(np.flip(y_all),y_all)
    if shape == "oblong":
        flat = C2 - C1_sketch
        x_all_oblong = np.append(np.linspace(0,flat/2,10), x_all + flat/2)
        y_all_oblong = np.append(np.zeros(10), y_all)
        oblong_x = np.append(-np.flip(x_all_oblong),x_all_oblong)
        oblong_y = np.append(np.flip(y_all_oblong),y_all_oblong)
    else:
        oblong_x = np.array([])
        oblong_y = np.array([])
    
    return round_x, round_y, oblong_x , oblong_y

def angle_to_theta(angle):
    theta = angle * np.pi / 180
    return theta

def sketch_profile1(C1, R, wall_angle, r, H):
    theta = wall_angle * np.pi / 180
    x = np.linspace(0, R * np.cos(theta), 10)  # circle
    y = R - (R ** 2 - x ** 2) ** 0.5

    x_all = x
    y_all = y

    x = np.linspace(R * np.cos(theta), x_b(C1, r, wall_angle), 10)  # wall CB
    y = y_from_xc_to_xb(x, C1, wall_angle, r, H)

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    x = np.linspace(x_b(C1, r, wall_angle), float(C1 / 2), 10)  # curve BA
    y = y_from_xb_to_xa(x, C1, r, H)

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    return x_all, y_all


def sketch_profile2(C1, H, theta, R, flat, r):
    x = np.linspace(0, flat / 2, 10)
    y = 0 * x

    x_all = x
    y_all = y

    x = np.linspace(flat / 2, flat / 2 + R * np.cos(theta), 10)  # curve DC
    y = profile2_y_from_xd_to_xc(x, R, flat)

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    x = np.linspace(flat / 2 + R * np.cos(theta), C1 / 2 - r * np.cos(theta), 10)  # wall CB
    y = H - r + r * np.sin(theta) + (x - C1 / 2 + r * np.cos(theta)) * (1 / np.tan(theta))

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    x = np.linspace(C1 / 2 - r * np.cos(theta), C1 / 2, 10)  # curve BA
    y = H - r + (r ** 2 - (x - C1 / 2) ** 2) ** 0.5
 

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    return x_all, y_all


def sketch_profile3(C1, R1, R2, wall_angle, r, H):
    x = np.linspace(0, x_d(C1, R1, R2, wall_angle, r, H), 10)  # curve OD
    y = profile_1_and_3_y_from_zero_to_xd(x, R1)

    x_all = x
    y_all = y

    x = np.linspace(x_d(C1, R1, R2, wall_angle, r, H), x_c(C1, R1, R2, wall_angle, r, H), 10)  # curve DC
    y = profile_1_and_3_y_from_xd_to_xc(x, C1, R1, R2, wall_angle, r, H)

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])
    x = np.linspace(x_c(C1, R1, R2, wall_angle, r, H), x_b(C1, r, wall_angle), 10)  # wall CB
    y = y_from_xc_to_xb(x, C1, wall_angle, r, H)
 
    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])
    x = np.linspace(x_b(C1, r, wall_angle), float(C1 / 2), 10)  # curve BA
    y = y_from_xb_to_xa(x, C1, r, H)

    x_all = np.append(x_all, x[1:])
    y_all = np.append(y_all, y[1:])

    return x_all, y_all
