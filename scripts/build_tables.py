"""Write the CSV versions of the supplementary tables to tables/."""
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cakmpc_supp import audits as A          # noqa: E402
from cakmpc_supp import certificate as C     # noqa: E402
from cakmpc_supp import conformal as CF      # noqa: E402
from cakmpc_supp import parameters as P      # noqa: E402
from cakmpc_supp import positioning as POS   # noqa: E402
from cakmpc_supp import scheduling as S      # noqa: E402
from cakmpc_supp import statistics as ST     # noqa: E402
from cakmpc_supp import timing as T          # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "tables")
os.makedirs(OUT, exist_ok=True)


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote tables/" + name)


write("tableS1_positioning.csv", ["method"] + [f"({k}) {v[0]}" for k, v in POS.CRITERIA.items()] + ["notes"],
      [[m] + e.split() + [n] for m, e, n in POS.ROWS])
write("tableS2_joint_parameters.csv", ["quantity", "symbol", "value", "unit", "rel_95pct_CRB_pct"], P.JOINT)
write("tableS3_lifted_state.csv", ["indices", "coordinate", "role", "physics_guided_product"], S.LIFTED_STATE)
write("tableS5_certificate_constants.csv", ["quantity", "value"], [
    ("calibration blocks n_b", C.N_B), ("held-out blocks", C.N_HELDOUT_BLOCKS), ("q_w", C.Q_W),
    ("level 1/(n_b+1)", round(1 / (C.N_B + 1), 6)), ("held-out coverage", "279 of 279"),
    ("half-widths, error coordinates 1-8", " ".join(map(str, C.HALF_WIDTHS_ERROR))),
    ("half-widths, context coordinates 9-17", " ".join(map(str, C.HALF_WIDTHS_CONTEXT))),
    ("largest error-block residual", C.MAX_ERROR_BLOCK_RESIDUAL),
    ("lambda", C.LAMBDA), ("max vertex spectral radius", C.MAX_VERTEX_SPECTRAL_RADIUS),
    ("||K_b||", C.K_B_NORM), ("rate bound", C.RATE_BOUND), ("d_bar", C.D_BAR),
    ("||A_ce||_F", C.A_CE_FRO), ("||B_c||", C.B_C_NORM), ("||A_ec||_F", C.A_EC_FRO),
    *[(f"sigma_{i} (A)", v) for i, v in C.SIGMA.items()],
    ("facets of X_f / Omega_b", f"{C.X_F_FACETS} / {C.OMEGA_B_FACETS}"),
    ("backward-recursion steps", C.BACKWARD_RECURSION_STEPS),
    ("QP inequality rows without / with X_f", f"{C.QP_ROWS_WITHOUT_XF} / {C.QP_ROWS_WITH_XF}"),
    ("amplitude margin u_fb - sigma_{Np-1} (A)", C.AMPLITUDE_MARGIN_A),
    ("slew margin rho - sigma_Np - sigma_{Np-1} (A)", C.SLEW_MARGIN_A),
    ("u_bar / u_bar_ff / u_bar_fb (A)", "60 / 39.21 / 18"), ("rho_bar (A per sample)", P.SLEW_LIMIT_A),
    ("alpha / n / q_nu", f"{C.ALPHA} / {C.N_SCORE_CAL} / {C.Q_NU}"),
    ("score exceedance, calibration / held-out", f"{100 * C.EXCEEDANCE_CALIBRATION:.3f} % / {100 * C.EXCEEDANCE_HELDOUT:.2f} %"),
    ("gamma_f terminal term", round(C.gamma_f_terminal_term(C.SLEW_MARGIN_A), 1)),
    ("kappa", C.KAPPA), ("a_2", C.A2), ("c_0", C.C0), ("J_b", C.J_B),
    ("bound (24) as |e1| (um)", C.E1_BOUND_24_UM),
    *[(f"J_bar_m, m = {m} ({r})", f"{C.j_bar(m):.3g}; |e1| <= {C.e1_bound_um(C.j_bar(m)):.0f} um")
      for r, m in C.OBSERVED_FALLBACK_RUNS.items()],
    *[(f"{s}: max|{k}| / e_bar", v) for s, d in C.INCLUSION.items() for k, v in d.items()],
])
write("tableS6_measurement_chain.csv", ["signal", "sensor", "use", "resolution_noise", "acquisition"],
      A.MEASUREMENT_CHAIN)
