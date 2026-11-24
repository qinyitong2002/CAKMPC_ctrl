"""Measurement chain (Table S6), calibration audit (Table S8), and
closed-loop residual audit (Table S10)."""

# ---------------------------------------------------------------------------
# Table S6 - measurement chain
# ---------------------------------------------------------------------------
ENCODER_LEAD_MM = 6.0
ENCODER_BITS = 17
ENCODER_NOISE_UM = 0.31          # standard deviation on stationary segments

MEASUREMENT_CHAIN = [
    # (signal, sensor, use, resolution / noise, acquisition)
    ("Screw-side position x; error e1", "motor encoder, 17 bit, 6 mm lead",
     "tracking error and feedback of all controllers",
     "0.046 um per count; noise SD 0.31 um", "drive, 1 kHz EtherCAT"),
    ("Axial load F_ext", "NS-WL5 load cell, +-20 kN",
     "scheduling (F_ext_bar, F_N_bar); low-pass filtered estimate F_hat for the clearance compensation",
     "-", "analog input of the I/O module, 1 kHz EtherCAT"),
    ("Housing temperature T", "WZPT-035 PT100",
     "scheduling (T_bar) and feedforward", "-", "I/O module, 1 kHz EtherCAT"),
    ("Output position x_out", "PDM-120S-A laser displacement sensor",
     "monitoring; not used by any controller", "-", "I/O module, 1 kHz EtherCAT"),
    ("Phase current", "CTC-100 current sensor",
     "auxiliary monitoring; not used by any controller", "-", "I/O module"),
]


def encoder_resolution_um(lead_mm=ENCODER_LEAD_MM, bits=ENCODER_BITS):
    return lead_mm * 1e3 / 2 ** bits


# Direction-bias sensitivity (Section S-I), simulation with the model of Table S2
DIRECTION_BIAS = {
    "F_g_const_N": 107.0,
    "crb_pct": 15.9,
    "force_deviation_N": 17.0,
    "reversal_window_ms": 20,
    "rmse_change_with_sv_um": 4.13,
    "rmse_change_without_sv_um": 27.38,
}

# ---------------------------------------------------------------------------
# Table S8 - calibration sets of Lemma 4 (score) and Lemma 2 (residual set)
# ---------------------------------------------------------------------------
SCORE_SETS = [
    # (set, samples, exceedances)
    ("calibration, second half", 48866, 2442),
    ("held-out (same decimation and stratification)", 1120, 47),
]
HELDOUT_STRATA = [
    # (s_v, load stratum, samples, exceedances)
    (+1, "low (|F_ext| <= F_N0)", 286, 10),
    (-1, "low (|F_ext| <= F_N0)", 283, 11),
    (+1, "high", 263, 12),
    (-1, "high", 288, 14),
]
CLOSED_LOOP_THRESHOLD_RATES = [
    # (regime, Pr(nu > 0.9), Pr(nu > 1), Pr(nu > 1.1))
    ("R1", 0.034, 0.016, 0.006),
    ("Rc", 0.041, 0.029, 0.014),
    ("R2", 0.227, 0.133, 0.065),
    ("thermal and load", 0.263, 0.185, 0.071),
]
LEMMA2_SPLIT = {
    "identification_trajectories": 13,
    "split": "2:2:1 into scale, calibration, and held-out blocks",
    "calibration_blocks": 559,
    "heldout_blocks": 279,
    "same_decimation": True,
    "same_stratification": True,
    "two_sample_test_p": 0.04,
    "heldout_coverage": "279 of 279",
}

# ---------------------------------------------------------------------------
# Table S10 - closed-loop residual audit
# ---------------------------------------------------------------------------
CLOSED_LOOP_AUDIT = [
    # (regime, trials, blocks, blocks outside W, cycles,
    #  cycles outside W in coordinates 1-8, in coordinates 9-17)
    ("R1", 8, 544, 0, 200000, 0, 0),
    ("Rc", 8, 544, 1, 200000, 26, 0),
    ("R2", 8, 2600, 5, 960000, 524, 622),
    ("R3", 5, 1625, 2, 600000, 334, 465),
]
MISMATCH_REFERENCE = ("Rc, 20 % mismatch (outside the certified regime)", 20, 1360, 1, 500000, 65, 227)

REVERSALS_IN_IDENTIFICATION_DATA = 3487
# Largest normalized residual max_j |w_j| / (q_w w_hat_j) on the identification
# data, within and outside +-20 ms of the reversals (reported precision).
REVERSAL_WINDOW_RESIDUAL = {"inside": 1.00, "outside": 1.00}
