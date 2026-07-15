import numpy as np


def calculate_thevenin_voltage(Vphi, R1, X1, Xm):
    Vth = Vphi * (
        Xm /
        np.sqrt(R1**2 + (X1 + Xm)**2)
    )
    return Vth


def synchronous_speed(frequency, poles):
    n_sync = (120 * frequency) / poles
    w_sync = (2 * np.pi * n_sync) / 60
    return n_sync, w_sync


def thevenin_resistance(R1, X1, Xm):
    Rth = R1 * (
        Xm / (X1 + Xm)
    )**2
    return Rth


def thevenin_reactance(X1):
    Xth = X1
    return Xth


def rotor_speed(n_sync, slip):
    n_rotor = (1 - slip) * n_sync
    return n_rotor


def induced_torque(Vth, Rth, Xth, R2, X2, w_sync, slip):
    torque = (
        3 * (Vth**2) * (R2 / slip)
    ) / (
        w_sync * (
            (Rth + (R2 / slip))**2 +
            (Xth + X2)**2
        )
    )
    return torque