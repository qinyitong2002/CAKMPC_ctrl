"""Unit tests of the split-conformal routines on synthetic exchangeable data."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cakmpc_supp import conformal as CF  # noqa: E402


def test_rank_matches_lemma_1():
    assert CF.conformal_rank(48866, 0.05) == int(np.ceil(0.95 * 48867))
    # alpha = 1/(n_b + 1) selects the largest calibration score (Lemma 2)
    assert CF.conformal_rank(559, 1 / 560) == 559


def test_marginal_coverage_of_the_quantile():
    rng = np.random.default_rng(0)
    n, alpha, trials = 200, 0.1, 4000
    hits = 0
    for _ in range(trials):
        s = rng.standard_normal(n + 1)
        hits += s[-1] <= CF.conformal_quantile(s[:-1], alpha)
    assert hits / trials >= 1 - alpha - 0.015


def test_residual_set_contains_every_calibration_block():
    rng = np.random.default_rng(1)
    residuals = rng.standard_normal((370 * 60, 17))
    blocks = CF.split_into_blocks(residuals, 370)
    w_hat = CF.scale_vector(blocks[:20])
    q_w, half_widths = CF.residual_set(blocks[20:], w_hat)
    inside, total = CF.coverage(blocks[20:], half_widths)
    assert inside == total and q_w > 0


def test_composite_score_is_calibrated_as_one_object():
    rng = np.random.default_rng(2)
    first = [rng.gamma(2.0, size=5000) for _ in range(3)]
    second = [rng.gamma(2.0, size=5000) for _ in range(3)]
    scales = tuple(np.quantile(f, 0.95) for f in first)
    q = CF.calibrate_composite(second, scales, 0.05)
    new = [rng.gamma(2.0, size=20000) for _ in range(3)]
    rate = np.mean(CF.raw_score(*new, scales) > q)
    assert rate <= 0.05 + 0.006


def test_holm_and_wilcoxon_bound():
    adj = CF.holm([2 / 256, 3 / 256, 2 / 256, 2 / 256, 5 / 256])
    assert np.allclose(adj, 0.0390625)
    assert CF.wilcoxon_min_p(5) == 1 / 32


def test_clopper_pearson_contains_the_estimate():
    lo, hi = CF.clopper_pearson(47, 1120)
    assert lo < 47 / 1120 < hi
    assert hi < 0.06
