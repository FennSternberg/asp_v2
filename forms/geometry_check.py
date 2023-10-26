import numpy as np

# piecewise function wall profile calculation (profile 1 and profile3)
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

def calc_R2(W, wall_angle):  # attempted assumed radius function
    R2 = W / 10 - wall_angle / 20 
    return R2 

def calc_Rc(C1, wall_angle, depth,
            r):  # Calculate critical value Rc to determine if valid profile3
    Rc = (0.5 * C1 * np.cos(wall_angle * np.pi / 180.) - (depth - r) * np.sin(
        wall_angle * np.pi / 180.) - r) / (1. - np.sin(wall_angle * np.pi / 180.))
    return Rc

def calc_R(C1, wall_angle, depth, r):  # Calculate true circle radius for profile1 type
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
    flat = 2 * (np.tan(theta) * (R_f - R_f * np.sin(theta) - depth + r - r * np.sin(theta)) - R_f * np.cos(
        theta) + C1 / 2 - r * np.cos(theta))
   
    if flat < 0:
        return False
    elif profile2_y_from_xd_to_xc(flat / 2 + R_f * np.cos(theta), R_f, flat) > profile2_y_from_xb_to_xa(
            C1 / 2 - r * np.cos(theta), C1, r, depth):
        return False
    else:
        return True


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

