# S-VII. Score Ablation and Statistical Details

## Table S13. Composite Score and Learned Policy

**(a) Components of the score (18).**

| Item | Distance $d_M$ | Residual $\varrho$ | Spread $\sigma_{\mathrm{ens}}$ | Composite |
|---|:-:|:-:|:-:|:-:|
| Share of the cycles with $\nu_k>1$ in which the component attains the maximum | 52.7 % | 29.4 % | 17.9 % | — |
| Held-out flag rate, each score recalibrated by (19) at $\alpha=0.05$ | 4.3 % | 5.6 % | 4.7 % | 4.2 % |

Each component carries a distinct part of the trigger. The single-component scores are recalibrated on the second calibration half in the same way as (19), so that their held-out rates are all close to $\alpha$; they differ in *which* cycles they flag.

**(b) Policy variants on the bench** (one session, $n=8$; RMSE in µm, shares in % of the cycles).

| Configuration | RMSE $R_1$ | RMSE $R_c$ | Optimizer share $R_1$ / $R_c$ | Admission failures $R_1$ / $R_c$ |
|---|:-:|:-:|:-:|:-:|
| CA-KMPC (five networks, composite score) | 4.4 | 3.9 | 5.8 / 6.6 | 0.6 / 0.6 |
| Single network, score without $\sigma_{\mathrm{ens}}$ (recalibrated) | 5.6 | 4.7 | 7.4 / 7.1 | 0.6 / 0.6 |
| No network correction, $M_2=\Pi_kK_bz^e_k$ | 6.7 | 5.8 | 10.8 / 5.1 | 0.7 / 0.2 |

**(c) Computation** (mean / p99.9, µs). Single network: 7.3 / 14.2; five networks with the spread: 26.5 / 51.9; admission test (20): 67.2 / 104.5. A single 15-64-32-16-1 network needs 3536 multiply–accumulate operations; the ensemble takes about 3.6 times as long as one network, and policy and test together take 93.7 µs on average, 28 % of the mean QP time.

The learned residual contributes about 2 µm of nominal accuracy over the backup law, and the ensemble a further 0.8–1.2 µm together with a lower optimizer share; both are retained.

## Table S14. Statistical Details

**Table III.** Medians over $n=20$ shared realizations per grade. The Holm correction is applied over the family of the 18 one-sided paired Wilcoxon comparisons of CA-KMPC with $B_4$, $B_5$, $B_6$, $B_7$, $B_8$, and $B_9$ at 12 %, 16 %, and 20 %. $B_1$, $B_2$, $B_3$, and $B_5$ were measured in a separate session and are reported as means for reference; ranking statements use the paired session. For $B_3$, the divergence rate is the primary figure, and its means are taken over the surviving trials only.

**Table IV** ($n=5$, real thermal drift). Paired differences of CA-KMPC (adaptation on) to each baseline, with bootstrap 95 % confidence intervals ($10^4$ resamples):

| Baseline | Mean difference (µm) | 95 % CI (µm) |
|---|:-:|:-:|
| $B_8$ physics NMPC | −5.5 | [−6.9, −3.1] |
| $B_6$ Koopman-LQR | −9.7 | [−14.0, −4.3] |
| $B_4$ bilinear KMPC | −11.2 | [−18.2, −5.2] |

With $n=5$, the smallest attainable one-sided exact Wilcoxon $p$ is $1/32=0.031$, and the smallest Holm-adjusted value over the family of three comparisons is 0.094; no comparison of Table IV is significant at 0.05. The bootstrap intervals rest on five pairs and indicate the direction and size of the differences rather than establish them.

**Table V** ($n=8$ at the two strongest levels). One-sided paired Wilcoxon tests of CA-KMPC against each paired baseline; Holm correction over the five comparisons within each level (smallest attainable $p=1/256$).

| Level | $B_4$ | $B_6$ | $B_7$ | $B_8$ | $B_9$ |
|---|:-:|:-:|:-:|:-:|:-:|
| Viscous +40 %, $p$ / $p_{\mathrm{adj}}$ | 0.0078 / 0.039 | 0.0117 / 0.039 | 0.0078 / 0.039 | 0.0078 / 0.039 | 0.0195 / 0.039 |
| Direction friction +40 %, $p$ / $p_{\mathrm{adj}}$ | 0.0117 / 0.047 | 0.0156 / 0.047 | 0.0117 / 0.047 | 0.0078 / 0.039 | 0.0117 / 0.047 |

Pooling both levels into one family of ten comparisons would raise the smallest adjusted value to 0.078. The levels with $n=5$ are reported without tests.

**Cross-session check.** See Section S-III; the 30 % acceptance threshold was fixed before the comparison.

Source: `cakmpc_supp/statistics.py`, `tables/tableS13_score_ablation.csv`, `tables/tableS14_*.csv`; `scripts/run_checks.py` recomputes the Holm adjustments.
