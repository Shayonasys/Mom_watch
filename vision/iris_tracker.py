import numpy as np


class IrisTracker:

    # iris landmarks
    LEFT_IRIS = [468, 469, 470, 471, 472]
    RIGHT_IRIS = [473, 474, 475, 476, 477]

    # Left eye landmarks
    LEFT_EYE = {
        "outer": 33,
        "inner": 133,
        "top": 159,
        "bottom": 145,
    }

    # Right eye landmarks
    RIGHT_EYE = {
        "outer": 362,
        "inner": 263,
        "top": 386,
        "bottom": 374,
    }

    def process(self, landmarks):

        if landmarks is None or len(landmarks) < 478:
            return None

        left = self._calculate_eye(
            landmarks,
            self.LEFT_IRIS,
            self.LEFT_EYE,
        )

        right = self._calculate_eye(
            landmarks,
            self.RIGHT_IRIS,
            self.RIGHT_EYE,
        )

        if left is None or right is None:
            return None

        left_ratio = left[1]
        right_ratio = right[1]

        average_ratio = (
            left_ratio + right_ratio
        ) / 2.0

        return average_ratio

    @staticmethod
    def _calculate_eye(
        landmarks,
        iris_ids,
        eye_ids,
    ):

        try:
            iris_points = np.array(
                [
                    [
                        landmarks[index].x,
                        landmarks[index].y,
                    ]
                    for index in iris_ids
                ],
                dtype=np.float64,
            )

            iris_center = iris_points.mean(axis=0)

            top = landmarks[eye_ids["top"]]
            bottom = landmarks[eye_ids["bottom"]]

            outer = landmarks[eye_ids["outer"]]
            inner = landmarks[eye_ids["inner"]]

            vertical_span = max(
                abs(bottom.y - top.y),
                1e-6,
            )

            horizontal_span = max(
                abs(inner.x - outer.x),
                1e-6,
            )

            y_ratio = (
                iris_center[1] - top.y
            ) / vertical_span

            x_ratio = (
                iris_center[0] - outer.x
            ) / horizontal_span

            return (
                float(np.clip(x_ratio, -1, 2)),
                float(np.clip(y_ratio, -1, 2)),
            )

        except (
            IndexError,
            AttributeError,
            TypeError,
        ):
            return None