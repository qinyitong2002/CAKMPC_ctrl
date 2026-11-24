# S-V. Closed-Loop Audit of the Residual Set

Lemma 2 calibrates $\mathcal W$ on identification trajectories, whereas Theorems 1 and 2 concern the closed loop, in which the feedback, the policy, and the trigger shape the distribution of the residuals. The one-step residuals $w_k=z_{k+1}-A(\vartheta_k)z_k-B(\vartheta_k)u_k$ were therefore recomputed from the bench logs, re-evaluating the lifting on the logged signals with the deployed model (in $R_3$, the model valid at each instant), normalized as in Section S-II, and cut into 0.37 s blocks. Table S10 reports, for each regime, the blocks whose score exceeds $q_w$ and the cycles in which a coordinate leaves $\mathcal W$, separately for the error coordinates 1–8 and the context coordinates 9–17.

### Table S10. Closed-Loop Residual Audit

| Regime | Trials | Blocks | Blocks outside $\mathcal W$ | Rate (95 % CI) | Cycles | Cycles outside, coord. 1–8 | Cycles outside, coord. 9–17 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| $R_1$ | 8 | 544 | 0 | 0 % (0–0.68 %) | 200 000 | 0 | 0 |
| $R_c$ | 8 | 544 | 1 | 0.18 % (0.005–1.02 %) | 200 000 | 26 | 0 |
| $R_2$ | 8 | 2600 | 5 | 0.19 % (0.06–0.45 %) | 960 000 | 524 | 622 |
| $R_3$ | 5 | 1625 | 2 | 0.12 % (0.015–0.44 %) | 600 000 | 334 | 465 |
| All certified regimes | 29 | 5313 | 8 | 0.15 % | 1 960 000 | 884 | 1087 |
| $R_c$, 20 % controller-side mismatch¹ | 20 | 1360 | 1 | 0.07 % (0.002–0.41 %) | 500 000 | 65 | 227 |

¹ Outside the certified regime: the perturbed feedforward acts on the plant as an unmodeled input, so that Assumption 2 need not hold; reported for reference.

The calibrated level is $1/(n_b+1)=0.18\,\%$ per block. In every regime the closed-loop rate is compatible with this level, and the lower confidence limits lie below it; across the certified regimes, 8 of 5313 blocks (0.15 %) left $\mathcal W$. Excursions occur in both coordinate groups under load steps ($R_2$) and heating ($R_3$). The 279 held-out blocks of Table S5 are consistent with Lemma 2 but cannot by themselves distinguish a level of $1.79\times10^{-3}$ from one of order $10^{-2}$; the audit adds 5313 closed-loop blocks to that evidence. The union bound of Corollary 2 ignores the dependence between blocks and is conservative relative to these rates.

Source: `cakmpc_supp/audits.py`, `tables/tableS10_closed_loop_audit.csv`; the confidence intervals are recomputed by `scripts/run_checks.py`.
