import asyncio
from logging import DEBUG

from bot.detectors.yolo_asset_detector import YoloAssetDetector

# Example: two target types
DETECTOR_CONFIGS = {"enemy": {"model_path": "models/yolo_goblin.pt", "target_classes": ["goblin", "orc"]}}

detectors = {key: YoloAssetDetector(cfg["model_path"], cfg["target_classes"]) for key, cfg in DETECTOR_CONFIGS.items()}


async def watch_assets(state):
    while True:
        frame = await state.get("__frame")
        if frame is None:
            continue

        detections = {}
        for key, detector in detectors.items():
            results = detector.detect(frame, debug=DEBUG)
            detections[key] = results

        await state.set("detections", detections)
        await asyncio.sleep(0.5)
