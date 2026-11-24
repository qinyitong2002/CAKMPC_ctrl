"""Table S1 - features of the proposed scheme and its nearest neighbors."""

CRITERIA = {
    "a": ("condition-dependent predictor",
          "the prediction model changes with a measured operating condition"),
    "b": ("one convex QP per cycle",
          "the online problem is a single convex quadratic program"),
    "c": ("certificate valid while the condition changes",
          "recursive feasibility is proved for time-varying conditions in a known set"),
    "d": ("certificate kept under online updates",
          "the certificate is shown to hold after the model is replaced online"),
    "e": ("computation allocated by model confidence",
          "whether the optimization is solved depends on a measure of model reliability"),
    "f": ("command guaranteed in every period",
          "an admissible command is available in every sampling period by construction"),
    "g": ("hardware validation", "closed-loop experiments on physical hardware"),
}

# entries: 'yes', 'partly', 'no', 'n/a'; notes refer to numbered footnotes
ROWS = [
    ("Koopman MPC, fixed lift [7], [20]", "no yes no no no no partly", ""),
    ("Koopman tube MPC [11]", "no yes partly no no no no", ""),
    ("Bilinear Koopman MPC [23], [24]", "yes no no no no no yes", ""),
    ("LPV-MPC, polytopic tubes [12]", "yes yes yes no no no no", "d: online updates not considered"),
    ("Robust event-triggered MPC [33]", "no yes yes no partly no no", "e: state-threshold trigger"),
    ("Approximate MPC [31]", "no n/a partly no no yes no", "f: explicit evaluation in bounded time"),
    ("Physics-based NMPC [47]", "yes no no no no partly yes", ""),
    ("Proposed", "yes yes yes yes yes yes yes",
     "c, d: on the event of Corollary 2; f: under the timing condition of Corollary 1"),
]
