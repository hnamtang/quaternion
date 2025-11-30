from math import pi, sqrt

from assert_equal import assert_obj_equal, assert_val_equal

from quaternion.quaternion import Quaternion
from quaternion.vector3 import Vector3


def test_norm():
    w, x, y, z = 1, 2, 3, 4
    q = Quaternion(w, x, y, z)

    assert_val_equal(q.norm(), sqrt(w**2 + x**2 + y**2 + z**2))


def test_scale():
    w, x, y, z = 1, 2, 3, 4
    q = Quaternion(w, x, y, z)

    factor = 10

    assert_obj_equal(
        q.scale(factor), Quaternion(w * factor, x * factor, y * factor, z * factor)
    )
    assert_obj_equal(
        q / factor, Quaternion(w / factor, x / factor, y / factor, z / factor)
    )


def test_normalize():
    w, x, y, z = 1, 2, 3, 4
    q = Quaternion(w, x, y, z)

    norm = sqrt(w**2 + x**2 + y**2 + z**2)

    assert_obj_equal(q.normalize(), Quaternion(w / norm, x / norm, y / norm, z / norm))


def test_add():
    w1, x1, y1, z1 = 1, 2, 3, 4
    q1 = Quaternion(w1, x1, y1, z1)

    w2, x2, y2, z2 = -4, 3, -2, 1
    q2 = Quaternion(w2, x2, y2, z2)

    assert_obj_equal(q1.add(q2), Quaternion(w1 + w2, x1 + x2, y1 + y2, z1 + z2))
    assert_obj_equal(q1 + q2, Quaternion(w1 + w2, x1 + x2, y1 + y2, z1 + z2))


def test_subtract():
    w1, x1, y1, z1 = 1, 2, 3, 4
    q1 = Quaternion(w1, x1, y1, z1)

    w2, x2, y2, z2 = -4, 3, -2, 1
    q2 = Quaternion(w2, x2, y2, z2)

    assert_obj_equal(q1.subtract(q2), Quaternion(w1 - w2, x1 - x2, y1 - y2, z1 - z2))
    assert_obj_equal(q1 - q2, Quaternion(w1 - w2, x1 - x2, y1 - y2, z1 - z2))
    assert_obj_equal(q2.subtract(q1), Quaternion(w2 - w1, x2 - x1, y2 - y1, z2 - z1))
    assert_obj_equal(q2 - q1, Quaternion(w2 - w1, x2 - x1, y2 - y1, z2 - z1))


def test_multiply():
    w1, x1, y1, z1 = 1, 2, 3, 4
    q1 = Quaternion(w1, x1, y1, z1)

    w2, x2, y2, z2 = -4, 3, -2, 1
    q2 = Quaternion(w2, x2, y2, z2)

    factor = 10

    v = Vector3(2, 2, 2)

    assert_obj_equal(q1 * q2, Quaternion(-8, 6, -4, -28))
    assert_obj_equal(q2 * q1, Quaternion(-8, -16, -24, -2))

    assert_obj_equal(
        q1 * factor, Quaternion(w1 * factor, x1 * factor, y1 * factor, z1 * factor)
    )
    assert_obj_equal(
        factor * q1, Quaternion(w1 * factor, x1 * factor, y1 * factor, z1 * factor)
    )

    assert_obj_equal(q1 * v, Quaternion(-18, 0, 6, 0))


def test_inverse():
    w1, x1, y1, z1 = 1, 2, 3, 4
    q1 = Quaternion(w1, x1, y1, z1)

    norm_squared = w1**2 + x1**2 + y1**2 + z1**2

    assert_obj_equal(
        q1.inverse(),
        Quaternion(
            w1 / norm_squared,
            -x1 / norm_squared,
            -y1 / norm_squared,
            -z1 / norm_squared,
        ),
    )


def test_transform():
    w1, x1, y1, z1 = 1, 2, 3, 4
    q1 = Quaternion(w1, x1, y1, z1)
    norm = sqrt(w1**2 + x1**2 + y1**2 + z1**2)
    q1_normalized = Quaternion(w1 / norm, x1 / norm, y1 / norm, z1 / norm)
    q1_conjugate = Quaternion(w1 / norm, -x1 / norm, -y1 / norm, -z1 / norm)

    v = Vector3(2, 2, 2)
    q_v = Quaternion(0, v.x, v.y, v.z)

    assert_obj_equal(q1.transform(v), Vector3(0.3999999999999999, 2.0, 2.8))
    assert_obj_equal(
        (q1_normalized * q_v * q1_conjugate).vector_part,
        Vector3(0.3999999999999999, 2.0, 2.8),
    )
