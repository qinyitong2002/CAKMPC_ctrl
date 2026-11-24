# CA-KMPC: Supplementary Material

Supplementary material of the article

> **Confidence-Triggered Koopman Predictive Control With Certified Feasibility for Humanoid Joints Under Operating-Condition Drift**, *IEEE Transactions on Systems, Man, and Cybernetics: Systems*.

The repository holds the supplementary sections of the article as documents, every number of the supplementary tables as Python data with CSV exports, the scripts that regenerate the supplementary figures and recompute the derived constants, the split-conformal routines of Lemmas 1, 2, and 4, and the humanoid gait data from which the test reference is derived. Numbers without the prefix "S" refer to the article.

## Contents

| Section | Document | Tables and figures |
|---|---|---|
| Nomenclature and positioning | [`docs/S0_nomenclature_and_positioning.md`](docs/S0_nomenclature_and_positioning.md) | Table S1 |
| S-I. Joint parameters and measurement chain | [`docs/S-I_joint_and_measurement.md`](docs/S-I_joint_and_measurement.md) | Tables S2, S6 |
| S-II. Lifted state, scheduling, and calibration | [`docs/S-II_lifting_scheduling_calibration.md`](docs/S-II_lifting_scheduling_calibration.md) | Tables S3, S7, S8; Figs. S1, S2 |
| S-III. Baselines, design parameters, and test protocol | [`docs/S-III_protocol_and_baselines.md`](docs/S-III_protocol_and_baselines.md) | Tables S4, S9; Fig. S3 |
| S-IV. Offline design and certificate constants | [`docs/S-IV_certificate.md`](docs/S-IV_certificate.md) | Algorithm S1, Table S5 |
| S-V. Closed-loop audit of the residual set | [`docs/S-V_closed_loop_audit.md`](docs/S-V_closed_loop_audit.md) | Table S10 |
| S-VI. Computation, timing, and deployment | [`docs/S-VI_computation.md`](docs/S-VI_computation.md) | Tables S11, S12; Figs. S4, S5 |
| S-VII. Score ablation and statistical details | [`docs/S-VII_score_and_statistics.md`](docs/S-VII_score_and_statistics.md) | Tables S13, S14 |

A PDF rendering of the same documents, `CA-KMPC_supplementary.pdf`, is produced by `scripts/build_pdf.sh`.

## Quick start

```bash
pip install -r requirements.txt
python scripts/run_checks.py      # recompute the derived constants and compare them with the tables
python scripts/build_tables.py    # regenerate tables/*.csv from cakmpc_supp/
python scripts/plot_figS4.py      # regenerate the figures from the same data
python scripts/plot_figS5.py
python -m pytest tests            # unit tests of the split-conformal routines
```

`scripts/run_checks.py` recomputes, among others, the probability bounds of Corollary 2, the Clopper–Pearson intervals of Tables S8 and S10, the terminal term of $\gamma_f$ and the bounds $\bar J_m$ of Theorem 2, the latency reductions, deadline-discard and fallback shares of Table S11, the memory footprint, and the Holm-adjusted $p$ values of Tables III–V, and reports whether each agrees with the tabulated value.

## Structure

```
cakmpc_supp/            numerical content of the supplement (single source of every tabulated number)
  parameters.py         Table S2 (joint), Table S9 (design and real-time settings)
  scheduling.py         Table S3 (lifted state), normalization of theta, Theta, Table S7
  certificate.py        Table S5 (certificate and bound constants), Corollary 2, Theorem 2 bounds
  audits.py             Table S6 (measurement chain), Table S8 (calibration), Table S10 (closed-loop audit)
  timing.py             source data of Table II, Tables S11 and S12
  statistics.py         Table S13, Table S14, source data of Tables I, III, IV, and V
  positioning.py        Table S1 with the criterion of each column
  conformal.py          split-conformal quantile, block calibration (Lemma 2), composite score (Lemma 4),
                        union bound (Corollary 2), Clopper-Pearson intervals, Holm correction
docs/                   supplementary sections S-0 to S-VII
tables/                 CSV export of every table
figures/                Figs. S1-S5
scripts/                checks, table export, figure scripts, PDF build
tests/                  unit tests
data/humanoid_gait/     joint-level gait data underlying the test reference
```

## Correspondence with the article

| Article | Repository |
|---|---|
| Model (1)–(2), Table S2 | `cakmpc_supp/parameters.py` |
| Lifted state (4), scheduling vector (3), $\Theta$ | `cakmpc_supp/scheduling.py`; Section S-II |
| Lemma 1, Lemma 2, (9) | `cakmpc_supp/conformal.py`: `conformal_quantile`, `block_scores`, `residual_set` |
| (18)–(19), Lemma 4 | `cakmpc_supp/conformal.py`: `raw_score`, `calibrate_composite`, `mahalanobis`, `ensemble_spread` |
| Corollary 2 | `cakmpc_supp/conformal.py`: `event_probability`; Section S-V |
| (11)–(14), Algorithm S1, Remark 2, Theorems 1 and 2 | `cakmpc_supp/certificate.py`; Section S-IV |
| Table II, Section VI-C | `cakmpc_supp/timing.py`; Section S-VI |
| Tables I, III, IV, V | `cakmpc_supp/statistics.py`; Section S-VII |

## Data

The repository contains the derived quantities reported in the article and the supplement, together with the humanoid gait data in `data/humanoid_gait/`. The raw bench logs are not included.

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

Code: MIT License ([`LICENSE`](LICENSE)). Documents, tables, figures, and data: CC BY 4.0 ([`LICENSE-docs`](LICENSE-docs)).
