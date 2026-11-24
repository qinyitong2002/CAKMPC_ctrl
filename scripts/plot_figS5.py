"""Fig. S5: latency stages on R1, triggered operation with the complete test (Table S11)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from _style import BLUE, CA_RED, GRAY, plt  # noqa: E402
from cakmpc_supp import parameters as P  # noqa: E402
from cakmpc_supp import timing as T  # noqa: E402

labels = ["input transfer", "lifting and score", "admission test (20)",
          "QP (optimizer cycles, completed)", "output transfer", "non-computational overhead"]
mean = [T.STAGES[k][0] for k in labels]
p999 = [T.STAGES[k][1] for k in labels]
mx = [T.STAGES[k][2] for k in labels]
colors = [GRAY, GRAY, BLUE, CA_RED, GRAY, "k"]

fig, ax = plt.subplots(figsize=(4.8, 2.2))
y = list(range(len(labels)))[::-1]
ax.barh(y, mean, color=colors, height=0.55, label="mean")
ax.scatter(p999, y, marker="|", s=90, color="k", zorder=3, label="p99.9")
ax.scatter(mx, y, marker="x", s=14, color="k", zorder=3, label="max")
ax.axvline(P.DESIGN["T_qp_dl_us"], color=BLUE, ls="--", lw=0.8)
ax.text(P.DESIGN["T_qp_dl_us"] + 8, 5.2, r"$T^{\mathrm{dl}}_{\mathrm{qp}}$", color=BLUE, fontsize=7)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlabel(r"Time per cycle ($\mu$s)")
ax.set_xlim(0, 720)
ax.legend(loc="upper right", bbox_to_anchor=(0.86, 1.0), frameon=False)
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "figures", "figS5_latency_stages.png")
fig.savefig(out)
print("wrote", os.path.normpath(out))
