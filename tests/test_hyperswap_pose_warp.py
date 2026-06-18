import unittest

import cv2
import inspect
import numpy as np

from reactor_core.hyperswap import HyperSwapper
from reactor_core.inswap import INSwapper


STD_LANDMARKS_256 = np.array([
    [84.87, 105.94],
    [171.13, 105.94],
    [128.00, 146.66],
    [96.95, 188.64],
    [159.05, 188.64],
], dtype=np.float32)


class HyperSwapPoseWarpTest(unittest.TestCase):
    def test_pose_warp_maps_face_features_to_target_landmarks(self):
        swapper = object.__new__(HyperSwapper)
        source_face = np.zeros((256, 256, 3), dtype=np.float32)
        colors = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (0.0, 1.0, 1.0),
        ]
        for point, color in zip(STD_LANDMARKS_256, colors):
            cv2.circle(source_face, tuple(np.round(point).astype(int)), 5, color, -1)

        target_landmarks = np.array([
            [92.0, 78.0],
            [224.0, 86.0],
            [155.0, 160.0],
            [107.0, 230.0],
            [207.0, 216.0],
        ], dtype=np.float32)
        M, _ = cv2.estimateAffinePartial2D(target_landmarks, STD_LANDMARKS_256)

        warped = swapper._warp_face_to_target_landmarks(
            source_face,
            M,
            target_landmarks,
            STD_LANDMARKS_256,
            output_size=(300, 300),
            interpolation=cv2.INTER_LINEAR,
            border_value=0.0,
        )

        for point, color in zip(target_landmarks, colors):
            x, y = np.round(point).astype(int)
            patch = warped[y - 3:y + 4, x - 3:x + 4]
            self.assertGreater(
                np.max(np.linalg.norm(patch - color, axis=2) < 0.25),
                0,
                f"Expected feature color {color} near target landmark {point}",
            )


class INSwapperPoseWarpContractTest(unittest.TestCase):
    def test_inswapper_paste_back_uses_pose_warp(self):
        source = inspect.getsource(INSwapper.get)

        self.assertIn("warp_face_to_target_landmarks", source)
