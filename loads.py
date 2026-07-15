import numpy as np


# Hoist (Constant Torque)
def hoist_torque(n_rotor, rated_torque):

    return np.ones_like(n_rotor) * rated_torque


# Calender (Constant Power)
def calender_torque(n_rotor, power_constant):

    w_rotor = (2 * np.pi * n_rotor) / 60

    # Avoid division by zero
    w_rotor = np.maximum(w_rotor, 15)

    torque = power_constant / w_rotor

    return torque


# Hydraulic Pump (Quadratic Torque)
def pump_torque(n_rotor, pump_constant):

    w_rotor = (2 * np.pi * n_rotor) / 60

    torque = pump_constant * w_rotor**2

    return torque


def operating_point(motor_torque, load_torque, n_rotor):
    """
    Numerically determines the operating point
    between the motor torque curve and the load torque curve.
    """

    index = np.argmin(np.abs(motor_torque - load_torque))

    return n_rotor[index], motor_torque[index]