import os
import numpy as np
import matplotlib.pyplot as plt

TRAJ_DIR = r"C:\Users\Azul\Desktop\limite de martin\results_phase_sectors\trajectories_crit"
OUT_DIR  = r"C:\Users\Azul\Desktop\limite de martin\results_phase_sectors"
os.makedirs(OUT_DIR, exist_ok=True)

m_targets = [1.95, 2.00, 2.05]
colors = {1.95: "#1f77b4", 2.00: "#2ca02c", 2.05: "#d62728"}

# ======================================================================
# Robust parser for filenames such as:
# traj_m1p95_k0p33_q1p00_d0p01pnpz.npz
# traj_m2p05_k0p33_q1p00_d1p57.npz
# ======================================================================
def parse_fname(fname):
    f = fname.replace(".npz", "").replace("traj_", "")
    parts = f.split("_")

    # m_phi and k_rot are safe
    m = float(parts[0][1:].replace("p", "."))
    k = float(parts[1][1:].replace("p", "."))

    # robust extraction of dphi_ini
    d_raw = parts[3][1:]              # e.g. 0p01pnpz
    d_sections = d_raw.split("p")     # ["0","01","pnpz"] → keep 0 and 01
    if len(d_sections) >= 2:
        d = float(d_sections[0] + "." + d_sections[1])
    else:  # fallback
        d = float(d_raw.replace("p", "."))

    return m, k, d


files = [f for f in os.listdir(TRAJ_DIR) if f.endswith(".npz")]

# ======================================================================
# FIGURE 1 — Phase Trajectories
# ======================================================================
plt.figure(figsize=(6.2, 4.3))
for fname in files:
    m, k, d = parse_fname(fname)
    if round(k, 2) != 0.33:
        continue
    if m in m_targets:
        data = np.load(os.path.join(TRAJ_DIR, fname))
        a = data["a"]
        dphi = data["dphi"]
        plt.plot(a, dphi, linewidth=1.1, alpha=0.55, color=colors[m])

plt.axhline(0, linestyle="--", linewidth=0.7, color="black", alpha=0.6)
plt.axhline(np.pi, linestyle=":", linewidth=0.7, color="black", alpha=0.6)
plt.xlabel(r"$a$")
plt.ylabel(r"$\Delta\phi$")
plt.title(r"Critical Phase Trajectories at $k_{\rm rot}\approx0.33$")
plt.grid(alpha=0.15)
plt.tight_layout()

out1 = os.path.join(OUT_DIR, "crit_trajectories.png")
plt.savefig(out1, dpi=300)
plt.close()

# ======================================================================
# FIGURE 2 — Phase Portrait
# ======================================================================
plt.figure(figsize=(5.8, 4.1))
for fname in files:
    m, k, d = parse_fname(fname)
    if abs(m - 2.00) < 0.03 and round(k, 2) == 0.33:
        data = np.load(os.path.join(TRAJ_DIR, fname))
        plt.plot(data["dphi"], data["dphidot"], linewidth=1.1, alpha=0.55, color="#2ca02c")

plt.axvline(0, linestyle="--", linewidth=0.7, color="black", alpha=0.6)
plt.axvline(np.pi, linestyle=":", linewidth=0.7, color="black", alpha=0.6)
plt.xlabel(r"$\Delta\phi$")
plt.ylabel(r"$d\Delta\phi/dN$")
plt.title(r"Phase Portrait at the Critical Mass")
plt.grid(alpha=0.15)
plt.tight_layout()

out2 = os.path.join(OUT_DIR, "crit_phase_portrait.png")
plt.savefig(out2, dpi=300)
plt.close()

print("\n==============================================")
print("  ✔ CRITICAL FIGURES GENERATED SUCCESSFULLY")
print("==============================================")
print(" →", out1)
print(" →", out2)
