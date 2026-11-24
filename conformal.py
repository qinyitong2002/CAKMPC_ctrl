"""Split-conformal routines behind Lemmas 1, 2, and 4 and Corollary 2.

The functions operate on arrays supplied by the user; they reproduce the
constructions of the article on any data set, for example on residuals and
scores produced with the model of Table S2.
"""

import math

import numpy as np
from scipy import stats


def conformal_rank(n, alpha):
    """Rank ceil((1 - alpha)(n + 1)) of Lemma 1; requires it to be <= n."""
    k = math.ceil((1.0 - alpha) * (n + 1) - 1e-12)
    if k > n:
        raise ValueError("alpha too small for n calibration scores")
    return k


def conformal_quantile(scores, alpha):
    """q_hat of Lemma 1: the ceil((1 - alpha)(n + 1))-th smallest score."""
    s = np.sort(np.asarray(scores, dtype=float))
    return s[conformal_rank(s.size, alpha) - 1]


# ---------------------------------------------------------------------------
# Lemma 2 - calibrated residual set
# ---------------------------------------------------------------------------
def split_into_blocks(residuals, block_length):
    """Cut a (T, n_z) residual array into consecutive blocks of block_length rows."""
    r = np.asarray(residuals, dtype=float)
    n_blocks = r.shape[0] // block_length
    return r[: n_blocks * block_length].reshape(n_blocks, block_length, r.shape[1])


def block_scores(blocks, w_hat):
    """s^(b) = max_{k in b} max_j |w_{k,j}| / w_hat_j for every block."""
    w_hat = np.asarray(w_hat, dtype=float)
    return np.max(np.abs(blocks) / w_hat, axis=(1, 2))


def scale_vector(scale_blocks):
    """w_hat: coordinatewise supremum of |w| over the disjoint scale set."""
    return np.max(np.abs(np.asarray(scale_blocks)), axis=(0, 1))


def residual_set(calibration_blocks, w_hat):
    """q_w and the half-widths q_w w_hat of W, eq. (9), at level 1/(n_b + 1).

    With alpha = 1/(n_b + 1) the rank of Lemma 1 equals n_b, so that q_w is
    the largest calibration block score.
    """
    s = block_scores(calibration_blocks, w_hat)
    n_b = s.size
    q_w = conformal_quantile(s, 1.0 / (n_b + 1.0))
    return q_w, q_w * np.asarray(w_hat, dtype=float)


def coverage(blocks, half_widths):
    """Number of blocks whose residuals all lie in W."""
    inside = np.all(np.abs(blocks) <= np.asarray(half_widths), axis=(1, 2))
    return int(inside.sum()), int(inside.size)


# ---------------------------------------------------------------------------
# Lemma 4 - composite score (18)-(19)
# ---------------------------------------------------------------------------
def raw_score(d_m, rho, sigma_ens, scales):
    """nu_raw = max{d_M/s_d, rho/s_r, sigma_ens/s_sigma}."""
    s_d, s_r, s_s = scales
    return np.maximum.reduce([np.asarray(d_m) / s_d, np.asarray(rho) / s_r,
                              np.asarray(sigma_ens) / s_s])


def calibrate_composite(second_half, scales, alpha):
    """q_nu of (19) on the second calibration half (scales fixed beforehand)."""
    return conformal_quantile(raw_score(*second_half, scales), alpha)


def mahalanobis(x, mean, covariance):
    """d_M of (18) for rows of x."""
    diff = np.atleast_2d(x) - mean
    sol = np.linalg.solve(covariance, diff.T).T
    return np.sqrt(np.einsum("ij,ij->i", diff, sol))


def ensemble_spread(outputs):
    """sigma_ens: sample standard deviation over the ensemble axis (divisor M - 1)."""
    return np.std(np.asarray(outputs), axis=0, ddof=1)


# ---------------------------------------------------------------------------
# Corollary 2 and reporting
# ---------------------------------------------------------------------------
def event_probability(n_blocks, n_b):
    """Union bound of Corollary 2."""
    return 1.0 - n_blocks / (n_b + 1.0)


def clopper_pearson(k, n, confidence=0.95):
    """Two-sided Clopper-Pearson interval for k successes in n trials."""
    a = 1.0 - confidence
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def holm(pvalues):
    """Holm step-down adjusted p values, in the input order."""
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    m = p.size
    adjusted = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adjusted[idx] = min(1.0, running)
    return adjusted


def wilcoxon_min_p(n):
    """Smallest attainable one-sided exact p value of the signed-rank test."""
    return 0.5 ** n
