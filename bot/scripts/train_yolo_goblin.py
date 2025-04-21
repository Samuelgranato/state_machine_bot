from ultralytics import YOLO

# Caminho para o modelo e dataset
MODEL_ARCH = "yolov8n.yaml"  # Pode trocar por yolov8s.yaml, yolov8m.yaml, etc.
DATA_CONFIG = "dataset/data.yaml"  # Certifique-se de ter 'train', 'val' e 'test' definidos no YAML
IMG_SIZE = (1080, 1920)
EPOCHS = 30

# Inicializa o modelo (novo)
model = YOLO(MODEL_ARCH)

# Treinamento com dataset completo
model.train(
    data=DATA_CONFIG, imgsz=IMG_SIZE, epochs=EPOCHS, rect=True, batch=16, workers=4, name="yolo_goblin_fullsplit"
)

# Avaliação no conjunto de teste
model.val(data=DATA_CONFIG, split="test", imgsz=IMG_SIZE, conf=0.1, name="yolo_goblin_test")
