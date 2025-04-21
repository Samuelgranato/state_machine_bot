import cv2
from ultralytics import YOLO

from bot.detectors.base import BaseDetector


class YoloAssetDetector(BaseDetector):
    def __init__(self, model_path: str, target_classes: list, conf_threshold: float = 0.1):
        self.model = YOLO(model_path)
        self.target_classes = target_classes
        self.conf_threshold = conf_threshold  # 👈 novo parâmetro configurável

    def detect(self, frame, debug=False) -> list:
        results = self.model(frame, conf=self.conf_threshold, verbose=False)[0]  # 👈 conf aqui
        detections = []

        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, cls_id = r
            label = results.names[int(cls_id)]

            if label in self.target_classes:
                detections.append({"label": label, "confidence": score, "bbox": (x1, y1, x2, y2)})

                if debug:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"{label} {score:.2f}",
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        1,
                    )

        if debug:
            cv2.imshow("YOLO Debug", frame)
            cv2.waitKey(1)

        return detections
