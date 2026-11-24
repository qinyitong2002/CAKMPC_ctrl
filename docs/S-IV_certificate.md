# S-IV. Offline Design and Certificate Constants

Algorithm S1 summarizes the offline design, and Table S5 lists the constants of the deployed model.

**Algorithm S1. Offline design of the certified predictive layer**

1. Identify $G$ by (7)–(8); apply the spectral scaling.
2. Calibrate $\mathcal W$ by Lemma 2 on 0.37 s blocks; compute $\mathcal D$ and $\bar d$.
3. Solve (11) for $P$, $K_b$, $Q_b$; compute $\lambda$ by (12a).
4. Compute $\mathcal B_\Delta$ (Lemma 3) and $\mathcal E_i$, $\mathcal C_i$, $\sigma_i$ by (12b); verify that the bounds in (13d)–(13e) and (14b)–(14c) are positive.
5. Compute $\mathcal X_f$ satisfying (14) by backward recursion on the 16 vertex models.
6. Compute $\Omega_{\mathrm{in}}\subset\Omega_2\subset\Omega_b$, verify Condition 1, and compute $J_b$.
7. Verify that the projections of $\mathcal X_f$ and $\Omega_b$, enlarged by $\bar r_e$ and $q_w\hat w_{1:2}$, lie in $\mathcal E_{\mathrm{op}}$ (Remark 2).
8. Store the slacks of (14), $\mathcal W$, $\bar d$, and $\mathcal B_\Delta$ for test (A4).

### Table S5. Constants of the Certificate (Deployed Model)

| Quantity | Symbol | Value |
|---|---|---|
| ***Residual set (Lemma 2)*** | | |
| Calibration / held-out blocks (0.37 s) | $n_b$ / — | 559 / 279 |
| Quantile / level | $q_w$ / $1/(n_b+1)$ | 1.0067 / $1.79\times10^{-3}$ |
| Held-out coverage | — | 279 of 279 blocks |
| Half-widths, error coordinates 1–8 | $q_w\hat w_{1:8}$ | 0.0294, 0.0091, 0.0303, 0.0017, 0.0148, 0.0032, 0.0062, 0.0147 |
| Half-widths, context coordinates 9–17 | $q_w\hat w_{9:17}$ | 0.863, 0.558, 0.039, 0.040, 0.025, 0.120, 0.026, 0.867, 0.699 |
| Largest error-block residual | $\max\lVert w^e\rVert$ | 0.0485 |
| ***Model and terminal ingredients*** | | |
| Contraction factor / largest vertex spectral radius | $\lambda$ / $\max_v\rho(A_{\mathrm{cl},v})$ | 0.9901 / 0.9802 |
| Feedback-gain norm | $\lVert K_b\rVert$ | 36.25 |
| Scheduling rate / coupling bound | $\bar\Delta_{\vartheta,j}$ / $\bar d$ | 1.400 ($j=1,2,3$) / 0.0468 |
| Coupling norms | $\lVert A_{ce}\rVert_F$ / $\lVert B_c\rVert$ / $\lVert A_{ec}\rVert_F$ | 3.98 / 0.0244 / 0.44 |
| Margins (A) | $\sigma_1,\sigma_6,\sigma_8,\sigma_{11}$ | 1.462, 5.395, 6.086, 7.068 |
| Margins (A) | $\sigma_{12},\sigma_{14},\sigma_{15}$ | 7.368, 7.908, 8.147 |
| Facets of $\mathcal X_f$ / $\Omega_b$ | — | 616 / 340 |
| Backward-recursion steps | $j^\ast$ | 307 |
| QP inequality rows without / with $\mathcal X_f$ | — | 30 / 646 |
| Tightened amplitude / slew bounds (A) | $\bar u_{\mathrm{fb}}-\sigma_{N_p-1}$ / $\bar\rho-\sigma_{N_p}-\sigma_{N_p-1}$ | 10.93 / 4.12 |
| ***Self-consistency of Assumption 3 (Remark 2)*** | | |
| $\mathcal X_f$, enlarged by $\bar r_e$ and $q_w\hat w_{1:2}$ | $\max\lvert e_1\rvert/\bar e_1$, $\max\lvert e_2\rvert/\bar e_2$ | 0.06, 0.03 |
| $\Omega_b$, enlarged likewise | $\max\lvert e_1\rvert/\bar e_1$, $\max\lvert e_2\rvert/\bar e_2$ | 0.14, 0.12 |
| ***Bound constants (Theorems 1 and 2)*** | | |
| Terminal term of $\gamma_f$ | $\lambda_{\max}(R)(\bar\rho-\sigma_{N_p}-\sigma_{N_p-1})^2$ | 33.9 |
| Constants | $\kappa$ / $a_2$ / $c_0$ / $J_b$ | $3.1\times10^4$ / 1 / $5.1\times10^4$ / $3.4\times10^4$ |
| Bound (24) | $c_0+a_2\kappa$; as $\lvert e_1\rvert$ | $8.2\times10^4$; 889 µm |
| Bound (25), $R_1$ ($m=2$) | $\bar J_m$; as $\lvert e_1\rvert$ | $2.06\times10^5$; 1.41 mm |
| Bound (25), $R_c$ ($m=4$) | $\bar J_m$; as $\lvert e_1\rvert$ | $3.30\times10^5$; 1.78 mm |
| Bound (25), $R_2$ ($m=11$) | $\bar J_m$; as $\lvert e_1\rvert$ | $7.64\times10^5$; 2.71 mm |
| ***Input budgets*** | | |
| Current limit / feedforward bound / feedback budget (A) | $\bar u$ / $\bar u_{\mathrm{ff}}$ / $\bar u_{\mathrm{fb}}$ | 60 / 39.21 / 18 |
| Slew limit (A per sample) | $\bar\rho$ | 18.56 |
| ***Confidence score (Lemma 4)*** | | |
| Level / calibration size / quantile | $\alpha$ / $n$ / $q_\nu$ | 0.05 / 48 866 / 1.4222 |
| Exceedance, calibration / held-out | — | 4.997 % / 4.20 % |