write("tableS7_scheduling.csv", ["component", "normalization", "Theta", "physical range", "rate bound", "measured"], [
    ("F_ext_bar", "F_ext / F_N0, F_N0 = 1 kN", "[-3.3, 3.3]", "-3.3 to 3.3 kN", "1.400",
     "R2: max 1.34, p99.9 0.108, 0 cycles above the bound; 6 kN reversal in about 10 ms"),
    ("T_bar", "(T - 25 degC) / 35 degC", "[-0.14, 1.14]", "20 to 65 degC", "1.400",
     "R3 (25-60 degC): per-sample change below the resolution; 0 cycles outside Theta"),
    ("F_N_bar", "|F_ext| / F_N0", "[0, 3.3]", "0 to 3.3 kN", "1.400", "as F_ext_bar"),
    ("s_v", "sign(v_ref)", "[-1, 1]", "-", "previewed", "-"),
])
write("tableS7_offline_recomputations.csv", ["design", "vertices", "lambda", "max spectral radius",
                                             "X_f facets", "sigma_Np-1 (A)", "replay p99.9 (us)"], [
    ("box (deployed)", *[S.BOX[k] for k in ("vertices", "lambda", "max_vertex_spectral_radius", "X_f_facets",
                                            "sigma_Np_minus_1_A", "replay_p999_us")]),
    ("triangular (F_ext_bar, F_N_bar) set", *[S.TRIANGULAR[k] for k in ("vertices", "lambda",
                                              "max_vertex_spectral_radius", "X_f_facets", "sigma_Np_minus_1_A",
                                              "replay_p999_us")]),
    ("component-wise rate bounds", 16, "-", "-", S.COMPONENTWISE["X_f_facets"], "-", "-"),
])
rows = []
for name, n, k in A.SCORE_SETS:
    lo, hi = CF.clopper_pearson(k, n)
    rows.append((name, n, k, f"{100 * k / n:.2f}", f"{100 * lo:.2f}-{100 * hi:.2f}"))
for sv, load, n, k in A.HELDOUT_STRATA:
    rows.append((f"held-out stratum s_v = {sv:+d}, load {load}", n, k, f"{100 * k / n:.2f}", ""))
write("tableS8_calibration_audit.csv", ["set", "samples", "exceedances", "rate_pct", "CP95_pct"], rows)
write("tableS8_closed_loop_thresholds.csv", ["regime", "Pr(nu>0.9)", "Pr(nu>1)", "Pr(nu>1.1)"],
      A.CLOSED_LOOP_THRESHOLD_RATES)
write("tableS9_design_parameters.csv", ["parameter", "value"],
      [(k, v) for k, v in P.DESIGN.items()] + [(k, v) for k, v in P.REALTIME.items()])
rows = []
for r in list(A.CLOSED_LOOP_AUDIT) + [A.MISMATCH_REFERENCE]:
    lo, hi = CF.clopper_pearson(r[3], r[2])
    rows.append((*r, f"{100 * r[3] / r[2]:.3f}", f"{100 * lo:.3f}-{100 * hi:.3f}"))
write("tableS10_closed_loop_audit.csv", ["regime", "trials", "blocks", "blocks_outside_W", "cycles",
                                         "cycles_outside_W_coords_1-8", "cycles_outside_W_coords_9-17",
                                         "block_rate_pct", "CP95_pct"], rows)
