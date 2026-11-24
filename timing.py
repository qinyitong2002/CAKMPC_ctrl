"""Computation and timing: source data of Table II, Table S11, and Table S12.

All times in microseconds.  Replay rows time the data update and the solve
of the condensed QP on an isolated core (Section S-VI); bench rows measure
the latency from sampling to the completion of the EtherCAT transfer.
"""

PERIOD_US = 1000.0

# ---------------------------------------------------------------------------
# Table II of the article (mean, p99, p99.9, max)
# ---------------------------------------------------------------------------
REPLAY = {
    "PGS, without X_f": (13.2, 54.9, 62.8, 64.4),
    "qpOASES, without X_f": (7.6, 33.7, 36.1, 38.4),
    "HPIPM, without X_f": (12.0, 28.8, 30.6, 34.3),
    "OSQP, without X_f": (38.4, 164.9, 166.5, 176.3),
    "PGS, with X_f (616 facets), Rc/R2": (331.0, 698.4, 732.5, 784.6),
    "PGS, with X_f, active terminal constraint": (432.0, 709.3, 742.8, 784.6),
    "qpOASES, with X_f (warm start)": (228.7, 674.8, 688.5, 706.4),
    "HPIPM, with X_f": (241.4, 672.5, 697.1, 727.4),
    "B8 NMPC (acados SQP-RTI)": (46.2, 171.7, 177.4, 186.9),
}

BENCH_R1 = {
    # (mean, p99.9, max); complete admission test (20) in every row
    "non-computational overhead": (204.0, 227.0, 235.0),
    "optimizer forced (M1)": (619.5, 673.8, 692.7),
    "policy forced (M2)": (295.8, 610.4, 676.1),
    "triggered (deployed)": (319.8, 855.6, 893.4),
}

# ---------------------------------------------------------------------------
# Table S11 - replay protocol statistics
# ---------------------------------------------------------------------------
REPLAY_SCREENING = {
    "instances": 200000,
    "failed_1mA_criterion": 69,
    "failed_p999_us": 265.0,
    "p999_including_failed_us": 732.5,
}
R1_REPLAY = {"mean_us": 302.0, "p999_us": 687.6}
ACTIVE_TERMINAL_SHARE = {"R1": 0.22, "Rc": 0.45, "R2": 0.61}
MEAN_ACTIVE_FACETS = {"R1": 9, "R2": 13}

# Bench, complete admission test, per regime
BENCH_REGIMES = {
    #        cycles,  opt.cycles, deadline, infeasible, m, recovery, admission %, RMSE M1, RMSE trig.
    "R1": dict(cycles=1_000_000, optimizer=57975, deadline=56, infeasible=0, m=2, recovery=1,
               admission_failure_pct=0.59, rmse_forced=3.8, rmse_triggered=4.2,
               latency_triggered=(319.8, 855.6, 893.4), latency_forced=(619.5, 673.8, 692.7)),
    "Rc": dict(cycles=200_000, optimizer=13427, deadline=2582, infeasible=32, m=4, recovery=3,
               admission_failure_pct=1.16, rmse_forced=3.4, rmse_triggered=3.7,
               latency_triggered=(376.6, 778.4, 805.3), latency_forced=(646.8, 755.1, 814.2)),
    "R2": dict(cycles=960_000, optimizer=241866, deadline=41423, infeasible=907, m=11, recovery=7,
               admission_failure_pct=3.44, rmse_forced=4.5, rmse_triggered=5.1,
               latency_triggered=(370.4, 895.4, 931.6), latency_forced=(636.8, 767.4, 809.9)),
}
FAULT_INJECTION = {"classes": 5, "injections_per_class": 20, "late_commands": 0}
LATE_COMMANDS = 0

# Iterates accepted by the deployed solver with constraint residuals
NUMERICAL_RESIDUALS = {"R1": 324, "R2": 1019, "fault_injection": 19,
                       "max_residual_A": 0.6, "transmitted_beyond_limits": 0}

# Stage decomposition, R1 triggered with the complete test (mean, p99.9, max)
STAGES = {
    "input transfer": (112.0, 171.0, 198.0),
    "lifting and score": (27.0, 49.0, 57.0),
    "admission test (20)": (63.0, 113.0, 121.0),
    "QP (optimizer cycles, completed)": (412.0, 587.0, 600.0),
    "output transfer": (65.0, 76.0, 83.0),
    "non-computational overhead": (204.0, 227.0, 235.0),
}
FIRST_OPTIMIZER_CYCLE_AFTER_POLICY_QP_MEAN_US = 531.0

# Policy evaluation and test, measured separately (mean, p99.9)
POLICY_TIMING = {
    "single network": (7.3, 14.2),
    "five-network ensemble with spread": (26.5, 51.9),
    "admission test (20)": (67.2, 104.5),
}

# ---------------------------------------------------------------------------
# Memory and extrapolation (Table S11)
# ---------------------------------------------------------------------------
MEMORY_COEFFICIENTS = {
    "X_f (616 facets x 9)": 616 * 9,
    "Omega_b (340 facets x 9)": 340 * 9,
    "Omega_2 and Omega_in (upper bound)": 340 * 9,
    "scheduled model G": 1530,
    "policy networks (5 x 3649)": 5 * 3649,
    "P, K_b, sigma_i, W and others": 200,
}
EMBEDDED_THROUGHPUT_RATIO = (3.0, 8.0)   # Cortex-A class relative to the i7-14650HX

# ---------------------------------------------------------------------------
# Table S12 - terminal-set alternatives and horizon
# ---------------------------------------------------------------------------
PRUNING = {
    "slack_threshold": 2.2e-4,
    "replay_mean_us": 286.0,
    "replay_p999_us": 608.0,
    "resolve_rate": 0.122,
}
PRUNING_VS_TRIGGERING = {
    # (mean, p99.9) end-to-end latency on R1
    "pruning only (optimizer every cycle)": (362.7, 663.1),
    "triggering only (bench)": (319.8, 855.6),
    "pruning and triggering": (331.8, 638.5),
}
HORIZON = [
    # (N_p, amplitude margin u_fb - sigma_{Np-1} [A], X_f facets,
    #  replay p99.9 [us], simulated RMSE on Rc [um])
    (8, 12.1, 502, 463.5, 4.1),
    (12, 10.93, 616, 732.5, 3.6),
    (16, 3.4, 683, 849.6, 4.3),
    (20, -2.7, 792, 1109.4, 4.7),
]
