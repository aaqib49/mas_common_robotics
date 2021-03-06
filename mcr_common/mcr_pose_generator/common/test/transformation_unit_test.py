#!/usr/bin/env python
"""
Test unit for the functions in transformations.py module.

To run it, type:
py.test [file_name]

"""

PKG = 'mcr_pose_generator'

import math
import numpy
import unittest
import rosunit
import mcr_pose_generator.transformations as transformations


class TestGraspPlanner(unittest.TestCase):
    """
    Tests functions in the transformations.py module.

    """
    def test_translation(self):
        """
        Translation test.

        """
        # params
        expected_result = numpy.identity(4)
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        gripper_matrix = numpy.identity(4)     # SDH transformation matrix

        # No translation case
        expected_result[2, 3] = offset

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Positive translation case
        offset = 0.3        # meters
        expected_result[2, 3] = offset

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative translation case
        offset = -0.3        # meters
        expected_result[2, 3] = offset

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result[{0}, {1}] : {2}".format(i, j, result[i, j])
                )

    def test_zenith(self):
        """
        Zenith test.

        """
        ## No zenith, no translation case
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        gripper_matrix = numpy.identity(4)     # SDH transformation matrix

        expected_result = numpy.identity(4)
        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Zenith and no translation cases
        # Negative zenith params
        offset = 0.0            # meters
        azimuthal = 0.0         # radians
        zenith = -math.pi / 2   # radians
        expected_result = numpy.array([
            [0.0, 0.0, -1.0, 0.0],
            [0.0, 1.0,  0.0, 0.0],
            [1.0, 0.0,  0.0, 0.0],
            [0.0, 0.0,  0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        # Negative zenith params
        offset = 0.0            # meters
        azimuthal = 0.0         # rads
        zenith = -math.pi / 6    # rads
        expected_result = numpy.array([
            [0.866, 0.0,  -0.5, 0.0],
            [0.0,   1.0,   0.0, 0.0],
            [0.5,   0.0, 0.866, 0.0],
            [0.0,   0.0,   0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Zenith and translation, but no azimuthal
        offset = 0.3             # meters
        azimuthal = 0.0          # rads
        zenith = math.pi / 6    # rads
        expected_result = numpy.array([
            [0.866, 0.0,   0.5,    0.0],
            [0.0,   1.0,   0.0,    0.0],
            [-0.5,  0.0, 0.866, offset],
            [0.0,   0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Zenith and azimuthal, but no translation
        offset = 0.0                # meters
        azimuthal = -math.pi / 6    # rads
        zenith = math.pi / 2        # rads
        expected_result = numpy.array([
            [0.0,  -0.5, 0.866, 0.0],
            [0.0, 0.866,   0.5, 0.0],
            [-1.0,  0.0,   0.0, 0.0],
            [0.0,   0.0,   0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Zenith, azimuthal, and translation
        offset = 0.3                # meters
        azimuthal = -math.pi / 6    # rads
        zenith = math.pi / 2        # rads
        expected_result = numpy.array([
            [0.0,  -0.5, 0.866,    0.0],
            [0.0, 0.866,   0.5,    0.0],
            [-1.0,  0.0,   0.0, offset],
            [0.0,   0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

    def test_azimuthal(self):
        """
        Azimuthal test.

        """
        ## No zenith, no azimuthal, and no translation case
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        gripper_matrix = numpy.identity(4)     # SDH transformation matrix

        expected_result = numpy.identity(4)
        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        # Positive azimuthal params
        offset = 0.0                # meters
        azimuthal = math.pi / 6     # radians
        zenith = 0.0                # radians
        expected_result = numpy.array([
            [1.0,   0.0,   0.0, 0.0],
            [0.0, 0.866,  -0.5, 0.0],
            [0.0,   0.5, 0.866, 0.0],
            [0.0,   0.0,   0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Azimuthal and translation cases
        # Positive azimuthal params
        offset = 0.3                # meters
        azimuthal = math.pi / 2     # radians
        zenith = 0.0                # radians
        expected_result = numpy.array([
            [1.0, 0.0,  0.0,    0.0],
            [0.0, 0.0, -1.0,    0.0],
            [0.0, 1.0,  0.0, offset],
            [0.0,  0.0, 0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative azimuthal params
        offset = 0.3                # meters
        azimuthal = -math.pi / 6    # radians
        zenith = 0.0                # radians
        expected_result = numpy.array([
            [1.0,   0.0,   0.0,    0.0],
            [0.0, 0.866,   0.5,    0.0],
            [0.0,  -0.5, 0.866, offset],
            [0.0,   0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

    def test_wrist_roll(self):
        """
        Wrist roll test.

        """
        ## No wrist roll, no zenith, no azimuthal, and no translation case
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        gripper_matrix = numpy.identity(4)     # SDH transformation matrix

        expected_result = numpy.identity(4)
        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Wrist roll, but no zenith, azimuthal, nor translation cases
        # Positive wrist roll params
        offset = 0.0                # meters
        azimuthal = 0.0             # radians
        zenith = 0.0                # radians
        wrist_roll = math.pi / 6    # radians
        expected_result = numpy.array([
            [0.866, -0.5, 0.0, 0.0],
            [0.5,  0.866, 0.0, 0.0],
            [0.0,    0.0, 1.0, 0.0],
            [0.0,    0.0, 0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative wrist roll params
        offset = 0.0                # meters
        azimuthal = 0.0             # radians
        zenith = 0.0                # radians
        wrist_roll = -math.pi / 2    # radians
        expected_result = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Wrist roll and translation, but no zenith, nor azimuthal cases
        # Positive wrist roll params
        offset = 0.3                # meters
        azimuthal = 0.0             # radians
        zenith = 0.0                # radians
        wrist_roll = math.pi / 6    # radians
        expected_result = numpy.array([
            [0.866, -0.5, 0.0,    0.0],
            [0.5,  0.866, 0.0,    0.0],
            [0.0,    0.0, 1.0, offset],
            [0.0,    0.0, 0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative wrist roll params
        offset = 0.3                # meters
        azimuthal = 0.0             # radians
        zenith = 0.0                # radians
        wrist_roll = -math.pi / 2    # radians
        expected_result = numpy.array([
            [0.0,  1.0, 0.0,    0.0],
            [-1.0, 0.0, 0.0,    0.0],
            [0.0,  0.0, 1.0, offset],
            [0.0,  0.0, 0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Wrist roll, azimuthal, and translation, but no zenith cases
        # Positive wrist roll params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = 0.0                # radians
        wrist_roll = math.pi / 6    # radians
        expected_result = numpy.array([
            [0.866,   -0.5,   0.0,    0.0],
            [0.433,   0.75,  -0.5,    0.0],
            [0.25,   0.433, 0.866, offset],
            [0.0,      0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative wrist roll params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = 0.0                # radians
        wrist_roll = -math.pi / 2    # radians
        expected_result = numpy.array([
            [0.0,    1.0,   0.0,    0.0],
            [-0.866, 0.0,  -0.5,    0.0],
            [-0.5,   0.0, 0.866, offset],
            [0.0,    0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Wrist roll, azimuthal,  translation, and zenith cases
        # Positive wrist roll params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = math.pi / 2        # radians
        wrist_roll = math.pi / 6    # radians
        expected_result = numpy.array([
            [0.25, 0.433, 0.866,    0.0],
            [0.433, 0.75,  -0.5,    0.0],
            [-0.866, 0.5,   0.0, offset],
            [0.0,    0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        # Negative wrist roll params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = math.pi / 2        # radians
        wrist_roll = -math.pi / 2    # radians
        expected_result = numpy.array([
            [-0.5,   0.0, 0.866,    0.0],
            [-0.866, 0.0,  -0.5,    0.0],
            [0.0,   -1.0,   0.0, offset],
            [0.0,    0.0,   0.0,    1.0]
        ])

        result = transformations.generate_grasp_matrix(gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial)

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

    def test_radial(self):
        """
        Radial test.

        """
        ## No radial
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        gripper_matrix = numpy.identity(4)     # SDH transformation matrix

        expected_result = numpy.identity(4)
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only radial
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.3        # meters

        expected_result = numpy.identity(4)
        expected_result[0, 3] = -radial

        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only radial and height
        # params
        offset = 0.3        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.1        # meters

        expected_result = numpy.array([
            [1.0, 0.0, 0.0, -radial],
            [0.0, 1.0, 0.0,     0.0],
            [0.0, 0.0, 1.0,  offset],
            [0.0, 0.0, 0.0,     1.0]
        ])

        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Radial and zenith
        # params
        offset = 0.0            # meters
        azimuthal = 0.0         # radians
        zenith = -math.pi / 2   # radians
        wrist_roll = 0.0        # radians
        radial = 0.1            # meters

        expected_result = numpy.array([
            [0.0, 0.0, -1.0, -radial],
            [0.0, 1.0,  0.0,     0.0],
            [1.0, 0.0,  0.0,     0.0],
            [0.0, 0.0,  0.0,     1.0]
        ])

        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

    def test_gripper_matrix(self):
        """
        Gripper configuration matrix test.

        """
        ## Only gripper matrix
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = gripper_matrix
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix and height offset
        # params
        offset = 0.3        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.3],
            [0.0,  0.0, 0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix and radial
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.2        # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [0.0,  1.0, 0.0,  0.0],
            [-1.0, 0.0, 0.0,  0.2],
            [0.0,  0.0, 1.0,  0.0],
            [0.0,  0.0, 0.0,  1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix, offset, and radial
        # params
        offset = 0.3        # meters
        azimuthal = 0.0     # radians
        zenith = 0.0        # radians
        wrist_roll = 0.0    # radians
        radial = 0.2        # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.2],
            [0.0,  0.0, 1.0, 0.3],
            [0.0,  0.0, 0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j],
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix and azimuthal
        # params
        offset = 0.0                # meters
        azimuthal = math.pi / 6    # radians
        zenith = 0.0                # radians
        wrist_roll = 0.0            # radians
        radial = 0.0                # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [0.0, 0.866,  -0.5, 0.0],
            [-1.0,  0.0,   0.0, 0.0],
            [0.0,   0.5, 0.866, 0.0],
            [0.0,   0.0,   0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix and zenith
        # params
        offset = 0.0        # meters
        azimuthal = 0.0     # radians
        zenith = -math.pi   # radians
        wrist_roll = 0.0    # radians
        radial = 0.0        # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [0.0, 1.0,  0.0, 0.0],
            [1.0, 0.0,  0.0, 0.0],
            [0.0, 0.0, -1.0, 0.0],
            [0.0, 0.0,  0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Only gripper matrix and wrist roll
        # params
        offset = 0.0                # meters
        azimuthal = 0.0             # radians
        zenith = 0.0                # radians
        wrist_roll = -math.pi / 2   # radians
        radial = 0.0                # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Rotation tests (azimuthal, zenith and/or wrist_roll)
        # params
        offset = 0.0                # meters
        azimuthal = math.pi / 6     # radians
        zenith = math.pi / 3        # radians
        wrist_roll = -math.pi / 2   # radians
        radial = 0.0                # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [-0.866,   0.0,  -0.5, 0.0],
            [0.433,   -0.5, -0.75, 0.0],
            [-0.25, -0.866, 0.433, 0.0],
            [0.0,      0.0,   0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## Rotation and height offset tests
        # params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = math.pi / 3        # radians
        wrist_roll = -math.pi / 2   # radians
        radial = 0.0                # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [-0.866,   0.0,  -0.5, 0.0],
            [0.433,   -0.5, -0.75, 0.0],
            [-0.25, -0.866, 0.433, 0.3],
            [0.0,      0.0,   0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

        ## All parameters tests
        # params
        offset = 0.3                # meters
        azimuthal = math.pi / 6     # radians
        zenith = math.pi / 3        # radians
        wrist_roll = -math.pi / 2   # radians
        radial = 0.2                # meters
        # youBot gripper (precision grasp)
        gripper_matrix = numpy.array([
            [0.0,  1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0]
        ])

        expected_result = numpy.array([
            [-0.866,   0.0,  -0.5, 0.0],
            [0.433,   -0.5, -0.75, 0.2],
            [-0.25, -0.866, 0.433, 0.3],
            [0.0,      0.0,   0.0, 1.0]
        ])
        result = transformations.generate_grasp_matrix(
            gripper_matrix, offset, zenith, azimuthal, wrist_roll, radial
        )

        cols = len(result)
        rows = cols
        for i in range(cols):
            for j in range(rows):
                self.assertAlmostEqual(
                    result[i, j], expected_result[i, j], places=3,
                    msg="result: {0}".format(result)
                )

if __name__ == '__main__':
    rosunit.unitrun(PKG, 'test_grasp_planner', TestGraspPlanner)
