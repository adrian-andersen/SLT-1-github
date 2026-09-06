"""
generate_circuit_diagrams.py
Draws publication-quality circuit diagrams matching Figures 1 to 6 of TET4100 SLT-1.
Saves them as crisp PNG images in assets/circuits/
"""

import os
import schemdraw
import schemdraw.elements as elm

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "circuits")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set schemdraw styling for clean white theme with high contrast
schemdraw.theme('default')

# ==========================================
# CIRCUIT 1: Task 1 - Basic RL Circuit
# ==========================================
def draw_circuit_1():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task1.png"), show=False, dpi=220) as d:
        d.config(fontsize=14, font='sans-serif', lw=2)
        
        # Source branch
        V1 = d.add(elm.SourceV().up().label(('+', 'U = 36 V', '-'), loc='left'))
        
        # Top wire with switch and R1
        d.add(elm.Switch().right().label('t = 0', loc='top'))
        d.add(elm.Resistor().right().label('$R_1 = 24\\,\\Omega$', loc='top'))
        d.add(elm.Dot())
        
        # Inductor branch
        d.push()
        d.add(elm.Inductor2().down().label(('+', '$L = 120\\,\\text{mH}$\n$v_L(t)$', '-'), loc='left').label('$i_L(t)$', loc='bot'))
        d.add(elm.Dot())
        d.pop()
        
        # Resistor R2 branch
        d.add(elm.Line().right().length(3))
        d.add(elm.Resistor().down().label('$R_2 = 48\\,\\Omega$', loc='right'))
        
        # Bottom wire
        d.add(elm.Line().left().length(3))
        d.add(elm.Line().to(V1.start))

    print("Circuit 1 drawn.")

# ==========================================
# CIRCUIT 2: Task 2 - Sequential Switching RC
# ==========================================
def draw_circuit_2():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task2.png"), show=False, dpi=220) as d:
        d.config(fontsize=14, font='sans-serif', lw=2)
        
        # Position 1: 10 V source (+ on top)
        V1 = d.add(elm.SourceV().up().label(('+', '10 V', '-'), loc='left'))
        d.add(elm.Dot().label('1', loc='left'))
        
        # Wire to bottom reference
        d.add(elm.Line().at(V1.start).right().length(2.5))
        d.add(elm.Dot())
        
        # Position 2: 20 V source (- on top, + on bottom)
        d.push()
        V2 = d.add(elm.SourceV().up().label(('-', '20 V', '+'), loc='left'))
        d.add(elm.Dot().label('2', loc='left'))
        d.pop()
        
        # Common line right
        d.add(elm.Line().right().length(3.5))
        d.add(elm.Dot())
        
        # Capacitor branch down
        d.add(elm.Capacitor().up().label(('+', '$1\\,\\mu\\text{F}$\n$v_C(t)$', '-'), loc='right'))
        d.add(elm.Resistor().up().label('$R = 1\\,\\text{k}\\Omega$', loc='right'))
        d.add(elm.Line().left().length(2.5))
        
        # Switch SPDT
        d.add(elm.SwitchSpdt2().left().label('$i(t)$', loc='bot'))

    print("Circuit 2 drawn.")

# ==========================================
# CIRCUIT 3: Task 3 - Dynamical System with Dependent Source
# ==========================================
def draw_circuit_3():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task3.png"), show=False, dpi=220) as d:
        d.config(fontsize=13, font='sans-serif', lw=2)
        
        # Capacitor branch on left
        C1 = d.add(elm.Capacitor().up().label(('+', '$C = 5\\,\\mu\\text{F}$\n$v_c(t)$', '-'), loc='left').label('$i_c$', loc='top'))
        
        # Switch at top closing at t=0
        d.add(elm.Switch(action='close').right().label('t = 0', loc='top'))
        d.add(elm.Dot())
        
        # Resistor R1 branch
        d.push()
        d.add(elm.Resistor().down().label(('+', '$R_1$\n$v_0(t)$', '-'), loc='left'))
        d.add(elm.Dot())
        d.pop()
        
        # Line to dependent source
        d.add(elm.Line().right().length(2.8))
        d.add(elm.Dot())
        
        # Dependent current source 7*i_delta (pointing UP)
        d.push()
        d.add(elm.SourceI().up().label('$7 i_\\Delta$', loc='left').reverse())
        d.pop()
        
        # Line to R2 branch
        d.add(elm.Line().right().length(2.8))
        d.add(elm.Resistor().down().label('$R_2 = 20\\,\\text{k}\\Omega$', loc='right').label('$i_\\Delta$', loc='bot'))
        
        # Bottom rail
        d.add(elm.Line().left().length(2.8))
        d.add(elm.Line().left().length(2.8))
        d.add(elm.Line().to(C1.start))

    print("Circuit 3 drawn.")

