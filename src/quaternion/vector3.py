from math import acos, pi, sqrt
from typing import Callable


class Vector3:
    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def norm(self, norm_type: int | str = 2) -> float:
        """
        Calculates norms of the vector.

        Parameter
        ----------
        norm_type: int | str
            Norm type of vector. 1, 2, or 'inf'. Default: 2

        Returns
        -------
        norm: float
            Norm of given type of vector.
        """
        if isinstance(norm_type, str):
            return max(abs(self.x), abs(self.y), abs(self.z))
        elif isinstance(norm_type, int):
            if norm_type == 1:
                return abs(self.x) + abs(self.y) + abs(self.z)
            elif norm_type == 2:
                return sqrt(self.x**2 + self.y**2 + self.z**2)
            else:
                raise ValueError(
                    f'norm_type must be either 1, 2, or "inf". Got {norm_type}'
                )
        else:
            raise TypeError(
                f"norm_type must be of type int or str. Got {type(norm_type)}"
            )

    def scale(self, factor: int | float) -> "Vector3":
        """
        Scales the vector by the given factor.

        Parameter
        ---------
        factor: int | float
            Scale factor.

        Returns
        -------
        v: Vector3
            The vector scaled by the given factor.
        """
        return Vector3(self.x * factor, self.y * factor, self.z * factor)

    def normalize(self) -> "Vector3":
        """
        Normalizes the vector.
        """
        norm = self.norm(2)

        return self.scale(1 / norm)

    def add(self, other: "Vector3") -> "Vector3":
        """
        Adds two vectors.
        """
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other: "Vector3") -> "Vector3":
        """
        Subtracts two vectors.
        """
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other: "Vector3") -> float:
        """
        Calculates dot product of two vectors.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        """
        Calculates cross product of two vectors.
        """
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angle(self, other: "Vector3", unit: str = "rad") -> float:
        """
        Calculates angle from two vectors.

        Parameters
        ----------
        other: Vector3
            The second vector.
        unit: str ('deg' | 'rad')
            The unit of angle. Default: 'rad'

        Returns
        -------
        angle: float
            Angle between two vectors.
        """
        if isinstance(unit, str):
            length_v1 = self.norm()
            length_v2 = other.norm()
            angle = acos(self.dot(other) / (length_v1 * length_v2))
            if unit == "deg":
                return angle * 180 / pi
            elif unit == "rad":
                return angle
            else:
                raise ValueError(f"unit must be either 'deg' or 'rad'. Got {unit}")
        else:
            raise TypeError(f"unit must be str. Got {type(unit)}")

    def copy(self) -> "Vector3":
        """
        Returns a copy of the vector.
        """
        return Vector3(self.x, self.y, self.z)

    def get(self) -> tuple[int | float, int | float, int | float]:
        """
        Extracts components of the vector.
        """
        return (self.x, self.y, self.z)

    def __add__(self, other: "Vector3") -> "Vector3":
        """
        Python magic method for vector addition.
        """
        return self.add(other)

    def __sub__(self, other: "Vector3") -> "Vector3":
        """
        Python magic method for vector subtraction.
        """
        return self.subtract(other)

    def __mul__(self, factor: int | float) -> "Vector3":
        """
        Python magic method for scaling vector.
        """
        return self.scale(factor)

    def __rmul__(self, factor: int | float) -> "Vector3":
        """
        Python magic method for scaling vector (vector multiplication from the right)
        """
        return self.scale(factor)

    def __neg__(self) -> "Vector3":
        """
        Python magic method for vector negation.
        """
        return Vector3(-self.x, -self.y, -self.z)

    def __abs__(self) -> float:
        """
        Python magic method for vector length.
        """
        return self.norm(2)

    def __eq__(self, other: object) -> bool:
        """
        Python magic method for comparing two vectors (equal).
        """
        if not isinstance(other, Vector3):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z

    def _to_string(self, precision: int = 2) -> str:
        """
        Constructs a string representation for vector with a precision (Default = 2).
        """
        format_component: Callable[[int | float, str], str] = lambda value, suffix: (
            f" {'-' if value < 0 else '+'} {abs(value):.{precision}f}{suffix}"
        )

        result = f"{self.x:.{precision}f}e_x"
        result += format_component(self.y, "e_y")
        result += format_component(self.z, "e_z")

        return result

    def __str__(self) -> str:
        """
        Returns a string representation of the vector (calls _toString with default precision).
        """
        return self._to_string()

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the vector.
        """
        return f"Vector3({self.x}, {self.y}, {self.z})"

    @staticmethod
    def from_plane(
        point1: tuple[int | float, int | float, int | float],
        point2: tuple[int | float, int | float, int | float],
        point3: tuple[int | float, int | float, int | float],
    ) -> "Vector3":
        """
        Caculates normal vector of a plane formed by three 3D points.
        """
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        x3, y3, z3 = point3

        v12 = Vector3(x2 - x1, y2 - y1, z2 - z1)
        v13 = Vector3(x3 - x1, y3 - y1, z3 - z1)

        return v12.cross(v13)


# -------------------------------------------------------------------------------------
# Module-level helper functions
# -------------------------------------------------------------------------------------
def dot(v1: Vector3, v2: Vector3) -> float:
    return v1.dot(v2)


def cross(v1: Vector3, v2: Vector3) -> Vector3:
    return v1.cross(v2)


def angle(v1: Vector3, v2: Vector3, unit: str = "rad") -> float:
    """
    Calculates angle from two vectors.

    Parameters
    ----------
    v1, v2: Vector3
        2 vector of class Vector3.
    unit: str ('deg' | 'rad')
        The unit of angle. Default: 'rad'

    Returns
    -------
    angle: float
        Angle between two vectors.
    """
    if isinstance(unit, str):
        length_v1 = v1.norm()
        length_v2 = v2.norm()
        angle = acos(v1.dot(v2) / (length_v1 * length_v2))
        if unit == "deg":
            return angle * 180 / pi
        elif unit == "rad":
            return angle
        else:
            raise ValueError(f"unit must be either 'deg' or 'rad'. Got {unit}")
    else:
        raise TypeError(f"unit must be str. Got {type(unit)}")
