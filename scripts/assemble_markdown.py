"""Concatenate docs/ into one Markdown file for the PDF rendering."""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
ORDER = [
    "S0_nomenclature_and_positioning.md",
    "S-I_joint_and_measurement.md",
    "S-II_lifting_scheduling_calibration.md",
    "S-III_protocol_and_baselines.md",
    "S-IV_certificate.md",
    "S-V_closed_loop_audit.md",
    "S-VI_computation.md",
    "S-VII_score_and_statistics.md",
]
print("---")
print('title: "Supplementary Material"')
print('subtitle: "Confidence-Triggered Koopman Predictive Control With Certified Feasibility for Humanoid Joints Under Operating-Condition Drift"')
print('author: "Anonymous Authors"')
print("---\n")
for name in ORDER:
    with open(os.path.join(ROOT, "docs", name), encoding="utf-8") as f:
        text = f.read()
    text = text.replace("](../figures/", "](figures/")
    text = text.replace("✓", r"$\checkmark$").replace("△", r"$\triangle$")
    text = re.sub(r"(?<=\| )×(?=[¹ ])", r"$\\times$", text)
    text = text.replace("| ×", r"| $\times$")
    text = re.sub(r"!\[(Fig\. S\d)\]\((figures/[^)]+)\)", r"![](\2){width=95%}", text)
    print(text)
    print("\n\\newpage\n")
