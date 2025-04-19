import re

import cv2
import easyocr
import numpy as np

# OCR engine
reader = easyocr.Reader(["en"], gpu=False)

# Caminho da imagem
img_path = "debug_stamina_roi_scaled_stamina_91.png"

# Carrega imagem e aplica pré-processamento
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.convertScaleAbs(gray, alpha=2, beta=0)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
_, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
resized = cv2.resize(thresh, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

# Opcional: aplica dilatação para melhorar separação dos números
kernel = np.ones((2, 2), np.uint8)
dilated = cv2.dilate(resized, kernel, iterations=1)

# Salva imagem de debug se quiser ver o resultado
cv2.imwrite("debug_stamina_processed.png", dilated)

# OCR
results = reader.readtext(dilated)

# Limpeza e exibição
if results:
    raw_text = results[0][1]
    clean_text = re.sub(r"[^\d]", "", raw_text)
    print(f"🔍 OCR bruto: {raw_text}")
    print(f"✅ Digitos limpos: {clean_text}")
else:
    print("❌ Nada detectado")