Half-widths and residual norms are given in the normalized lifted coordinates of Section S-II; $m$ is the longest observed run of consecutive fallback cycles (Table S11). Source: `cakmpc_supp/certificate.py`, `tables/tableS5_certificate_constants.csv`; `scripts/run_checks.py` recomputes the derived entries.

## Certificate checks

(i) *Coverage:* all 279 held-out blocks lie in $\mathcal W$. (ii) *Positivity of the tightened bounds:* $\bar u_{\mathrm{fb}}-\sigma_{N_p-1}=10.93$ A and $\bar\rho-\sigma_{N_p}-\sigma_{N_p-1}=4.12$ A, so that (13d), (13e), (14b), and (14c) leave nonempty admissible ranges. (iii) *Coupling:* $A_{ce}$ and $B_c$ enter the certificate through $\bar\delta_c$ in (22c) alone. (iv) *Current budget:* $\bar u_{\mathrm{ff}}+\bar u_{\mathrm{fb}}=57.21\ \mathrm A\le\bar u=60$ A, so that the transmitted current never saturates. (v) *Operating set:* the certified sets and all admitted predictions remain in $\mathcal E_{\mathrm{op}}$ with a ratio of at most 0.14 (Remark 2).

## Margins

Each $\mathcal E_i$ is a symmetric polytope obtained from the images of $\mathcal E_{i-1}$ under the 16 vertex closed-loop matrices and from the box $\mathcal B_\Delta$; each increment $\sigma_{i+1}-\sigma_i=h_{\mathcal E_i}(K_b^\top)$ is the value of one linear program over the vertices of $\mathcal E_i$. Because $\mathcal W^e$ is a box, $\sigma_1=h_{\mathcal W^e}(K_b^\top)=\sum_{j=1}^8\lvert K_{b,j}\rvert q_w\hat w_j$, the same quantity that tightens the admission test (20)(iii).

