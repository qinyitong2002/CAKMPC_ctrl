"""Constants of the certificate of the deployed model (Table S5)."""

import math

from . import parameters as P

# ---------------------------------------------------------------------------
# Residual set (Lemma 2)
# ---------------------------------------------------------------------------
N_B = 559                       # calibration blocks of 0.37 s
N_HELDOUT_BLOCKS = 279
BLOCK_LENGTH_S = 0.37
Q_W = 1.0067
HELDOUT_COVERAGE = (279, 279)
HALF_WIDTHS_ERROR = (0.0294, 0.0091, 0.0303, 0.0017, 0.0148, 0.0032, 0.0062, 0.0147)
HALF_WIDTHS_CONTEXT = (0.863, 0.558, 0.039, 0.040, 0.025, 0.120, 0.026, 0.867, 0.699)
MAX_ERROR_BLOCK_RESIDUAL = 0.0485

# ---------------------------------------------------------------------------
# Model and terminal ingredients
# ---------------------------------------------------------------------------
LAMBDA = 0.9901
MAX_VERTEX_SPECTRAL_RADIUS = 0.9802
K_B_NORM = 36.25
RATE_BOUND = 1.400
D_BAR = 0.0468
A_CE_FRO = 3.98
B_C_NORM = 0.0244
A_EC_FRO = 0.44
SIGMA = {1: 1.462, 6: 5.395, 8: 6.086, 11: 7.068, 12: 7.368, 14: 7.908, 15: 8.147}
X_F_FACETS = 616
OMEGA_B_FACETS = 340
BACKWARD_RECURSION_STEPS = 307
QP_ROWS_WITHOUT_XF = 30
QP_ROWS_WITH_XF = 646
AMPLITUDE_MARGIN_A = 10.93      # u_bar_fb - sigma_{Np-1}
SLEW_MARGIN_A = 4.12            # rho_bar - sigma_{Np} - sigma_{Np-1}

# ---------------------------------------------------------------------------
# Confidence score (Lemma 4)
# ---------------------------------------------------------------------------
ALPHA = 0.05
N_SCORE_CAL = 48866
Q_NU = 1.4222
EXCEEDANCE_CALIBRATION = 2442 / 48866      # 4.997 %
EXCEEDANCE_HELDOUT = 47 / 1120             # 4.20 %

# ---------------------------------------------------------------------------
# Bound constants (Theorems 1 and 2)
# ---------------------------------------------------------------------------
KAPPA = 3.1e4
A2 = 1.0
C0 = 5.1e4
J_B = 3.4e4
E1_BOUND_24_UM = 889.0          # (24) expressed as a bound on |e1|
OBSERVED_FALLBACK_RUNS = {"R1": 2, "Rc": 4, "R2": 11}

# ---------------------------------------------------------------------------
# Self-consistency of Assumption 3: max |e_i| / e_bar_i over the certified
# sets, enlarged by r_bar_e and q_w w_hat_{1:2} (four LPs per set)
# ---------------------------------------------------------------------------
INCLUSION = {
    "X_f": {"e1": 0.06, "e2": 0.03},
    "Omega_b": {"e1": 0.14, "e2": 0.12},
}

# ---------------------------------------------------------------------------
# Numerical residual of the deployed solver (Section VI-C)
# ---------------------------------------------------------------------------
SOLVER_RESIDUAL_MAX_A = 0.6


def gamma_f_terminal_term(slew):
    """Terminal term lambda_max(R) * slew^2 of gamma_f."""
    return P.DESIGN["R"] * slew ** 2


def j_bar(m, c0=C0, a2=A2, kappa=KAPPA, j_b=J_B):
    """Ultimate bound (25) of Theorem 2 for a longest fallback run m."""
    return max(c0 + a2 * (m + 1) * kappa, j_b + m * kappa) + m * kappa


def bound_24():
    """Right-hand side c0 + a2 kappa of the limit in (24)."""
    return C0 + A2 * KAPPA


def e1_bound_um(bound):
    """Express a bound on ||e||_Qe^2 as a bound on |e1| in micrometers.

    The conversion |e1| <= s1 (bound / lambda_min(Q_e))^(1/2) scales with the
    square root of the bound; it is anchored at the value reported for (24).
    """
    return E1_BOUND_24_UM * math.sqrt(bound / bound_24())


def event_probability(n_blocks, n_b=N_B):
    """Corollary 2: probability of the certified event over n_blocks blocks."""
    return 1.0 - n_blocks / (n_b + 1.0)


def blocks_in(duration_s):
    return math.ceil(duration_s / BLOCK_LENGTH_S)
