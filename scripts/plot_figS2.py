"""Fig. S2: calibration of the composite score.

Requires data/score_calibration.csv with the columns
    set   ('heldout' for the held-out set of Table S8)
    nu    (normalized score nu_k)
The held-out flag rate is plotted against the nominal level alpha, with the
score recalibrated on the second calibration half (column set == 'cal2').
The dashed line of panel (b) is y = alpha, the guarantee of Lemma 4.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from _style import BLUE, CA_RED, plt  # noqa: E402
from cakmpc_supp import conformal as CF  # noqa: E402

path = os.path.join(os.path.dirname(__file__), "..", "data", "score_calibration.csv")
if not os.path.exists(path):
    sys.exit("data/score_calibration.csv not found; see the docstring of this script")
data = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
cal = data["nu"][data["set"] == "cal2"]
held = data["nu"][data["set"] == "heldout"]

fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.2))
ax[0].hist(held, bins=60, range=(0, 2), density=True, color=BLUE, alpha=0.35)
for thr, ls, lab in ((0.9, ":", "enter $M_2$"), (1.0, "-", r"$\nu=1$"), (1.1, ":", "leave $M_2$")):
    ax[0].axvline(thr, color="k" if thr == 1.0 else CA_RED, ls=ls, lw=0.8, label=lab)
ax[0].set_xlabel(r"Normalized score $\nu$")
ax[0].set_ylabel("Density")
ax[0].legend(frameon=False)
alphas = np.linspace(0.01, 0.2, 20)
rates = [np.mean(held * 1.0 > CF.conformal_quantile(cal, a) / CF.conformal_quantile(cal, 0.05)) for a in alphas]
ax[1].plot(alphas, rates, color=CA_RED, lw=1.0, label="held-out flag rate")
ax[1].plot(alphas, alphas, "k--", lw=0.8, label=r"$y=\alpha$ (Lemma 4)")
ax[1].set_xlabel(r"Nominal level $\alpha$")
ax[1].set_ylabel("Held-out flag rate")
ax[1].legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "figS2_score_calibration.png"))
