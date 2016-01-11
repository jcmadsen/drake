from __future__ import print_function
import unittest
import numpy as np
import pydrake
from pydrake.autodiffutils import toAutoDiff
import os.path

class TestRBMForwardKin(unittest.TestCase):
    def testFK_value(self):
        r = pydrake.rbtree.RigidBodyTree(os.path.join(pydrake.getDrakePath(), "examples/Pendulum/Pendulum.urdf"))
        self.assertEqual(r.num_positions, 7)
        self.assertEqual(r.num_velocities, 7)

        kinsol = r.doKinematics(np.zeros((7,1)), np.zeros((7,1)))

        p = r.forwardKin(kinsol, np.zeros((3,1)), 0, 1, 0)
        self.assertTrue(np.allclose(p, np.zeros((3,1))))

    def testFK_gradient(self):
        r = pydrake.rbtree.RigidBodyTree(os.path.join(pydrake.getDrakePath(), "examples/Pendulum/Pendulum.urdf"))

        q = toAutoDiff(np.zeros((7,1)), np.eye(7, 7))
        v = toAutoDiff(np.zeros((7,1)), np.zeros((7, 7)))
        kinsol = r.doKinematics(q, v)

        point = np.ones((3,1))
        p = r.forwardKin(kinsol, point, 2, 0, 0)
        self.assertTrue(np.allclose(p.value(), np.ones((3,1))))
        self.assertTrue(np.allclose(p.derivatives(),
                                    np.array([[1, 0, 0, 0, 1, -1, 1],
                                              [0, 1, 0, -1, 0, 1, 0],
                                              [0, 0, 1, 1, -1, 0, -1]])))

if __name__ == '__main__':
    unittest.main()


