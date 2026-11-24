"""Common figure style (serif fonts, IEEE-like sizes)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.linewidth": 0.6,
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})
CA_RED = "#c0262d"
BLUE = "#1f5fa8"
GREEN = "#2e8b3e"
GRAY = "#6b6b6b"
