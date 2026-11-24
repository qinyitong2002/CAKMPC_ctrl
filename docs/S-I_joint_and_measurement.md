# S-I. Joint Parameters and Measurement Chain

## Identified parameters

Table S2 lists the parameters of model (1)–(2). Bidirectional friction sweeps separate the force–current gain, the breakaway friction, and a rig bias removed in preprocessing; D-optimal excitation sets the intervals. Source: `cakmpc_supp/parameters.py`, `tables/tableS2_joint_parameters.csv`.

### Table S2. Measured and Verified Parameters of the Joint

| Quantity | Symbol (unit) | Value | Rel. 95 % CRB (%)¹ |
|---|---|---|---|
| Rated axial force | $F_{\mathrm{rated}}$ (kN) | 6.5 | design |
| Translational mass | $M$ (kg) | 33.6 | 2.6 |
| Joint viscous sum | $B_v+\sigma_2$ (N·s/m) | 1779 | 8.5 |
| Translational time constant | $\tau_{\mathrm{sys}}$ (ms) | 18.9 | derived |
| Force–current gain | $K_f$ (N/A) | 109.5 | 1.3 |
| Coulomb friction, zero load | $F_c(0)$ (N) | 120 | 1.6 |
| Static friction, zero load | $F_s(0)$ (N) | 158.3 | 2.5 |
| Stribeck minimum velocity | $v_s^{\min}$ (mm/s) | 0.23 | 1.6 |
| Stribeck saturation knee | $F_N^\ast$ (N) | 512 | 8.6 |
| Stribeck saturation shift | $\Delta v_s$ (mm/s) | 4.393 | 1.6 |
| Load coupling | $(\alpha_{F1},\alpha_{F2})$ | (1.80, 0.111) | (2.8, 2.5) |
| Direction bias (constant) | $F_{g,\mathrm{const}}$ (N) | 107 | 15.9 |
| Force-path lost motion | $\delta(F)$ (µm) | 255 | fit $R^2=0.9998$ |
| Series contact stiffness | $\sigma_0$ (N/m) | $1.75\times10^7$ | 10 |
| Contact damping | $\sigma_1$ (N·s/m) | 150 | prior |
| Thermal coupling | $\alpha_T$ (1/°C) | 0.0145 | 2.8 |
| Torque constant | $K_t$ (N·m/A) | 0.0901 | calib. |
| Reference contact force | $F_{N0}$ (N) | 1000 | design |

¹ $1.96\sigma$ divided by the estimate; "derived", "prior", "calib.", and "design": not estimated from the identification data.

## Direction bias

The direction bias $F_{g,\mathrm{const}}$ has the widest interval in Table S2. In simulation with the model of Table S2, a change of $\pm15.9\,\%$ ($\pm17$ N) changes the RMSE within $\pm20$ ms of the reversals by 4.13 µm when the direction channel $s_v$ is part of the scheduling vector and by 27.38 µm when it is removed. The direction channel thus carries most of the bias in the transition matrices, and the remainder enters the residual calibrated in $\mathcal W$ (Section S-II).

## Measurement chain

The tracking error $e_1$ is the screw-side error of $x$, measured by the motor encoder. The laser displacement sensor observes the output position $x_{\mathrm{out}}$ for monitoring and is not used by any controller. Every signal is acquired in the same 1 kHz EtherCAT cycle (Fig. S3).

### Table S6. Measurement Chain

| Signal | Sensor | Use | Resolution / noise | Acquisition |
|---|---|---|---|---|
| Screw-side position $x$; error $e_1$ | motor encoder, 17 bit, 6 mm lead | tracking error and feedback of all controllers | 0.046 µm per count; noise SD 0.31 µm on stationary segments | drive, EtherCAT |
| Axial load $F_{\mathrm{ext}}$ | NS-WL5 load cell, ±20 kN | scheduling ($\bar F_{\mathrm{ext}},\bar F_N$); low-pass filtered estimate $\hat F$ for the clearance compensation $x_{\mathrm{ref}}\leftarrow x_{\mathrm{ref}}-\hat\delta(\hat F)$ | — | analog input of the I/O module |
| Housing temperature $T$ | WZPT-035 PT100 | scheduling ($\bar T$) and feedforward | — | I/O module |
| Output position $x_{\mathrm{out}}$ | PDM-120S-A laser displacement sensor | monitoring; not used by any controller | — | I/O module |
| Phase current | CTC-100 current sensor | auxiliary monitoring; not used by any controller | — | I/O module |

Source: `cakmpc_supp/audits.py`, `tables/tableS6_measurement_chain.csv`.
