"""Fig. S4: horizon sensitivity (Table S12)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from _style import BLUE, CA_RED, GRAY, plt  # noqa: E402
from cakmpc_supp import parameters as P  # noqa: E402
from cakmpc_supp import timing as T  # noqa: E402

n_p = [r[0] for r in T.HORIZON]
margin = [r[1] for r in T.HORIZON]
facets = [r[2] for r in T.HORIZON]
p999 = [r[3] for r in T.HORIZON]
rmse = [r[4] for r in T.HORIZON]
x = range(len(n_p))
colors = [CA_RED if n == 12 else GRAY for n in n_p]

fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.1))
ax[0].bar(x, facets, color=colors, width=0.6)
ax[0].set_ylabel(r"Facets of $\mathcal{X}_f$")
ax[0].set_title("(a)", loc="left")
ax[1].bar(x, p999, color=colors, width=0.6)
ax[1].axhline(P.DESIGN["T_qp_dl_us"], color=BLUE, ls="--", lw=0.8)
ax[1].axhline(1000.0, color="k", ls=":", lw=0.8)
ax[1].text(-0.4, P.DESIGN["T_qp_dl_us"] + 20, r"$T^{\mathrm{dl}}_{\mathrm{qp}}$", color=BLUE, fontsize=7)
ax[1].text(-0.35, 1015, r"$T_s$", fontsize=7)
ax[1].set_ylabel(r"Replay p99.9 solve time ($\mu$s)")
ax[1].set_ylim(0, 1200)
ax[1].set_title("(b)", loc="left")
ax[2].bar(x, margin, color=colors, width=0.6)
ax[2].axhline(0, color="k", lw=0.6)
ax[2].set_ylabel(r"$\bar u_{\mathrm{fb}}-\sigma_{N_p-1}$ (A)")
ax2 = ax[2].twinx()
ax2.plot(list(x), rmse, "o-", color=BLUE, ms=3, lw=0.9)
ax2.set_ylabel(r"Simulated RMSE on $R_c$ ($\mu$m)", color=BLUE)
ax2.tick_params(axis="y", colors=BLUE)
ax2.set_ylim(3.0, 5.0)
ax[2].set_title("(c)", loc="left")
for a in ax:
    a.set_xticks(list(x))
    a.set_xticklabels([str(n) for n in n_p])
    a.set_xlabel(r"$N_p$ ($N_c=N_p/2$)")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "figures", "figS4_horizon.png")
fig.savefig(out)
print("wrote", os.path.normpath(out))
