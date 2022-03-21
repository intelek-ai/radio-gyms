import os
import unittest
import numpy as np

from radio_gyms.engines import Tracer
from radio_gyms.engines.ray_tracer.triangle import Triangle
from radio_gyms.engines.ray_tracer.box import Box
from numpy.typing import NDArray

POZNAN_OBJ_PATH = os.path.join(os.getcwd(), "assets", "models", "poznan.obj")

class TestTracer(unittest.TestCase):

    def test_triangle(self):
        a:NDArray = np.array([5,0,-3])
        b:NDArray = np.array([-5,0,-2])
        c:NDArray = np.array([0,-4,4])
        test_triangle = Triangle(a, b, c)

        ray_pos = np.array([0, 15 ,0])
        ray_dir = np.array([0, -1, 0])
        ray = (ray_pos, ray_dir)
        result = test_triangle.is_intersect(ray)
        self.assertGreater(result, 0)
        ray_pos2 = np.array([0, 15, 0])
        ray_dir2 = np.array([0, 1, 0])
        ray2 = (ray_pos2, ray_dir2)
        result = test_triangle.is_intersect(ray2)
        self.assertLess(result, 0)

    def test_box(self):
        a: NDArray = np.array([5, 0, -3])
        b: NDArray = np.array([-5, 0, -2])
        c: NDArray = np.array([0, -4, 4])
        test_triangle = Triangle(a, b, c)
        box = Box([test_triangle])

        ray_pos = np.array([0, 0, 0])
        ray_dir = np.array([0, -1, 0])
        ray = (ray_pos, ray_dir)
        result = box.is_intersect(ray)
        self.assertEqual(result, True)

        ray_pos2 = np.array([0, 10, 0])
        ray_dir2 = np.array([0, 1, 0])
        ray2 = (ray_pos2, ray_dir2)
        result2 = box.is_intersect(ray2)
        self.assertEqual(result2, False)

    def test_tracer_direct(self):
        tracer = Tracer(POZNAN_OBJ_PATH)
        tx_pos = np.array([0, 15, 0])
        rx_pos = np.array([-30, 1.5, 45])
        result1 = tracer.trace_outdoor(tx_pos, rx_pos)
        self.assertEqual(result1["direct"], False)
        tx_pos2 = np.array([0, 100, 0])
        rx_pos2 = np.array([0, 101, 0])
        result2 = tracer.trace_outdoor(tx_pos2, rx_pos2)
        self.assertEqual(result2["direct"], True)

    def test_tracer_reflect(self):
        tracer = Tracer(POZNAN_OBJ_PATH)
        tx_pos = np.array([0, 15, 0])
        rx_pos = np.array([-30, 1.5, 45])
        result = tracer.find_edge(tx_pos, rx_pos)
        self.assertEqual(len(result), 3)
