import numpy as np
import matplotlib.pyplot as plt

from motor import (
    calculate_thevenin_voltage,
    synchronous_speed,
    thevenin_resistance,
    thevenin_reactance,
    rotor_speed,
    induced_torque
)

from loads import (
    hoist_torque,
    calender_torque,
    pump_torque,
    operating_point
)

# MOTOR PARAMETERS ################################################

Vphi = 440 / np.sqrt(3)

R1 = 0.085
X1 = 0.196
R2 = 0.067
X2 = 0.161
Xm = 6.65

frequency = 60
poles = 8

# THÉVENIN EQUIVALENT #############################################

Vth = calculate_thevenin_voltage(Vphi, R1, X1, Xm)
Rth = thevenin_resistance(R1, X1, Xm)
Xth = thevenin_reactance(X1)

# SYNCHRONOUS SPEED ################################################

n_sync, w_sync = synchronous_speed(
    frequency,
    poles
)

# SLIP VECTOR #####################################################

slip = np.linspace(0.001, 1, 1000)

# MOTOR TORQUE CURVE ##############################################

n_rotor = rotor_speed(
    n_sync,
    slip
)

motor_torque = induced_torque(
    Vth,
    Rth,
    Xth,
    R2,
    X2,
    w_sync,
    slip
)

# MAXIMUM TORQUE ##################################################

max_torque = np.max(motor_torque)
max_index = np.argmax(motor_torque)

n_max_torque = n_rotor[max_index]
slip_max_torque = slip[max_index]

print(f"Maximum torque = {max_torque:.2f} N·m")
print(f"Rotor speed = {n_max_torque:.2f} rpm")
print(f"Slip = {slip_max_torque:.3f}")

# LOAD PARAMETERS #################################################

CONSTANT_TORQUE = 800

w_nominal = (2 * np.pi * n_sync) / 60

CALENDER_CONSTANT = CONSTANT_TORQUE * w_nominal
PUMP_CONSTANT = CONSTANT_TORQUE / (w_nominal ** 2)

# LOAD TORQUE CURVES ##############################################

hoist_curve = hoist_torque(
    n_rotor,
    CONSTANT_TORQUE
)

calender_curve = calender_torque(
    n_rotor,
    CALENDER_CONSTANT
)

pump_curve = pump_torque(
    n_rotor,
    PUMP_CONSTANT
)

# OPERATING POINTS ################################################

n_hoist, T_hoist = operating_point(
    motor_torque,
    hoist_curve,
    n_rotor
)

n_calender, T_calender = operating_point(
    motor_torque,
    calender_curve,
    n_rotor
)

n_pump, T_pump = operating_point(
    motor_torque,
    pump_curve,
    n_rotor
)

# RESULTS #########################################################

print("-" * 50)

print(f"Vth = {Vth:.2f} V")
print(f"Rth = {Rth:.4f} Ω")
print(f"Xth = {Xth:.4f} Ω")

print()

print(f"Motor maximum torque = {np.max(motor_torque):.2f} N·m")
print(f"Hoist maximum torque = {np.max(hoist_curve):.2f} N·m")
print(f"Calender maximum torque = {np.max(calender_curve):.2f} N·m")
print(f"Pump maximum torque = {np.max(pump_curve):.2f} N·m")

print()

print("OPERATING POINTS")
print(f"Hoist      -> {n_hoist:.2f} rpm | {T_hoist:.2f} N·m")
print(f"Calender   -> {n_calender:.2f} rpm | {T_calender:.2f} N·m")
print(f"Pump       -> {n_pump:.2f} rpm | {T_pump:.2f} N·m")

print("-" * 50)

# TORQUE-SPEED CHARACTERISTICS ####################################

plt.figure(figsize=(10, 6))

plt.plot(
    n_rotor,
    motor_torque,
    linewidth=3,
    label="Induction motor"
)

plt.plot(
    n_rotor,
    hoist_curve,
    linewidth=2,
    label="Hoist"
)

plt.plot(
    n_rotor,
    calender_curve,
    linewidth=2,
    label="Calender"
)

plt.plot(
    n_rotor,
    pump_curve,
    linewidth=2,
    label="Hydraulic pump"
)

# Maximum torque

plt.scatter(
    n_max_torque,
    max_torque,
    color="red",
    s=70,
    label="Maximum torque"
)

plt.annotate(
    r"$T_{max}$",
    (n_max_torque, max_torque),
    xytext=(n_max_torque + 40, max_torque - 150),
    arrowprops=dict(arrowstyle="->")
)

# Operating points

plt.scatter(
    n_hoist,
    T_hoist,
    marker="o",
    s=70,
    label="Hoist operating point"
)

plt.scatter(
    n_calender,
    T_calender,
    marker="s",
    s=70,
    label="Calender operating point"
)

plt.scatter(
    n_pump,
    T_pump,
    marker="^",
    s=70,
    label="Pump operating point"
)

plt.title("Torque-Speed Characteristics")
plt.xlabel("Mechanical speed (rpm)")
plt.ylabel("Torque (N·m)")
plt.xlim(0, n_sync)
plt.ylim(0, 3500)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

###############################################################
# EFFECT OF ROTOR RESISTANCE
###############################################################

R2_low = 0.03
R2_nominal = 0.067
R2_high = 0.20

torque_low = induced_torque(
    Vth,
    Rth,
    Xth,
    R2_low,
    X2,
    w_sync,
    slip
)

torque_nominal = induced_torque(
    Vth,
    Rth,
    Xth,
    R2_nominal,
    X2,
    w_sync,
    slip
)

torque_high = induced_torque(
    Vth,
    Rth,
    Xth,
    R2_high,
    X2,
    w_sync,
    slip
)

plt.figure(figsize=(8, 5))

plt.plot(
    n_rotor,
    torque_low,
    label="R₂ = 0.03 Ω"
)

plt.plot(
    n_rotor,
    torque_nominal,
    label="R₂ = 0.067 Ω"
)

plt.plot(
    n_rotor,
    torque_high,
    label="R₂ = 0.20 Ω"
)

plt.grid(True)
plt.legend()
plt.xlabel("Mechanical speed (rpm)")
plt.ylabel("Torque (N·m)")
plt.title("Effect of Rotor Resistance")
plt.tight_layout()
plt.show()