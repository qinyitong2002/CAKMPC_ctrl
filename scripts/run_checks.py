"""Verify the arithmetic relations between the numbers of the supplementary
tables and the article.  Run from the repository root:

    python scripts/run_checks.py

Each check prints PASS or FAIL with the recomputed value; the script exits
with a non-zero status if any check fails.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cakmpc_supp import audits as A          # noqa: E402
from cakmpc_supp import certificate as C     # noqa: E402
from cakmpc_supp import conformal as CF      # noqa: E402
from cakmpc_supp import parameters as P      # noqa: E402
from cakmpc_supp import scheduling as S      # noqa: E402
from cakmpc_supp import statistics as ST     # noqa: E402
from cakmpc_supp import timing as T          # noqa: E402

RESULTS = []


def check(name, value, expected, tol):
    ok = abs(value - expected) <= tol
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {value:.6g} (reported {expected:.6g})")


def check_true(name, condition, detail=""):
    RESULTS.append(bool(condition))
    print(f"{'PASS' if condition else 'FAIL'}  {name} {detail}")


print("Section II-C - input budgets")
check("u_ff + u_fb <= u_bar", P.FEEDFORWARD_BOUND_A + P.FEEDBACK_BUDGET_A, 57.21, 1e-9)
check_true("current budget below the limit", P.FEEDFORWARD_BOUND_A + P.FEEDBACK_BUDGET_A <= P.CURRENT_LIMIT_A)

print("\nScheduling set (Table S7)")
check("Theta upper temperature (degC)", S.temperature_from_t_bar(S.THETA["T_bar"][1]), 64.9, 0.05)
check("Theta lower temperature (degC)", S.temperature_from_t_bar(S.THETA["T_bar"][0]), 20.1, 0.05)
check_true("R3 ramp inside Theta", S.temperature_from_t_bar(S.THETA["T_bar"][1]) >= S.MEASURED_RATES["R3_temperature_range_degC"][1])
check_true("R2 load rate below the bound", S.MEASURED_RATES["R2_F_ext_bar_max_change"] <= S.RATE_BOUND)
check("ideal 6 kN step in normalized units", 6000.0 / S.F_N0, 6.0, 1e-12)
check("triangular set: relative reduction of the replay p99.9",
      1 - S.TRIANGULAR["replay_p999_us"] / S.BOX["replay_p999_us"], 0.062, 5e-4)

print("\nCertificate (Table S5)")
check("gamma_f terminal term, untightened slew", C.gamma_f_terminal_term(P.SLEW_LIMIT_A), 688.9, 0.05)
check("gamma_f terminal term, tightened slew", C.gamma_f_terminal_term(C.SLEW_MARGIN_A), 33.9, 0.05)
check("bound of (24), c0 + a2 kappa", C.bound_24(), 8.2e4, 1)
for m, expected in ((0, 8.2e4), (1, 1.44e5), (2, 2.06e5), (4, 3.30e5), (11, 7.64e5)):
    check(f"J_bar_m for m = {m}", C.j_bar(m), expected, 1e3)
for regime, m in C.OBSERVED_FALLBACK_RUNS.items():
    print(f"      {regime}: m = {m}, J_bar_m = {C.j_bar(m):.3g}, |e1| bound = {C.e1_bound_um(C.j_bar(m)):.0f} um")
check("|e1| bound of (24) over the largest nominal RMSE", C.E1_BOUND_24_UM / 5.7, 156, 1)
check_true("margins after a back-off by the solver residual remain positive",
           C.AMPLITUDE_MARGIN_A - C.SOLVER_RESIDUAL_MAX_A > 0 and C.SLEW_MARGIN_A - C.SOLVER_RESIDUAL_MAX_A > 0,
           f"({C.AMPLITUDE_MARGIN_A - C.SOLVER_RESIDUAL_MAX_A:.2f} A, {C.SLEW_MARGIN_A - C.SOLVER_RESIDUAL_MAX_A:.2f} A)")
check_true("Assumption 3: certified sets inside E_op",
           max(v for s in C.INCLUSION.values() for v in s.values()) <= 1.0)
check("score exceedance, calibration", C.EXCEEDANCE_CALIBRATION, 0.04997, 5e-6)
check("score exceedance, held-out", C.EXCEEDANCE_HELDOUT, 0.0420, 5e-5)

print("\nCorollary 2")
for duration, expected in ((25, 0.879), (120, 0.42)):
    nb = C.blocks_in(duration)
    check(f"event probability, {duration} s ({nb} blocks)", C.event_probability(nb), expected, 5e-3)
nb = C.blocks_in(1e6 * P.SAMPLING_PERIOD_S)
check("blocks in 10^6 cycles", nb, 2703, 0)
check("expected violating blocks in 10^6 cycles", nb / (C.N_B + 1), 4.83, 5e-3)

print("\nClosed-loop audit (Table S10)")
total_blocks = sum(r[2] for r in A.CLOSED_LOOP_AUDIT)
total_out = sum(r[3] for r in A.CLOSED_LOOP_AUDIT)
check("blocks over R1, Rc, R2, R3", total_blocks, 5313, 0)
check("blocks outside W", total_out, 8, 0)
check("closed-loop block exceedance rate", total_out / total_blocks, 0.0015, 5e-5)
check("calibrated level 1/(n_b + 1)", 1 / (C.N_B + 1), 0.00179, 5e-6)
for regime, trials, blocks, out, *_ in A.CLOSED_LOOP_AUDIT:
    lo, hi = CF.clopper_pearson(out, blocks)
    print(f"      {regime}: {out}/{blocks}, 95 % CI [{100 * lo:.3f} %, {100 * hi:.3f} %]")

print("\nCalibration audit (Table S8)")
for name, n, k in A.SCORE_SETS:
    lo, hi = CF.clopper_pearson(k, n)
    print(f"      {name}: {k}/{n} = {100 * k / n:.2f} %, 95 % CI [{100 * lo:.2f} %, {100 * hi:.2f} %]")
check("held-out strata add up", sum(s[2] for s in A.HELDOUT_STRATA), 1120, 0)
check("held-out exceedances add up", sum(s[3] for s in A.HELDOUT_STRATA), 47, 0)
check("second calibration half, strata add up", sum(P.DESIGN["calibration_second_half_strata"]), 48866, 0)
check("policy training samples", 4 * P.DESIGN["training_samples_per_stratum"], 97732, 0)

print("\nMeasurement chain (Table S6)")
check("encoder resolution (um per count)", A.encoder_resolution_um(), 0.0458, 5e-4)

print("\nTiming (Table II, Table S11)")
r1 = T.BENCH_R1
check("R1 mean-latency reduction", 1 - r1["triggered (deployed)"][0] / r1["optimizer forced (M1)"][0], 0.484, 5e-4)
check("Corollary 1: T_qp_dl + T_oh <= T_s", P.DESIGN["T_qp_dl_us"] + P.DESIGN["T_oh_design_us"], 950.0, 0)
check_true("measured overhead below the design bound",
           T.STAGES["non-computational overhead"][2] <= P.DESIGN["T_oh_design_us"])
check("p99.9 with X_f as a share of T_s", T.REPLAY["PGS, with X_f (616 facets), Rc/R2"][2] / T.PERIOD_US, 0.733, 5e-4)
check("p99.9 with active terminal constraint as a share of T_s",
      T.REPLAY["PGS, with X_f, active terminal constraint"][2] / T.PERIOD_US, 0.743, 5e-4)
check_true("active-constraint rows bounded by the full replay",
           T.REPLAY["PGS, with X_f, active terminal constraint"][3] <= T.REPLAY["PGS, with X_f (616 facets), Rc/R2"][3])
check("replay screening failure rate", T.REPLAY_SCREENING["failed_1mA_criterion"] / T.REPLAY_SCREENING["instances"],
      0.000345, 5e-7)
for regime, d in T.BENCH_REGIMES.items():
    share = d["optimizer"] / d["cycles"]
    dl = d["deadline"] / d["optimizer"]
    inf = d["infeasible"] / d["optimizer"]
    fb = (d["deadline"] + d["infeasible"]) / d["cycles"]
    red = 1 - d["latency_triggered"][0] / d["latency_forced"][0]
    cost = d["rmse_triggered"] - d["rmse_forced"]
    print(f"      {regime}: optimizer share {100 * share:.1f} %, deadline discards {100 * dl:.2f} %, "
          f"infeasible {100 * inf:.2f} %, fallback {100 * fb:.4f} % of cycles, "
          f"latency reduction {100 * red:.1f} %, RMSE cost {cost:.1f} um ({100 * cost / d['rmse_triggered']:.1f} %)")
check("R2 fallback share", (41423 + 907) / 960000, 0.0441, 5e-5)
for regime in ("R1", "R2"):
    print(f"      {regime}: iterates with constraint residuals "
          f"{100 * T.NUMERICAL_RESIDUALS[regime] / T.BENCH_REGIMES[regime]['optimizer']:.2f} % of optimizer cycles")
pol = T.POLICY_TIMING
check("ensemble and test, mean (us)", pol["five-network ensemble with spread"][0] + pol["admission test (20)"][0], 93.7, 1e-9)
check("ensemble and test over the mean QP time", (26.5 + 67.2) / 331.0, 0.283, 5e-4)
check("ensemble over a single network", pol["five-network ensemble with spread"][0] / pol["single network"][0], 3.6, 0.05)
mem = sum(T.MEMORY_COEFFICIENTS.values()) * 8 / 1e6
check("memory in double precision (MB, 10^6 bytes)", mem, 0.253, 5e-4)
lo, hi = T.EMBEDDED_THROUGHPUT_RATIO
print(f"      embedded extrapolation of the QP p99.9: {lo * 732.5:.0f}-{hi * 732.5:.0f} us")

print("\nHorizon (Table S12)")
for n_p, margin, facets, p999, rmse in T.HORIZON:
    status = "feasible" if margin > 0 else "negative margin"
    print(f"      N_p = {n_p:2d}: margin {margin:6.2f} A, {facets} facets, p99.9 {p999:7.1f} us, "
          f"simulated RMSE {rmse} um ({status})")
best = min((r for r in T.HORIZON if r[1] > 0), key=lambda r: r[4])
check("horizon with the lowest simulated RMSE among feasible horizons", best[0], 12, 0)

print("\nStatistics (Table S14)")
check("smallest one-sided Wilcoxon p, n = 5", CF.wilcoxon_min_p(5), 1 / 32, 1e-12)
check("smallest Holm-adjusted p, n = 5, family of 3", 3 * CF.wilcoxon_min_p(5), 0.09375, 1e-12)
for level, tests in ST.TABLE_V_TESTS.items():
    adj = CF.holm(list(tests.values()))
    print(f"      {level}: " + ", ".join(f"{k} p = {p:.4f}, p_adj = {a:.3f}" for (k, p), a in zip(tests.items(), adj)))
    check_true(f"all Holm-adjusted p below 0.05 within '{level}'", max(adj) < 0.05)
pooled = CF.holm([p for t in ST.TABLE_V_TESTS.values() for p in t.values()])
print(f"      pooled over both levels (10 comparisons): smallest p_adj = {min(pooled):.3f}")
ca = ST.TABLE_IV["CA-KMPC, adaptation on"][0]
for base, (diff, lo, hi) in ST.TABLE_IV_PAIRED.items():
    check(f"Table IV mean difference to {base}", ca - ST.TABLE_IV[base][0], diff, 1e-9)
for base, expected in (("B8 physics NMPC", 0.28), ("B6 Koopman-LQR", 0.41), ("B4 bilinear KMPC", 0.45)):
    check(f"Table IV relative reduction against {base}", 1 - ca / ST.TABLE_IV[base][0], expected, 6e-3)
check("slope ratio B4 / CA-KMPC (Table III)", ST.TABLE_III["B4 bilinear KMPC"][1] / ST.TABLE_III["CA-KMPC"][1], 2.6, 0.02)
ca20 = ST.TABLE_III["CA-KMPC"][0][-1]
for base, expected in (("B6 Koopman-LQR", 0.43), ("B7 ADRC", 0.55), ("B4 bilinear KMPC", 0.60),
                       ("B8 physics NMPC", 0.67), ("B9 offset-free MPC", 0.71)):
    check(f"20 % mismatch, reduction against {base}", 1 - ca20 / ST.TABLE_III[base][0][-1], expected, 6e-3)

print("\nNominal session (Table I, part b)")
ns = ST.NOMINAL_SESSION
for regime in ("R1", "Rc"):
    print(f"      {regime}: fixed PD - CA-KMPC = {ns[('feedforward + fixed PD', regime)][0] - ns[('CA-KMPC', regime)][0]:.1f} um, "
          f"(Delta u_NN = 0) - CA-KMPC = {ns[('CA-KMPC, Delta u_NN = 0', regime)][0] - ns[('CA-KMPC', regime)][0]:.1f} um, "
          f"single network - CA-KMPC = {ns[('CA-KMPC, single network', regime)][0] - ns[('CA-KMPC', regime)][0]:.1f} um")

print(f"\n{sum(RESULTS)} of {len(RESULTS)} checks passed.")
sys.exit(0 if all(RESULTS) else 1)
