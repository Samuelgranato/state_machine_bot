class BaseOCREngine:
    def read(self, image) -> str:
        raise NotImplementedError("Subclasses must implement 'read'")