## Coupling bound

$\bar d$ is attained at a pair of vertices of $\Theta$ and $\mathcal Z^c$ ($16\times2^9$ evaluations), because $\lVert A_{ec}(\vartheta)c\rVert_P$ is convex in each argument.

## Context-prediction change $\bar\delta_c$

$\eta_i:=\tilde z^c_{i\mid k+1}-z^c_{i+1\mid k}$ obeys $\eta_0=w^c_k$ and $\eta_{i+1}=A_{cc}(\hat\vartheta')\eta_i+(A_{ce}(\hat\vartheta')+B_c(\hat\vartheta')K_b)\epsilon_i+\Delta^c_i$. The vector $\bar\delta_c$ is the elementwise smaller of the extent of $\mathcal Z^c$ and the bound obtained by propagating this recursion over $N_p$ steps with $\epsilon_i\in\mathcal E_i$; it vanishes in the previewed coordinates $s_v$ and $\bar a$, which both predictions take from the same preview. The context feedback $A_{ce}$, $B_c$ enters the certificate through this bound alone.

## Lipschitz constant $L_J$

With predictions and inputs stacked in $y$, (13a) is $y^\top Hy$ and $\lvert q(y+\delta)-q(y)\rvert\le\lVert H\rVert(2\bar y+\lVert\delta\rVert)\lVert\delta\rVert$ for $\lVert y\rVert\le\bar y$; $\lVert\delta\rVert$ is bounded through $\epsilon_i\in\mathcal E_i$ and $\lvert K_b\epsilon_i\rvert\le\sigma_{i+1}-\sigma_i$.

## Constants $a_2$, $c_0$, and $J_b$

With $J_{\max}$ the largest value of (13a) over the feasible set and $e_s>0$, $J^\star_k\le J_{\max}\le(J_{\max}/(\lambda_{\min}(Q_e)e_s^2))\lVert e_k\rVert^2_{Q_e}$ if $\lVert e_k\rVert\ge e_s$, and $J^\star_k\le c_0(e_s)$ otherwise; hence $a_2:=\max\{1,J_{\max}/(\lambda_{\min}(Q_e)e_s^2)\}$ and $c_0:=c_0(e_s)$, with $e_s$ minimizing (24). Using $\lVert z^e_{i\mid k}\rVert_P\le\lambda^i\lVert x\rVert_P+\bar d(1-\lambda^i)/(1-\lambda)$ and $Q_b\preceq P$, $c_0$ is of order $N_p\bar d^2/(1-\lambda)^2$ and vanishes as $\bar d\to0$. $J_b$ is the maximum of (13a) under the backup sequence over $\Omega_b$, the previews, and $\mathcal Z^c$, attained at vertices. For the deployed design, the terminal term of $\gamma_f$ uses the tightened slew bound of (14c), which reduces it from $\lambda_{\max}(R)\bar\rho^2\approx689$ to 33.9. The bounds expressed in micrometers in Table S5 lie two orders of magnitude above the measured errors; they establish robustness with respect to the residual, the scheduling rate, and the context coupling rather than predict the achieved accuracy.

## Inexact solutions

The analysis of Section V presumes exact solutions of (13). The deployed solver stops on an iterate tolerance of 1 mA or at its iteration cap, and on the bench 0.42 %–0.56 % of the optimizer cycles returned iterates whose constraint residuals reached at most 0.6 A (Table S11); $\Pi_k$ and the final limit check kept every transmitted command within the amplitude and slew limits. Tightening (13d) and (13e) by this residual leaves margins of 10.33 A and 3.52 A, so that a design that accounts for the solver tolerance remains feasible.
