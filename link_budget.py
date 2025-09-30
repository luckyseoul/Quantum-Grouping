"""
link_budget.py - Link Budget Calculations for Quantum Grouping
Computes survival probability η and optimal n for RF/laser mediums over 401M km.
Usage: python link_budget.py --medium rf --d_tx 34 --d_rx 3 --lambda 0.01 --r 4.01e11
Default: rf, D_tx=34m, D_rx=3m, λ=0.01m, r=4.01e11m (Mars).
"""

import argparse
import math

def calculate_eta(medium, d_tx, d_rx, lam, r):
    """Calculate η from link budget: divergence, collection, detector, pointing."""
    # Divergence θ ≈ 1.22 λ / D_tx (Airy disk)
    theta = 1.22 * lam / d_tx
    # Spot size at r
    spot = r * theta
    # Collection fraction ∝ (D_rx / spot)^2
    collection = (d_rx / spot)**2
    # Detector efficiency 0.7, pointing 0.95
    eta = collection * 0.7 * 0.95
    # Medium adjustment (RF broader, laser tighter)
    if medium == "laser":
        eta *= 10  # Tighter beam factor (X-ray λ=1e-10 vs. 0.01)
    return max(eta, 1e-6)  # Floor to avoid log(0)

def optimal_n(eta):
    """Optimal n for 90% P_success = 1 - (1 - η)^n ≥ 0.9."""
    if eta >= 1:
        return 1
    n = math.ceil(-math.log(0.1) / math.log(1 - eta))
    p_success = 1 - (1 - eta)**n
    return n, p_success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Link Budget for Quantum Grouping")
    parser.add_argument("--medium", type=str, default="rf", choices=["rf", "laser"], help="Medium type")
    parser.add_argument("--d_tx", type=float, default=34, help="Transmit aperture (m)")
    parser.add_argument("--d_rx", type=float, default=3, help="Receive aperture (m)")
    parser.add_argument("--lambda", type=float, default=0.01, help="Wavelength (m)")
    parser.add_argument("--r", type=float, default=4.01e11, help="Distance (m)")
    args = parser.parse_args()

    eta = calculate_eta(args.medium, args.d_tx, args.d_rx, args.lambda, args.r)
    n, p_success = optimal_n(eta)
    print(f"Medium: {args.medium.upper()}")
    print(f"η (survival): {eta:.6f}")
    print(f"Optimal n: {n}")
    print(f"P_success: {p_success:.4f}")
