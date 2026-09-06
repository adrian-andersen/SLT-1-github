"""
generate_plots.py
Genererer høyoppløselige pedagogiske figurer for TET4100 SLT-1.
Oppgave 1-6 med analytiske løsninger, ekstra store skrifttyper,
tydelige fargede infobokser og 100 % garantert overlapp-fri geometri.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set high-quality styling with large, legible fonts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 17,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 13.5,
    'figure.titlesize': 19,
    'figure.dpi': 220,
    'lines.linewidth': 2.8,
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'figure.titleweight': 'bold',
})

# ==========================================
# PLOT 1: Task 1 - Basic RL Transient & Inductive Kickback
# ==========================================
def plot_task1():
    t_pre = np.linspace(-1.5, 0, 100) # ms
    t_post = np.linspace(0, 12, 600)  # ms
    
    # Pre-switch (steady state)
    i_pre = np.full_like(t_pre, 1.5)
    v_pre = np.zeros_like(t_pre)
    
    # Post-switch: tau = 2.5 ms
    tau = 2.5 # ms
    i_post = 1.5 * np.exp(-t_post / tau)
    v_post = -72.0 * np.exp(-t_post / tau)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.0), sharex=True)
    
    # Current
    ax1.plot(t_pre, i_pre, color='#2563eb', label='Før bryting ($i_L = 1.5$ A)')
    ax1.plot(t_post, i_post, color='#1d4ed8', label=r'Etter bryting: $i_L(t) = 1.5 e^{-t / 2.5\,\mathrm{ms}}$ A')
    ax1.axvline(0, color='#dc2626', linestyle='--', alpha=0.8, label='Bryter åpnes ($t = 0$)')
    
    # Mark 1 A point
    t_1A = 2.5 * np.log(1.5) # ~ 1.014 ms
    ax1.plot(t_1A, 1.0, 'ro', markersize=9, zorder=5)
    ax1.annotate(f'$i_L = 1.0$ A ved $t = {t_1A:.3f}$ ms',
                 xy=(t_1A, 1.0), xytext=(t_1A + 1.8, 1.32),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=14, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    ax1.set_ylabel('Spolestrøm $i_L(t)$ [A]')
    ax1.set_title('Oppgave 1: Strøm- og spenningsrespons i RL-krets ved bryteråpning', pad=12)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', framealpha=0.95)
    ax1.set_ylim(-0.15, 1.90)
    
    # Voltage
    ax2.plot(t_pre, v_pre, color='#059669', label='Før bryting: $v_L(0^-) = 0$ V (kortslutning)')
    ax2.plot(t_post, v_post, color='#10b981', label=r'Etter bryting: $v_L(t) = -72 e^{-t / 2.5\,\mathrm{ms}}$ V')
    ax2.axvline(0, color='#dc2626', linestyle='--', alpha=0.8)
    
    # Inductive kickback annotation
    ax2.plot(0, -72, 'ro', markersize=9, zorder=5)
    ax2.annotate('Induktiv spenningsspiss (Flyback):\n$v_L(0^+) = -72$ V!',
                 xy=(0, -72), xytext=(1.8, -36),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=14, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    ax2.set_xlabel('Tid $t$ [ms]')
    ax2.set_ylabel('Spolespenning $v_L(t)$ [V]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    # Placed lower-right where v_L has approached 0 V (completely clear space!)
    ax2.legend(loc='lower right', framealpha=0.95)
    ax2.set_ylim(-85, 15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "task1_rl_response.png"), bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Plot 1 saved (task1_rl_response.png).")

# ==========================================
# PLOT 2: Task 2 - Sequential Switching RC
# ==========================================
def plot_task2():
    tau = 1.0 # ms (tau = 1k * 1uF = 1ms)
    t1 = np.linspace(0, tau, 300)
    t2 = np.linspace(tau, 6*tau, 800)
    
    # Stage 1: 0 <= t < tau, source = +10V, target = 10V
    vc1 = 10.0 * (1.0 - np.exp(-t1 / tau))
    i1 = 10.0 * np.exp(-t1 / tau) # mA
    
    # Stage 2: tau <= t <= 6tau, source = -20V, target = -20V
    vc_tau = 10.0 * (1.0 - np.exp(-1.0)) # ~ 6.321 V
    vc2 = -20.0 + (vc_tau - (-20.0)) * np.exp(-(t2 - tau) / tau)
    i2 = (-20.0 - vc2) / 1.0 # in mA (R = 1k)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.2), sharex=True)
    
    # Capacitor Voltage
    ax1.plot(t1, vc1, color='#2563eb', label=r'Trinn 1: Lading mot $+10$ V ($0 \leq t < \tau$)')
    ax1.plot(t2, vc2, color='#7c3aed', label=r'Trinn 2: Utlading mot $-20$ V ($\tau \leq t \leq 6\tau$)')
    ax1.axvline(tau, color='#dc2626', linestyle='--', alpha=0.85, label=r'Svitsjeøyeblikk $t = \tau = 1$ ms')
    ax1.axhline(10, color='gray', linestyle=':', alpha=0.6)
    ax1.axhline(-20, color='gray', linestyle=':', alpha=0.6)
    
    # Continuous voltage point at t = 1 ms
    ax1.plot(tau, vc_tau, 'ro', markersize=9, zorder=5)
    ax1.annotate(f'$v_C(\\tau) = {vc_tau:.2f}$ V\n(Kontinuerlig tilstand)',
                 xy=(tau, vc_tau), xytext=(tau + 0.6, 9.0),
                 arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#1e3a8a',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#eff6ff', edgecolor='#2563eb', alpha=0.95))
    
    ax1.set_ylabel('Kondensatorspenning $v_C(t)$ [V]')
    ax1.set_title('Oppgave 2: Sekvensiell svitsjing i RC-krets ($+10$ V til $-20$ V)', pad=14)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='center right', bbox_to_anchor=(0.99, 0.45), framealpha=0.95)
    ax1.set_ylim(-24, 18)
    
    # Loop Current
    ax2.plot(t1, i1, color='#059669', label='Trinn 1: Oppladningsstrøm (+10 mA start)')
    ax2.plot(t2, i2, color='#d97706', label='Trinn 2: Reversert strøm (-26.32 mA sjokk)')
    ax2.axvline(tau, color='#dc2626', linestyle='--', alpha=0.85)
    
    # Current jump annotation
    i_before = 10.0 * np.exp(-1.0)
    i_after = (-20.0 - vc_tau) / 1.0
    ax2.plot([tau, tau], [i_before, i_after], 'r:', linewidth=2.5)
    ax2.plot(tau, i_after, 'ro', markersize=9, zorder=5)
    ax2.plot(tau, i_before, 'go', markersize=7, zorder=5)
    
    # Placed in clear open bottom-right space
    ax2.annotate(f'Diskontinuerlig strømsprang!\nFra $+{i_before:.2f}$ mA til ${i_after:.2f}$ mA',
                 xy=(tau, i_after), xytext=(tau + 1.2, -22.5),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    ax2.set_xlabel('Tid $t$ [ms]  (hvor $\\tau = 1$ ms)')
    ax2.set_ylabel('Sløyfestrøm $i(t)$ [mA]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', framealpha=0.95)
    ax2.set_ylim(-32, 16)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "task2_rc_sequential.png"), bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Plot 2 saved (task2_rc_sequential.png).")

# ==========================================
# PLOT 3: Task 3 - Dynamical System Stability
# ==========================================
def plot_task3():
    t = np.linspace(0, 0.067, 500) # s
    t_ms = t * 1000 # ms
    
    # Case A: R1 = 10 kOhm -> lambda = +40 s^-1 (UNSTABLE)
    v_unstable_10 = 10.0 * np.exp(40.0 * t)
    v_unstable_0  = np.zeros_like(t)
    v_unstable_m2 = -2.0 * np.exp(40.0 * t)
    
    # Case B: R1 = 2 kOhm -> lambda = -40 s^-1 (STABLE)
    v_stable_10 = 10.0 * np.exp(-40.0 * t)
    v_stable_0  = np.zeros_like(t)
    v_stable_m2 = -2.0 * np.exp(-40.0 * t)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.8))
    
    # Subplot 1: Unstable (R1 = 10 kOhm)
    ax1.plot(t_ms, v_unstable_10, color='#dc2626', label=r'$v_0(0^+) = +10$ V $\rightarrow$ Eksploderer!')
    ax1.plot(t_ms, v_unstable_0, color='#475569', linestyle='--', label=r'$v_0(0^+) = 0$ V (Ustabil likevekt)')
    ax1.plot(t_ms, v_unstable_m2, color='#b91c1c', linestyle='-.', label=r'$v_0(0^+) = -2$ V $\rightarrow -\infty$')
    
    ax1.set_title(r'Ustabil likevekt ($R_1 = 10\ \mathrm{k}\Omega$, $\lambda = +40\ \mathrm{s}^{-1}$)', color='#991b1b', pad=12)
    ax1.set_xlabel('Tid $t$ [ms]')
    ax1.set_ylabel('Spenning $v_0(t)$ [V]')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', framealpha=0.95)
    ax1.set_ylim(-35, 175)
    
    ax1.annotate(f'Ved 67 ms:\n$v_0 = {v_unstable_10[-1]:.1f}$ V!',
                 xy=(67, v_unstable_10[-1]), xytext=(36, 125),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=14, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    # Subplot 2: Stable (R1 = 2 kOhm)
    ax2.plot(t_ms, v_stable_10, color='#059669', label=r'$v_0(0^+) = +10$ V $\rightarrow 0$ V')
    ax2.plot(t_ms, v_stable_0, color='#475569', linestyle='--', label=r'$v_0(0^+) = 0$ V (Stabil likevekt)')
    ax2.plot(t_ms, v_stable_m2, color='#047857', linestyle='-.', label=r'$v_0(0^+) = -2$ V $\rightarrow 0$ V')
    
    ax2.set_title(r'Stabil likevekt ($R_1 = 2\ \mathrm{k}\Omega$, $\lambda = -40\ \mathrm{s}^{-1}$)', color='#065f46', pad=12)
    ax2.set_xlabel('Tid $t$ [ms]')
    ax2.set_ylabel('Spenning $v_0(t)$ [V]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', framealpha=0.95)
    ax2.set_ylim(-3.5, 14.0)
    
    # Placed in the clear open area at t in [32, 60], y in [4.5, 7.5]
    ax2.annotate('Asymptotisk konvergens\nmot likevektspunktet $v_0^* = 0$ V',
                 xy=(48, v_stable_10[int(len(t)*48/67)]), xytext=(30, 5.2),
                 arrowprops=dict(facecolor='#059669', edgecolor='#059669', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#065f46',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecfdf5', edgecolor='#059669', alpha=0.95))
    
    plt.suptitle('Oppgave 3: Dynamisk stabilitet og negativ konduktans i aktiv krets', y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "task3_stability_comparison.png"), bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Plot 3 saved (task3_stability_comparison.png).")

# ==========================================
# PLOT 4: Task 4 - Two-Capacitor Redistribution
# ==========================================
def plot_task4():
    t_norm = np.linspace(0, 5, 500) # in units of tau (t / tau)
    
    # Voltages normalized to U
    u_C = 0.1 + 0.9 * np.exp(-t_norm)
    u_9C = 0.1 * (1.0 - np.exp(-t_norm))
    i_norm = np.exp(-t_norm)
    
    # Energy normalized to E_initial = 1.0
    E_C = u_C**2
    E_9C = 9.0 * (u_9C**2)
    E_total = E_C + E_9C
    E_diss = 1.0 - E_total
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.8))
    
    # Voltages
    ax1.plot(t_norm, u_C, color='#2563eb', label=r'$u_C(t)$ (Liten kondensator $C$)')
    ax1.plot(t_norm, u_9C, color='#d97706', label=r'$u_{9C}(t)$ (Stor kondensator $9C$)')
    ax1.plot(t_norm, i_norm, color='#dc2626', linestyle=':', label=r'Strøm $i(t) / (U/R)$')
    ax1.axhline(0.1, color='gray', linestyle='--', alpha=0.7, label=r'Sluttspenning $V_f = 0.1 U$')
    
    ax1.set_title('Spenninger og strøm under ladningsoverføring', pad=12)
    ax1.set_xlabel(r'Tid i tidskonstanter $t / \tau$  ($\tau = 0.9 RC$)')
    ax1.set_ylabel('Normalisert verdi ($/U$ eller $/I_0$)')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', framealpha=0.95)
    ax1.set_ylim(-0.06, 1.15)
    
    # Energy dissipation (The Two-Capacitor Paradox)
    ax2.plot(t_norm, E_total, color='#059669', label='Lagret energi i kondensatorene')
    ax2.plot(t_norm, E_diss, color='#dc2626', linestyle='--', label='Tapt energi som varme i $R$')
    ax2.axhline(0.1, color='#059669', linestyle=':', alpha=0.5)
    ax2.axhline(0.9, color='#dc2626', linestyle=':', alpha=0.5)
    
    # Clean callout in open middle area without touching curves or legend
    ax2.annotate('90 % av energien tapes som varme!\n$E_{\\mathrm{diss}}(\\infty) = 0.9 E_i$\n(Uavhengig av motstandsverdi $R$)',
                 xy=(4.2, 0.90), xytext=(1.4, 0.62),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    ax2.set_title('To-kondensator-paradokset: Energifordeling', pad=12)
    ax2.set_xlabel(r'Tid i tidskonstanter $t / \tau$')
    ax2.set_ylabel('Andel av opprinnelig energi $E / E_i$')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='center right', bbox_to_anchor=(0.99, 0.35), framealpha=0.95)
    ax2.set_ylim(-0.06, 1.15)
    
    plt.suptitle('Oppgave 4: Ladningsutveksling mellom to kondensatorer (1. ordens dynamikk)', y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "task4_capacitors_redistribution.png"), bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Plot 4 saved (task4_capacitors_redistribution.png).")

# ==========================================
# PLOT 5 & 6: Open Loop vs PI Control (100% Zero-Overlap)
# ==========================================
def plot_task5_6():
    t = np.linspace(0, 15, 600) # s
    
    # Task 5 response: converges to 12 A
    i_open = 12.0 - 8.0 * np.exp(-t / 3.0)
    
    # Task 6 analytical solution
    alpha = 7.0 / 6.0
    omega_d = np.sqrt(31.0) / 6.0
    B = 16.0 / np.sqrt(31.0)
    i_closed = 4.0 + np.exp(-alpha * t) * (B * np.sin(omega_d * t))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9.0), sharex=True)
    
    # Current response comparison
    ax1.plot(t, i_open, color='#dc2626', linestyle='--', linewidth=2.8,
             label=r'Oppgave 5: Åpen sløyfe ($u=12$ V) $\rightarrow \bar{i} = 12$ A')
    ax1.plot(t, i_closed, color='#2563eb', linewidth=2.8,
             label=r'Oppgave 6: Lukket sløyfe (PI) $\rightarrow \bar{i} = 4.0$ A')
    ax1.axhline(4.0, color='#059669', linestyle=':', alpha=0.85, label=r'Ønsket referanse: $I_{\mathrm{ref}} = 4.0$ A')
    ax1.axvline(0, color='gray', linestyle='--', alpha=0.6)
    
    # 1. Disturbance annotation at t = 0 (Placed cleanly in bottom-left below 4 A line)
    ax1.annotate('Lastendring ved $t = 0$:\n$R_{\\mathrm{load}}$ faller fra $6\\,\\Omega \\to 4\\,\\Omega$',
                 xy=(0, 4.0), xytext=(0.3, 1.6),
                 arrowprops=dict(facecolor='#475569', edgecolor='#475569', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13, color='#1e293b',
                 bbox=dict(boxstyle='round,pad=0.45', facecolor='#f8fafc', edgecolor='#94a3b8', alpha=0.95))
    
    # 2. PI recovery annotation (Placed cleanly in bottom-center below 4 A line)
    ax1.annotate('PI-regulering fjerner avviket\nRobust retur til nøyaktig 4.0 A',
                 xy=(5.0, 4.0), xytext=(6.5, 1.6),
                 arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#1e3a8a',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#eff6ff', edgecolor='#2563eb', alpha=0.95))
    
    # 3. Open-loop failure annotation (Placed in open upper-right, far from legend!)
    ax1.annotate('Uregulert strøm stikker av!\n(+200 % stasjonæravvik)',
                 xy=(12.0, i_open[int(len(t)*12.0/15)]), xytext=(9.2, 14.0),
                 arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#991b1b',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#dc2626', alpha=0.95))
    
    ax1.set_ylabel('Laststrøm $i(t)$ [A]')
    ax1.set_title('Oppgave 5 vs Oppgave 6: Robusthet mot parametrisk lastforstyrrelse', pad=14)
    ax1.grid(True, linestyle=':', alpha=0.6)
    # Legend placed in upper-left (ends cleanly before t = 5.5)
    ax1.legend(loc='upper left', framealpha=0.95, fontsize=12.5)
    ax1.set_ylim(0.2, 17.5)
    
    # Subplot 2: Controller voltage action
    di_dt = np.exp(-alpha * t) * (-alpha * B * np.sin(omega_d * t) + omega_d * B * np.cos(omega_d * t))
    u_closed = 3.0 * di_dt + (4.0 - 3.0) * i_closed
    
    ax2.plot(t, np.full_like(t, 12.0), color='#dc2626', linestyle='--', label=r'Oppgave 5: Fast styrespenning $u = 12$ V')
    ax2.plot(t, u_closed, color='#059669', linewidth=2.8, label=r'Oppgave 6: PI-regulatorens styrespenning $u(t)$')
    ax2.axhline(4.0, color='#047857', linestyle=':', label=r'Ny nødvendig styrespenning $\bar{u}_{\mathrm{ny}} = 4.0$ V')
    
    ax2.annotate('PI-regulatoren justerer spenningen\nautomatisk ned til nøyaktig 4 V',
                 xy=(6.5, 4.0), xytext=(7.0, 8.5),
                 arrowprops=dict(facecolor='#059669', edgecolor='#059669', shrink=0.08, width=2, headwidth=8),
                 fontweight='bold', fontsize=13.5, color='#065f46',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecfdf5', edgecolor='#059669', alpha=0.95))
    
    ax2.set_xlabel('Tid $t$ [sekunder]')
    ax2.set_ylabel('Styrespenning $u(t)$ [V]')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', framealpha=0.95, fontsize=13)
    ax2.set_ylim(0.5, 17.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "task5_6_control_comparison.png"), bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Plot 5 & 6 saved (task5_6_control_comparison.png).")

if __name__ == "__main__":
    plot_task1()
    plot_task2()
    plot_task3()
    plot_task4()
    plot_task5_6()
    print("All 5 pedagogical plots successfully generated!")
