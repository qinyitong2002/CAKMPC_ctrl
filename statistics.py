"""Score ablation (Table S13), statistical details (Table S14), and the
source data of Tables I, III, IV, and V of the article.  RMSE in micrometers.
"""

# ---------------------------------------------------------------------------
# Table S13 - composite score (18) and learned policy
# ---------------------------------------------------------------------------
DOMINANT_COMPONENT = {"Mahalanobis distance": 0.527, "one-step residual": 0.294,
                      "ensemble spread": 0.179}
SINGLE_COMPONENT_HELDOUT_RATE = {"distance only": 0.043, "residual only": 0.056,
                                 "spread only": 0.047, "composite": 47 / 1120}

# Bench, one session, n = 8 per cell: (RMSE mean, SD, RMSE_excl, e95, max,
#  peak |i_q|, RMS i_q, optimizer share %, admission failure %)
NOMINAL_SESSION = {
    ("CA-KMPC", "R1"): (4.4, 1.0, 4.6, 10.3, 13.8, 13.6, 5.8, 5.8, 0.6),
    ("CA-KMPC", "Rc"): (3.9, 0.8, 3.8, 8.2, 11.4, 12.1, 5.2, 6.6, 0.6),
    ("feedforward only", "R1"): (542.0, 205.0, 508.0, 779.0, 794.0, 12.3, 5.9, None, None),
    ("feedforward only", "Rc"): (436.0, 189.0, 397.0, 682.0, 721.0, 11.6, 5.8, None, None),
    ("feedforward + fixed PD", "R1"): (6.5, 2.1, 6.1, 15.3, 18.7, 10.8, 5.5, None, None),
    ("feedforward + fixed PD", "Rc"): (6.1, 1.8, 4.3, 13.9, 16.3, 10.1, 5.3, None, None),
    ("CA-KMPC, Delta u_NN = 0", "R1"): (6.7, 2.4, 5.8, 14.4, 17.2, 17.6, 6.2, 10.8, 0.7),
    ("CA-KMPC, Delta u_NN = 0", "Rc"): (5.8, 1.6, 3.9, 12.6, 15.8, 9.6, 5.1, 5.1, 0.2),
    ("CA-KMPC, single network", "R1"): (5.6, 1.5, 5.2, 11.7, 16.2, 11.8, 5.6, 7.4, 0.6),
    ("CA-KMPC, single network", "Rc"): (4.7, 1.3, 3.8, 9.8, 12.9, 9.8, 5.1, 7.1, 0.6),
}

# ---------------------------------------------------------------------------
# Table I (part a) - nominal tracking, n = 8
# (RMSE, SD, RMSE_excl, e95, max, peak |i_q|, RMS i_q)
# ---------------------------------------------------------------------------
TABLE_I = {
    ("CA-KMPC", "R1"): (4.3, 0.9, 4.0, 10.2, 14.3, 14.2, 5.1),
    ("B8 NMPC", "R1"): (4.5, 1.6, 4.3, 12.6, 16.1, 18.4, 6.5),
    ("B9 offset-free", "R1"): (5.9, 1.1, 5.3, 14.3, 14.7, 14.6, 6.5),
    ("CA-KMPC", "Rc"): (3.8, 0.8, 3.3, 6.7, 9.4, 12.6, 4.8),
    ("B8 NMPC", "Rc"): (3.9, 0.8, 3.1, 9.2, 12.3, 11.0, 5.8),
    ("B9 offset-free", "Rc"): (5.2, 0.8, 4.4, 12.2, 13.0, 12.9, 5.0),
    ("CA-KMPC", "R2"): (5.7, 1.3, 4.2, 12.6, 21.8, 33.4, 26.4),
    ("B8 NMPC", "R2"): (6.9, 1.3, 5.6, 13.6, 20.2, 29.8, 25.1),
    ("B9 offset-free", "R2"): (7.7, 1.0, 6.8, 13.9, 28.7, 32.4, 30.1),
}

# ---------------------------------------------------------------------------
# Table III - median RMSE on Rc versus controller-side model mismatch, n = 20
# ---------------------------------------------------------------------------
GRADES = (0, 4, 8, 12, 16, 20)
TABLE_III = {
    "CA-KMPC": ((3.6, 24.3, 44.1, 65.5, 84.7, 94.4), 469, 0.0),
    "B6 Koopman-LQR": ((3.8, 29.1, 55.7, 89.6, 106.4, 164.5), 764, 0.0),
    "B7 ADRC": ((4.2, 56.3, 118.2, 167.9, 203.7, 208.4), 1081, 0.0),
    "B4 bilinear KMPC": ((2.3, 32.6, 86.5, 141.4, 192.8, 238.4), 1226, 1.7),
    "B8 physics NMPC": ((4.1, 62.1, 124.1, 180.7, 233.9, 288.4), 1424, 0.0),
    "B9 offset-free MPC": ((5.4, 69.0, 122.7, 190.4, 256.3, 322.6), 1583, 1.7),
    # separate session; means; B3 over surviving trials only
    "B5 deep KMPC": ((4.7, 24.3, 48.2, 70.7, 95.0, 145.9), 672, 0.0),
    "B2 Koopman tube MPC": ((5.0, 95.0, 214.0, 315.9, 444.5, 549.7), 2767, 0.0),
    "B1 adaptive PID": ((2.9, 85.7, 196.3, 302.6, 410.5, 504.1), 2562, 4.2),
    "B3 online KMPC": ((1.6, 48.1, 65.7, 84.4, 206.3, 182.4), None, 95.0),
}
SEPARATE_SESSION = ("B1 adaptive PID", "B2 Koopman tube MPC", "B3 online KMPC", "B5 deep KMPC")