rows = []
for reg, d in T.BENCH_REGIMES.items():
    rows.append((reg, d["cycles"], d["optimizer"], f"{100 * d['optimizer'] / d['cycles']:.1f}", d["deadline"],
                 f"{100 * d['deadline'] / d['optimizer']:.2f}", d["infeasible"],
                 f"{100 * d['infeasible'] / d['optimizer']:.2f}",
                 f"{100 * (d['deadline'] + d['infeasible']) / d['cycles']:.4f}", d["m"], d["recovery"],
                 d["admission_failure_pct"], *d["latency_triggered"], *d["latency_forced"],
                 f"{100 * (1 - d['latency_triggered'][0] / d['latency_forced'][0]):.1f}",
                 d["rmse_forced"], d["rmse_triggered"]))
write("tableS11_bench_regimes.csv", ["regime", "cycles", "optimizer_cycles", "optimizer_share_pct",
                                     "deadline_discards", "deadline_pct_of_optimizer", "infeasible_discards",
                                     "infeasible_pct_of_optimizer", "fallback_pct_of_cycles", "m",
                                     "max_recovery_cycles", "admission_failure_pct", "triggered_mean_us",
                                     "triggered_p999_us", "triggered_max_us", "forced_mean_us", "forced_p999_us",
                                     "forced_max_us", "mean_latency_reduction_pct", "rmse_forced_um",
                                     "rmse_triggered_um"], rows)
write("tableS11_stages.csv", ["stage", "mean_us", "p999_us", "max_us"], [(k, *v) for k, v in T.STAGES.items()])
write("tableII_source.csv", ["row", "mean_us", "p99_us", "p999_us", "max_us"], [(k, *v) for k, v in T.REPLAY.items()]
      + [(f"bench R1: {k}", v[0], "", v[1], v[2]) for k, v in T.BENCH_R1.items()])
write("tableS11_memory.csv", ["component", "coefficients", "bytes_double"],
      [(k, v, 8 * v) for k, v in T.MEMORY_COEFFICIENTS.items()])
write("tableS12_horizon.csv", ["N_p", "amplitude_margin_A", "X_f_facets", "replay_p999_us",
                               "simulated_rmse_Rc_um"], T.HORIZON)
write("tableS12_pruning.csv", ["scheme", "mean_us", "p999_us"], [(k, *v) for k, v in T.PRUNING_VS_TRIGGERING.items()])
write("tableS13_score_ablation.csv", ["item", "value"],
      [(f"dominant component: {k}", v) for k, v in ST.DOMINANT_COMPONENT.items()]
      + [(f"held-out flag rate: {k}", round(v, 4)) for k, v in ST.SINGLE_COMPONENT_HELDOUT_RATE.items()]
      + [(f"timing {k} (mean, p99.9 us)", f"{v[0]}, {v[1]}") for k, v in T.POLICY_TIMING.items()])
write("tableI_nominal_session.csv", ["configuration", "regime", "rmse", "sd", "rmse_excl", "e95", "max",
                                     "peak_iq", "rms_iq", "optimizer_share_pct", "admission_failure_pct"],
      [(c, r, *v) for (c, r), v in ST.NOMINAL_SESSION.items()])
rows = []
for level, (n, f, d) in ST.TABLE_V.items():
    rows.append((level, n, f, *[d[m][0] for m in ST.METHODS_V]))
write("tableV_plant_side.csv", ["level", "n", "F_em_rms_N", *ST.METHODS_V], rows)
rows = []
for level, tests in ST.TABLE_V_TESTS.items():
    adj = CF.holm(list(tests.values()))
    for (m, p), a in zip(tests.items(), adj):
        rows.append((level, m, round(p, 5), round(a, 4)))
write("tableS14_tableV_tests.csv", ["level", "baseline", "p", "p_holm"], rows)
write("tableS14_tableIV_paired.csv", ["baseline", "mean_difference_um", "ci_low", "ci_high"],
      [(k, *v) for k, v in ST.TABLE_IV_PAIRED.items()])
