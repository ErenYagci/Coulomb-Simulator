import math
from typing import List, Tuple

# Coulomb's Constant (N·m^2 / C^2)
COULOMB_CONSTANT = 8.9875517923e9

class PointCharge:
    def __init__(self, charge: float, x: float, y: float, label: str = ""):
        self.charge = charge  # Charge in Coulombs (C)
        self.x = x            # Position X in meters (m)
        self.y = y            # Position Y in meters (m)
        self.label = label

    def distance_to(self, other: "PointCharge") -> float:
        return math.hypot(other.x - self.x, other.y - self.y)


def calculate_force(source: PointCharge, target: PointCharge) -> Tuple[float, float]:
    """
    Calculates the electrostatic force components (Fx, Fy) exerted by 
    the source charge on the target charge.
    """
    dx = target.x - source.x
    dy = target.y - source.y
    r = math.hypot(dx, dy)

    # Avoid zero division if charges occupy the exact same coordinate
    if r == 0:
        return 0.0, 0.0

    # Coulomb's Law: F = k * (q1 * q2) / r^2
    force_magnitude = COULOMB_CONSTANT * (source.charge * target.charge) / (r ** 2)

    # Unit vector components: (dx / r) and (dy / r)
    fx = force_magnitude * (dx / r)
    fy = force_magnitude * (dy / r)

    return fx, fy


def calculate_net_force(sources: List[PointCharge], test_charge: PointCharge) -> Tuple[float, float, float, float]:
    """
    Computes the net resultant electrostatic force vector acting on the test charge.
    Returns: (net_fx, net_fy, net_magnitude, angle_degrees)
    """
    net_fx = 0.0
    net_fy = 0.0

    for src in sources:
        fx, fy = calculate_force(src, test_charge)
        net_fx += fx
        net_fy += fy

    net_magnitude = math.hypot(net_fx, net_fy)
    angle_degrees = math.degrees(math.atan2(net_fy, net_fx))

    return net_fx, net_fy, net_magnitude, angle_degrees
