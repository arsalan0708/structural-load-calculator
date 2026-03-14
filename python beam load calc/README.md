# Beam Load & Stress Calculator

Python tool for basic beam calculations using a simple, well-defined case.

## What it does
- Calculates uniform load, shear force, bending moment, and bending stress.
- Uses the bending stress formula `σ = M * y / I`.
- Plots load, shear, moment, and stress vs. position along the beam.

## Assumptions
- Simply supported beam.
- Uniformly distributed load (UDL) across the entire span.
- Input "Total load P" is the total applied load over the length (N).

## Formulas used
- Uniform load: `w = P / L`
- Reactions: `R1 = R2 = w * L / 2`
- Shear: `V(x) = R1 - w * x`
- Moment: `M(x) = R1 * x - (w * x^2) / 2`
- Stress: `σ(x) = M(x) * y / I`

## Requirements
- Python 3.10+
- NumPy
- Matplotlib

Install deps:
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

You will be prompted for:
- Beam length `L` (m)
- Total load `P` (N)
- Distance from neutral axis `y` (m)
- Moment of inertia `I` (m^4)
- Number of calculation points

## Notes
This is a baseline structural calculation tool meant for learning and quick checks. If you need more load cases (point loads, triangular loads, fixed ends), say the word and we can extend it.
