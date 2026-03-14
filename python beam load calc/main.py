import math
from dataclasses import dataclass

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


@dataclass
class BeamInputs:
    length_m: float
    total_load_n: float
    y_m: float
    inertia_m4: float
    points: int


def prompt_float(label: str, min_value: float | None = None) -> float:
    while True:
        raw = input(label).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if min_value is not None and value <= min_value:
            print(f"Please enter a value greater than {min_value}.")
            continue
        return value


def prompt_int(label: str, min_value: int) -> int:
    while True:
        raw = input(label).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value < min_value:
            print(f"Please enter a value of at least {min_value}.")
            continue
        return value


def get_inputs() -> BeamInputs:
    print("Beam Load & Stress Calculator")
    print("Assumes a simply supported beam with a uniformly distributed load.")
    print("")
    length_m = prompt_float("Beam length L (m): ", min_value=0.0)
    total_load_n = prompt_float("Total load P (N): ", min_value=0.0)
    y_m = prompt_float("Distance from neutral axis y (m): ", min_value=0.0)
    inertia_m4 = prompt_float("Moment of inertia I (m^4): ", min_value=0.0)
    points = prompt_int("Number of calculation points (e.g., 200): ", min_value=10)
    print("")
    return BeamInputs(
        length_m=length_m,
        total_load_n=total_load_n,
        y_m=y_m,
        inertia_m4=inertia_m4,
        points=points,
    )


def compute_distributions(inputs: BeamInputs):
    length = inputs.length_m
    total_load = inputs.total_load_n
    w = total_load / length if length > 0 else math.inf

    x = np.linspace(0.0, length, inputs.points)

    # Simply supported beam with UDL w (N/m)
    reactions = w * length / 2.0
    shear = reactions - w * x
    moment = reactions * x - 0.5 * w * x**2

    stress = (moment * inputs.y_m) / inputs.inertia_m4

    return x, w, shear, moment, stress


def summarize_results(x, w, shear, moment, stress, inputs: BeamInputs):
    max_moment = float(np.max(np.abs(moment)))
    max_stress = float(np.max(np.abs(stress)))
    max_shear = float(np.max(np.abs(shear)))

    print("Results (absolute maxima):")
    print(f"Uniform load w: {w:.3f} N/m")
    print(f"Max shear: {max_shear:.3f} N")
    print(f"Max moment: {max_moment:.3f} N·m")
    print(f"Max stress: {max_stress:.3f} Pa")

    mid_index = int(len(x) / 2)
    print("")
    print("Mid-span values:")
    print(f"x = {x[mid_index]:.3f} m")
    print(f"Shear = {shear[mid_index]:.3f} N")
    print(f"Moment = {moment[mid_index]:.3f} N·m")
    print(f"Stress = {stress[mid_index]:.3f} Pa")
    print("")


def plot_results(x, w, shear, moment, stress, inputs: BeamInputs, output_path: str = "beam_results.png"):
    load = np.full_like(x, w)

    fig, axes = plt.subplots(4, 1, figsize=(9, 12), sharex=True)
    fig.suptitle("Beam Load & Stress Distributions", fontsize=14)

    axes[0].plot(x, load, color="#1f77b4")
    axes[0].set_ylabel("Load (N/m)")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(x, shear, color="#ff7f0e")
    axes[1].set_ylabel("Shear (N)")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(x, moment, color="#2ca02c")
    axes[2].set_ylabel("Moment (N·m)")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(x, stress, color="#d62728")
    axes[3].set_ylabel("Stress (Pa)")
    axes[3].set_xlabel("Position x (m)")
    axes[3].grid(True, alpha=0.3)

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")

    backend = mpl.get_backend().lower()
    if "agg" not in backend:
        plt.show()


def main():
    inputs = get_inputs()
    x, w, shear, moment, stress = compute_distributions(inputs)
    summarize_results(x, w, shear, moment, stress, inputs)
    plot_results(x, w, shear, moment, stress, inputs)


if __name__ == "__main__":
    main()
