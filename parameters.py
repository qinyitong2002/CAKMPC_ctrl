"""Joint parameters (Table S2) and design parameters (Table S9).

Units are SI unless stated in the key.  ``crb_pct`` is the relative 95 %
Cramer-Rao bound (1.96 sigma divided by the estimate); entries marked
'derived', 'prior', 'calib.', or 'design' were not estimated from the
identification data.
"""

# ---------------------------------------------------------------------------
# Table S2 - measured and verified parameters of the joint, model (1)-(2)
# ---------------------------------------------------------------------------
JOINT = [
    # (quantity, symbol, value, unit, crb_pct)
    ("Rated axial force", "F_rated", 6.5, "kN", "design"),
    ("Translational mass", "M", 33.6, "kg", 2.6),
    ("Joint viscous sum", "B_v + sigma_2", 1779.0, "N s/m", 8.5),
    ("Translational time constant", "tau_sys", 18.9, "ms", "derived"),
    ("Force-current gain", "K_f", 109.5, "N/A", 1.3),
    ("Coulomb friction, zero load", "F_c(0)", 120.0, "N", 1.6),
    ("Static friction, zero load", "F_s(0)", 158.3, "N", 2.5),
    ("Stribeck minimum velocity", "v_s_min", 0.23, "mm/s", 1.6),
    ("Stribeck saturation knee", "F_N_star", 512.0, "N", 8.6),
    ("Stribeck saturation shift", "Delta_v_s", 4.393, "mm/s", 1.6),
    ("Load coupling, linear", "alpha_F1", 1.80, "-", 2.8),
    ("Load coupling, quadratic", "alpha_F2", 0.111, "-", 2.5),
    ("Direction bias (constant)", "F_g_const", 107.0, "N", 15.9),
    ("Force-path lost motion", "delta(F)", 255.0, "um", "fit R^2 = 0.9998"),
    ("Series contact stiffness", "sigma_0", 1.75e7, "N/m", 10.0),
    ("Contact damping", "sigma_1", 150.0, "N s/m", "prior"),
    ("Thermal coupling", "alpha_T", 0.0145, "1/degC", 2.8),
    ("Torque constant", "K_t", 0.0901, "N m/A", "calib."),
    ("Reference contact force", "F_N0", 1000.0, "N", "design"),
]

# ---------------------------------------------------------------------------
# Input budgets (Section II-C)
# ---------------------------------------------------------------------------
CURRENT_LIMIT_A = 60.0          # u_bar, peak, enforced in all controllers
FEEDFORWARD_BOUND_A = 39.21     # u_bar_ff over the +-3 kN operating range
FEEDBACK_BUDGET_A = 18.0        # u_bar_fb
SLEW_LIMIT_A = 18.56            # rho_bar, A per sample
CONTINUOUS_RATING_A = 16.5      # enforced by the I^2 t protection of the drive
SAMPLING_PERIOD_S = 1e-3

# ---------------------------------------------------------------------------
# Table S9 - design parameters and implementation settings of CA-KMPC
# ---------------------------------------------------------------------------
DESIGN = {
    # predictive layer
    "N_p": 12,
    "N_c": 6,
    "Q_e": (2000.0, 500.0),           # diagonal, shared with B6, B8, B9
    "R": 2.0,
    "lifted_dimension": 17,
    "regressor_dimension": 90,
    "identified_coefficients": 1530,
    "identification_snapshots": 2.8e5,
    "vertex_spectral_radius_cap": 0.98,
    # deployed QP solver and deadline
    "solver": "dual projected Gauss-Seidel (PGS)",
    "iteration_cap": 5000,
    "termination_tolerance_A": 1e-3,
    "T_qp_dl_us": 650.0,
    "T_oh_design_us": 300.0,
    # online update (15)-(16)
    "N_u": 185,
    "lambda_f": 0.9998,
    "eps_exc": 1e-3,
    "update_budget_beta": 0.008,      # parameter of the update budget b_G
    "A4_online_LP": False,            # (A4) compares stored slacks, no online LP
    "background_test_time_ms": (3.0, 6.0),
    "rls_update_time_us_vectorized": (6.7, 9.1),
    # supervisor
    "alpha": 0.05,
    "N_d": 20,
    "hysteresis": (0.9, 1.1),
    "buffer_samples": 2000,
    "startup_hold_ms": 500,
    "startup_samples_in_Omega_in": 200,
    "startup_window_ms": 30,
    # learned policy
    "ensemble_size": 5,
    "network_layers": (15, 64, 32, 16, 1),
    "parameters_per_network": 3649,
    "training_samples": 9.8e4,        # 24 433 per (s_v, F_N) stratum
    "training_samples_per_stratum": 24433,
    "training_load_range_kN": (-3.0, 3.0),
    "training_temperature_range_degC": (25.0, 45.0),
    "training_reference": "random multi-sine, 0.2-0.8 Hz, stroke <= 55 mm, both directions",
    # composite score (18)-(19)
    "score_distance_input": "x = [z (17); F_ext_bar; T_bar], 19 coordinates",
    "score_covariance": "sample covariance with Ledoit-Wolf shrinkage, policy training set",
    "score_spread": "sample standard deviation of the five outputs (divisor 4)",
    "calibration_decimation_samples": 20,
    "calibration_second_half_strata": (12217, 12217, 12216, 12216),
    "q_nu": 1.4222,
    # selection of hyperparameters
    "hyperparameter_selection": "nested validation on conditions excluded from the tests",
    # baselines
    "B9_observer_bandwidth_rad_s": 120.0,
}

# ---------------------------------------------------------------------------
# Real-time configuration of the control computer (Section S-III)
# ---------------------------------------------------------------------------
REALTIME = {
    "processor": "Intel i7-14650HX, performance cores at 2.2 GHz",
    "os": "Ubuntu 22.04, PREEMPT_RT",
    "compiler": "gcc 11, -O3 -march=native",
    "soft_plc": "EtherCAT master on an isolated performance core, priority 95",
    "control_thread": "isolated performance core, SCHED_FIFO 90, mlockall, preallocated memory",
    "background_thread": "RLS and tests (A1)-(A4) on a third isolated core, SCHED_FIFO 25",
    "isolation": "isolcpus, nohz_full, rcu_nocbs",
    "model_replacement": "double buffer with atomic pointer swap at a cycle boundary",
    "bus": "EtherCAT, 1 kHz",
}