# ==========================================
# CIRCUIT 4: Task 4 - Two Capacitors
# ==========================================
def draw_circuit_4():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task4.png"), show=False, dpi=220) as d:
        d.config(fontsize=14, font='sans-serif', lw=2)
        
        # Capacitor C on left
        C1 = d.add(elm.Capacitor().up().label(('+', '$C$\n$u_C(0^+) = U$', '-'), loc='left'))
        
        # Switch closing at t=0
        d.add(elm.Switch(action='close').right().label('S\nt = 0', loc='top'))
        
        # Resistor R on top
        d.add(elm.Resistor().right().label(('+', '$R$\n$u_R(t)$', '-'), loc='top').label('$i(t)$', loc='bot'))
        
        # Capacitor 9C on right
        d.add(elm.Capacitor().down().label(('+', '$9C$\n$u_{9C}(t)$', '-'), loc='right'))
        
        # Bottom wire
        d.add(elm.Line().to(C1.start))

    print("Circuit 4 drawn.")

# ==========================================
# CIRCUIT 5: Task 5 - Equilibrium Control
# ==========================================
def draw_circuit_5():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task5.png"), show=False, dpi=220) as d:
        d.config(fontsize=14, font='sans-serif', lw=2)
        
        # Controllable voltage source u(t)
        V1 = d.add(elm.SourceV().up().label(('+', '$u(t)$', '-'), loc='left'))
        
        # Top wire with inductor L
        d.add(elm.Inductor2().right().label('$L = 3\\,\\text{H}$', loc='top').label('$i(t) \\rightarrow$', loc='bot'))
        
        # Dependent voltage source -k*i(t)
        # Note: in schemdraw, SourceControlledV gives diamond
        d.add(elm.SourceControlledV().right().label(('+', '$-k \\cdot i(t)$', '-'), loc='top'))
        
        # Load resistor
        d.add(elm.Resistor().down().label('$R_{\\text{load}} = 6\\,\\Omega$', loc='right'))
        
        # Bottom wire
        d.add(elm.Line().to(V1.start))

    print("Circuit 5 drawn.")

# ==========================================
# CIRCUIT 6: Task 6 - PI Controller Digital Network & Load
# ==========================================
def draw_circuit_6():
    with schemdraw.Drawing(file=os.path.join(OUTPUT_DIR, "circuit_task6.png"), show=False, dpi=220) as d:
        d.config(fontsize=13, font='sans-serif', lw=2)
        
        # Reference current source I_ref
        Iref = d.add(elm.SourceI().up().label('$I_{\\text{ref}} = 4\\,\\text{A}$', loc='left'))
        d.add(elm.Dot())
        
        # Parallel capacitor C in blue box
        d.add(elm.Line().right().length(2))
        d.add(elm.Dot())
        d.push()
        d.add(elm.Capacitor().down().label(('+', '$C = 0.15\\,\\text{F}$\n$v_C(t)$', '-'), loc='left'))
        d.add(elm.Dot())
        d.pop()
        
        # Series resistor R1
        d.add(elm.Resistor().right().label('$R_1 = 6\\,\\Omega$', loc='top'))
        d.add(elm.Dot().label(('+', '$u(t)$', '-'), loc='right'))
        
        # Inductor L
        d.add(elm.Inductor2().right().label('$L = 3\\,\\text{H}$', loc='top').label('$i(t) \\rightarrow$', loc='bot'))
        
        # Dependent voltage source -k*i
        d.add(elm.SourceControlledV().right().label(('+', '$-k \\cdot i(t)$', '-'), loc='top'))
        
        # Load resistor R_load
        d.add(elm.Resistor().down().label('$R_{\\text{load}} = 4\\,\\Omega$', loc='right'))
        
        # Bottom return rail
        d.add(elm.Line().to(Iref.start))

    print("Circuit 6 drawn.")

if __name__ == "__main__":
    draw_circuit_1()
    draw_circuit_2()
    draw_circuit_3()
    draw_circuit_4()
    draw_circuit_5()
    draw_circuit_6()
    print("All circuit diagrams successfully generated in:", OUTPUT_DIR)
