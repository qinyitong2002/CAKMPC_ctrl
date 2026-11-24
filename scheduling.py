"""Lifted state (Table S3), scheduling vector, and scheduling set (Table S7)."""

import math

import numpy as np

# ---------------------------------------------------------------------------
# Table S3 - composition of the physics-guided lifted state
# ---------------------------------------------------------------------------
LIFTED_STATE = [
    # (indices, coordinate, role, physics-guided product)
    ("1-2", "e1, e2", "physical tracking output", False),
    ("3-4", "tanh(e1), tanh(e2)", "unit-scale saturation", False),
    ("5-6", "tanh(e1/2), tanh(e2/2)", "mid-regime nonlinearity", False),
    ("7", "tanh(e1 e2)", "position-velocity coupling", False),
    ("8", "tanh((e1 + e2)/2)", "combined nonlinear error", False),
    ("9", "F_N_bar", "contact-force proxy", False),
    ("10", "s_v", "direction indicator (taken from the preview)", False),
    ("11", "a_bar = a_ref / s_a", "commanded acceleration (taken from the preview)", False),
    ("12", "v_bar = v / s_vel", "carriage velocity", False),
    ("13", "F_N_bar e1", "load-correlated error", True),
    ("14", "s_v tanh(e2)", "direction-dependent error", True),
    ("15", "tanh(e1 F_N_bar)", "saturated load-error", True),
    ("16", "F_N_bar s_v", "load x direction", True),
    ("17", "tanh(F_N_bar)", "saturated load", False),
]
ERROR_DEPENDENT_CONTEXT = ("F_N_bar e1", "s_v tanh(e2)", "tanh(e1 F_N_bar)")
REFERENCE_PEAKS = {"s_a_mm_s2": 448.0, "s_vel_mm_s": 135.0}


def psi(e):
    """Error block psi(e) of the lifted state, eq. (4)."""
    e1, e2 = float(e[0]), float(e[1])
    return np.array([
        e1, e2,
        math.tanh(e1), math.tanh(e2),
        math.tanh(e1 / 2.0), math.tanh(e2 / 2.0),
        math.tanh(e1 * e2),
        math.tanh((e1 + e2) / 2.0),
    ])


def l_psi(e_op_sq):
    """Lipschitz-type bound ||psi(e)|| <= L_psi ||e|| on E_op (Section S-II)."""
    return math.sqrt(2.75 + e_op_sq / 4.0)


# ---------------------------------------------------------------------------
# Scheduling vector (3) and scheduling set Theta
# ---------------------------------------------------------------------------
F_N0 = 1000.0        # N
T0 = 25.0            # degC
DELTA_T_N = 35.0     # degC; Theta covers 20-65 degC (policy data: 25-45 degC)

THETA = {
    # component: (lower, upper)
    "F_ext_bar": (-3.3, 3.3),
    "T_bar": (-0.14, 1.14),
    "F_N_bar": (0.0, 3.3),
    "s_v": (-1.0, 1.0),
}


def scheduling_vector(f_ext_n, temperature_degc, v_ref):
    """theta_k = [F_ext_bar, T_bar, F_N_bar, s_v] of eq. (3)."""
    return np.array([
        f_ext_n / F_N0,
        (temperature_degc - T0) / DELTA_T_N,
        abs(f_ext_n) / F_N0,
        float(np.sign(v_ref)),
    ])


def temperature_from_t_bar(t_bar):
    return T0 + DELTA_T_N * t_bar


def in_theta(theta):
    keys = ("F_ext_bar", "T_bar", "F_N_bar", "s_v")
    return all(THETA[k][0] <= x <= THETA[k][1] for k, x in zip(keys, theta))


# ---------------------------------------------------------------------------
# Table S7 - scheduling rates measured on the bench
# ---------------------------------------------------------------------------
RATE_BOUND = 1.400   # deployed uniform bound Delta_theta (per sample)

MEASURED_RATES = {
    "R2_reversal_10_90_ms": 10.0,            # +3 -> -3 kN
    "R2_F_ext_bar_max_change": 1.34,
    "R2_F_ext_bar_p999_change": 0.108,
    "R2_cycles_above_bound": 0,
    "R2_cycles_outside_theta": 0,
    "R3_T_bar_max_change": "below the resolution of the temperature channel",
    "R3_preload_kN": 2.5,
    "R3_temperature_range_degC": (25.0, 60.0),
    "R3_cycles_outside_theta": 0,
}
POLICY_TRAINING_TEMPERATURE_DEGC = (25.0, 45.0)

# Offline recomputation with component-wise rate bounds (not deployed)
COMPONENTWISE = {
    "b_Delta_reduction_pct": 34.0,
    "kappa_reduction_pct": 22.0,
    "X_f_facets": 463,
}

# Offline recomputation with the triangular (F_ext_bar, F_N_bar) set (not deployed)
TRIANGULAR = {
    "vertices": 12,
    "lambda": 0.9901,
    "max_vertex_spectral_radius": 0.9796,
    "X_f_facets": 564,
    "sigma_Np_minus_1_A": 7.05,
    "replay_p999_us": 686.9,
}
BOX = {
    "vertices": 16,
    "lambda": 0.9901,
    "max_vertex_spectral_radius": 0.9802,
    "X_f_facets": 616,
    "sigma_Np_minus_1_A": 7.068,
    "replay_p999_us": 732.5,
}
