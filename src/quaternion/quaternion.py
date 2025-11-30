from __future__ import annotations

from math import cos, pi, sin, sqrt
from typing import Callable

from .vector3 import Vector3


class Quaternion:
    def __init__(
        self, w: int | float, x: int | float, y: int | float, z: int | float
    ) -> None:
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def norm(self) -> float:
        return sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def scale(self, factor: int | float) -> Quaternion:
        """
        Scales the quaternion by the given factor.

        Parameter
        ---------
        factor: int | float
            Scale factor.

        Returns
        -------
        q: Quaternion
            A new quaternion representing the scaled result.
        """
        return Quaternion(
            self.w * factor, self.x * factor, self.y * factor, self.z * factor
        )

    def normalize(self) -> Quaternion:
        """
        Normalizes the quaternion.
        """
        norm = self.norm()

        return self.scale(1 / norm)

    def add(self, other: Quaternion) -> Quaternion:
        """
        Add two quaternions.
        """
        return Quaternion(
            self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z
        )

    def subtract(self, other: Quaternion) -> Quaternion:
        """
        Subtracts two quaternions.
        """
        return Quaternion(
            self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z
        )

    def multiply(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def conjugate(self) -> Quaternion:
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> Quaternion:
        norm_squared = self.norm() ** 2
        q_conj = self.conjugate()
        return q_conj.scale(1 / norm_squared)

    def transform(self, v: Vector3) -> Vector3:
        p = Quaternion(
            0, v.x, v.y, v.z
        )  # convert Vector3 to Quaternion with zero real part

        if self.norm() != 1:
            t = (
                self * p * self.inverse()
            )  # apply transformation for quaternion of length other than 1
        else:
            t = self * p * self.conjugate()  # apply transformation for unit quaternion

        return Vector3(t.x, t.y, t.z)

    def copy(self) -> Quaternion:
        """
        Returns a copy of the quaternion.
        """
        return Quaternion(self.w, self.x, self.y, self.z)

    def get(self) -> tuple[int | float, int | float, int | float, int | float]:
        """
        Extracts components of the quaternion.
        """
        return (self.w, self.x, self.y, self.z)

    def __add__(self, other: Quaternion) -> Quaternion:
        """
        Adds two quaternions.
        """
        return self.add(other)

    def __sub__(self, other: Quaternion) -> Quaternion:
        """
        Python magic method for quaternion subtraction.
        """
        return self.subtract(other)

    def __mul__(self, other: int | float | Vector3 | Quaternion) -> Quaternion:
        """
        Python magic method for quaternion multiplication with a constant
        or another quaternion.
        """
        if isinstance(other, (int, float)):
            return self.scale(other)
        elif isinstance(other, Vector3):
            q_other = Quaternion(0, other.x, other.y, other.z)
            return self.multiply(q_other)
        elif isinstance(other, Quaternion):
            return self.multiply(other)
        else:
            return NotImplemented

    def __rmul__(self, other: int | float | Quaternion) -> Quaternion:
        """
        Python magic method for quaternion multiplication
        (quaternion multiplication from the right)
        """
        if isinstance(other, (int, float)):
            return self.scale(other)
        elif isinstance(other, Quaternion):
            return other.multiply(self)
        else:
            return NotImplemented

    def __truediv__(self, other: int | float) -> Quaternion:
        """
        Python magic method for quaternion division with a constant.
        """
        if isinstance(other, (int, float)):
            return self.scale(1 / other)
        else:
            return NotImplemented

    def __abs__(self) -> float:
        """
        Python magic method for norm of the quaternion.
        """
        return self.norm()

    def __eq__(self, other: object) -> bool:
        """
        Python magic method for comparing two quaternions (equal).
        """
        if not isinstance(other, Quaternion):
            return NotImplemented

        return (
            self.w == self.w
            and self.x == self.x
            and self.y == self.y
            and self.z == self.z
        )

    def _toString(self, precision: int = 2) -> str:
        """
        Returns a string representation of the quaternion with controlled precision.

        Args:
            precision: Number of decimal places to display (default: 2)

        Returns:
            A formatted string representation of the quaternion.
        """
        # Lambda to format a component with proper sign
        format_component: Callable[[int | float, str], str] = lambda value, suffix: (
            f" {'-' if value < 0 else '+'} {abs(value):.{precision}f}{suffix}"
        )

        # Start with the scalar component
        result = f"{self.w:.{precision}f}"

        # Add vector component
        result += format_component(self.x, "i")
        result += format_component(self.y, "j")
        result += format_component(self.z, "k")

        return result

    def __str__(self) -> str:
        """
        Returns a string representation of the quaternion (calls _toString with default precision).
        """
        return self._toString()

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the quaternion.
        """
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    @property
    def scalar_part(self) -> int | float:
        return self.w

    @property
    def vector_part(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

    @staticmethod
    def from_axis_angle(axis: Vector3, angle: int | float) -> Quaternion:
        if axis.length() != 1:
            axis = axis.normalize()

        half_angle = angle / 2

        return Quaternion(
            cos(half_angle),
            sin(half_angle) * axis.x,
            sin(half_angle) * axis.y,
            sin(half_angle) * axis.z,
        )
