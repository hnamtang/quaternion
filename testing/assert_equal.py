import pytest

from quaternion.quaternion import Quaternion
from quaternion.vector3 import Vector3


def assert_obj_equal(actual: Vector3 | Quaternion, expected: Vector3 | Quaternion):
    """
    Compares 2 objects (Vector3 or Quaternion) for equality with 10 decimal place precision.

    Parameters
    ----------
    actual: Vector3 | Quaternion
        The object to test (Vector3 or Quaternion).
    expected: Vector3 | Quaternion
        The expected value (Vector3 or Quaternion).
    """
    if isinstance(actual, Vector3) and isinstance(expected, Vector3):
        assert actual.x == pytest.approx(expected.x, rel=1e-10)
        assert actual.y == pytest.approx(expected.y, rel=1e-10)
        assert actual.z == pytest.approx(expected.z, rel=1e-10)
    elif isinstance(actual, Quaternion) and isinstance(expected, Quaternion):
        assert actual.w == pytest.approx(expected.w, rel=1e-10)
        assert actual.x == pytest.approx(expected.x, rel=1e-10)
        assert actual.y == pytest.approx(expected.y, rel=1e-10)
        assert actual.z == pytest.approx(expected.z, rel=1e-10)
    else:
        raise TypeError(
            "Both arguments must be of the same type (Vector3 or Quaternion)."
        )


def assert_val_equal(actual: float, expected: float):
    """
    Compares 2 numeric values for equality with 10 decimal place precision.
    """
    assert actual == pytest.approx(expected, rel=1e-10)