# ---------------------------------------------------------------------------
# Table IV - real thermal drift R3, n = 5 (mean, SD, max, saturated %)
# ---------------------------------------------------------------------------
TABLE_IV = {
    "CA-KMPC, adaptation on": (13.9, 6.9, 21.2, 0.9),
    "CA-KMPC, adaptation off": (14.7, 8.4, 22.7, 1.4),
    "CA-KMPC, triggered": (16.6, 8.6, 27.3, 1.2),
    "B8 physics NMPC": (19.4, 12.1, 34.1, 3.0),
    "B6 Koopman-LQR": (23.6, 12.7, 44.7, 1.9),
    "B4 bilinear KMPC": (25.1, 14.6, 54.7, 2.3),
}
TABLE_IV_PAIRED = {
    # paired difference CA-KMPC (adaptation on) - baseline, bootstrap 95 % CI
    "B8 physics NMPC": (-5.5, -6.9, -3.1),
    "B6 Koopman-LQR": (-9.7, -14.0, -4.3),
    "B4 bilinear KMPC": (-11.2, -18.2, -5.2),
}

# ---------------------------------------------------------------------------
# Table V - plant-side perturbations emulated by the loading axis on Rc
# (median RMSE, IQR, emulated-force tracking error %); n = 5, n = 8 for +40 %
# ---------------------------------------------------------------------------
METHODS_V = ("CA-KMPC", "B4", "B6", "B7", "B8", "B9")
TABLE_V = {
    # level: (n, F_em RMS [N], {method: (median, IQR, tracking error %)})
    "none": (5, 0.0, {"CA-KMPC": (3.6, 1.5, None), "B4": (2.6, 0.7, None), "B6": (3.6, 1.4, None),
                      "B7": (4.7, 2.4, None), "B8": (4.3, 2.1, None), "B9": (5.2, 2.6, None)}),
    "inertia +10 %": (5, 0.7, {"CA-KMPC": (4.0, 1.6, 6.5), "B4": (4.3, 2.1, 8.2), "B6": (4.1, 2.1, 8.5),
                               "B7": (5.6, 2.4, 10.7), "B8": (5.9, 2.9, 9.7), "B9": (6.8, 3.1, 12.2)}),
    "inertia +20 %": (5, 1.4, {"CA-KMPC": (4.8, 1.6, 7.9), "B4": (7.3, 1.8, 9.2), "B6": (7.1, 2.2, 9.3),
                               "B7": (7.9, 2.6, 11.4), "B8": (8.7, 2.9, 9.8), "B9": (10.3, 3.5, 11.9)}),
    "viscous +20 %": (5, 19.8, {"CA-KMPC": (43.1, 11.5, 8.7), "B4": (91.6, 29.3, 11.8), "B6": (60.7, 23.3, 8.6),
                                "B7": (97.3, 27.0, 14.7), "B8": (121.4, 39.4, 13.6), "B9": (57.3, 21.8, 7.4)}),
    "viscous +40 %": (8, 39.5, {"CA-KMPC": (76.8, 27.5, 8.2), "B4": (153.2, 56.3, 16.5), "B6": (109.7, 38.2, 11.8),
                                "B7": (182.5, 66.5, 9.7), "B8": (193.8, 79.6, 16.3), "B9": (121.3, 42.1, 7.6)}),
    "direction friction +20 %": (5, 24.0, {"CA-KMPC": (52.6, 21.1, 7.9), "B4": (98.8, 41.0, 8.5),
                                           "B6": (60.5, 22.5, 9.4), "B7": (131.2, 36.4, 10.7),
                                           "B8": (122.3, 48.7, 12.6), "B9": (76.4, 26.5, 9.1)}),
    "direction friction +40 %": (8, 48.0, {"CA-KMPC": (79.8, 32.7, 7.4), "B4": (221.8, 80.7, 13.4),
                                           "B6": (127.3, 48.5, 9.2), "B7": (196.8, 64.4, 13.6),
                                           "B8": (264.2, 97.9, 15.4), "B9": (116.1, 46.3, 9.8)}),
}
TABLE_V_TESTS = {
    # one-sided paired Wilcoxon, raw p, n = 8; Holm over the five comparisons of a level
    "viscous +40 %": {"B4": 2 / 256, "B6": 3 / 256, "B7": 2 / 256, "B8": 2 / 256, "B9": 5 / 256},
    "direction friction +40 %": {"B4": 3 / 256, "B6": 4 / 256, "B7": 3 / 256, "B8": 2 / 256, "B9": 3 / 256},
}

# ---------------------------------------------------------------------------
# Table S14 - statistical details
# ---------------------------------------------------------------------------
CROSS_SESSION = {
    "methods": ("CA-KMPC", "B4", "B6"),
    "grades_pct": (0, 8, 20),
    "max_relative_deviation_pct": (21, 16, 5),
    "acceptance_threshold_pct": 30,
    "threshold_fixed": "before the comparison",
}
TABLE_III_FAMILY = "18 one-sided comparisons of CA-KMPC with B4, B5, B6, B7, B8, and B9 at 12 %, 16 %, and 20 %"
TABLE_IV_FAMILY = "3 one-sided comparisons of CA-KMPC (adaptation on) with B8, B6, and B4"
TABLE_V_FAMILY = "5 one-sided comparisons of CA-KMPC with B4, B6, B7, B8, and B9 within each level"
