import numpy as np
from assert_equal import assert_obj_equal, assert_val_equal

from quaternion.vector3 import Vector3


def test_norms():
    x = 5.2
    y = 2.7
    z = -8.3
    v = Vector3(x, y, z)

    # 1st norm
    assert_val_equal(v.norm(1), abs(x) + abs(y) + abs(z))

    # 2nd norm
    assert_val_equal(v.norm(2), np.sqrt(x**2 + y**2 + z**2))

    # Infinity norm
    assert_val_equal(v.norm("inf"), max(abs(x), abs(y), abs(z)))


def test_normalize():
    x = 5.2
    y = 2.7
    z = -8.3
    length = np.sqrt(x**2 + y**2 + z**2)
    v = Vector3(x, y, z)

    assert_obj_equal(v.normalize(), Vector3(x / length, y / length, z / length))


def test_dot():
    x1 = 5.2
    y1 = 2.7
    z1 = -8.3
    v1 = Vector3(x1, y1, z1)

    x2 = -0.2
    y2 = 1.5
    z2 = -4.4
    v2 = Vector3(x2, y2, z2)

    assert_val_equal(v1.dot(v2), x1 * x2 + y1 * y2 + z1 * z2)


def test_cross():
    x1 = 5.2
    y1 = 2.7
    z1 = -8.3
    v1 = Vector3(x1, y1, z1)

    x2 = -0.2
    y2 = 1.5
    z2 = -4.4
    v2 = Vector3(x2, y2, z2)

    x_result = y1 * z2 - z1 * y2
    y_result = z1 * x2 - x1 * z2
    z_result = x1 * y2 - y1 * x2

    assert_obj_equal(v1.cross(v2), Vector3(x_result, y_result, z_result))


def test_angle():
    x1, y1, z1 = 1, 0, 0
    v1 = Vector3(x1, y1, z1)

    x2, y2, z2 = 0, 0, 1
    v2 = Vector3(x2, y2, z2)

    assert_val_equal(v1.angle(v2), np.pi / 2)
    assert_val_equal(v1.angle(v2, "deg"), 90)


def test_normal_vector():
    p1 = (0, 0, 0)
    p2 = (1, 0, 0)
    p3 = (0, 0, 1)

    assert_obj_equal(Vector3.from_plane(p1, p2, p3), Vector3(0, -1, 0))


def test_scaling():
    x1, y1, z1 = 1, 2, 3
    v1 = Vector3(x1, y1, z1)

    factor = 2.3

    assert_obj_equal(v1.scale(factor), Vector3(x1 * factor, y1 * factor, z1 * factor))
    assert_obj_equal(v1 * factor, Vector3(x1 * factor, y1 * factor, z1 * factor))
    assert_obj_equal(factor * v1, Vector3(x1 * factor, y1 * factor, z1 * factor))


def test_comparison():
    x1, y1, z1 = 1, 2, 3
    v1 = Vector3(x1, y1, z1)

    x2, y2, z2 = 1.0, 2.0, 3.0
    v2 = Vector3(x2, y2, z2)

    assert_val_equal(v1 == v2, True)
