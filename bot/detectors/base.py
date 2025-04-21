class BaseDetector:
    def detect(self, frame) -> list:
        raise NotImplementedError("Must implement detect method")
