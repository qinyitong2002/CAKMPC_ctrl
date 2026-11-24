"""Numerical content of the CA-KMPC supplementary material.

Every number that the supplementary tables report is defined once in the
modules of this package; the CSV files in ``tables/`` and the figures in
``figures/`` are generated from them by the scripts in ``scripts/``, and
``scripts/run_checks.py`` verifies the arithmetic relations between them.

Modules
-------
parameters   Identified joint parameters (Table S2) and design parameters (Table S9).
scheduling   Lifted state (Table S3), normalization of the scheduling vector and the
             scheduling set (Table S7).
certificate  Certificate constants and bound constants (Table S5).
audits       Measurement chain (Table S6), calibration audit (Table S8) and
             closed-loop residual audit (Table S10).
timing       Replay and bench timing (Table S11), terminal-set alternatives and
             horizon sensitivity (Table S12).
statistics   Score ablation (Table S13) and statistical details (Table S14).
conformal    Split-conformal routines used by Lemmas 1, 2, and 4 and Corollary 2.
"""

__all__ = [
    "parameters",
    "scheduling",
    "certificate",
    "audits",
    "timing",
    "statistics",
    "conformal",
]
