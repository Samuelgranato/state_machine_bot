# 🧠 State Machine Bot

This is a reactive visual automation project for 3D games using a modular structure in Python. It uses machine learning, OCR, and computer vision to interact with screen elements in real-time. Designed to be easily adaptable to different games, with a focus on performance, modularity, and extensibility.

---

## 🔧 Technologies Used

- `asyncio` for concurrent watchers and actors
- `EasyOCR` for text recognition (health, stamina, status)
- `YOLOv8` for visual asset detection (e.g., enemies, resources)
- `OpenCV` for image processing
- `mss` for efficient screen capture
- `rich` and `tkinter` for dashboards and visual output

---

## 📁 Project Structure

```
app/
├── main.py                  # Bot entry point
├── orchestrator.py         # Main loop and watcher initialization
├── config.py               # Global parameters
├── state.py                # Shared state management
├── menu.py                 # Interactive menu to launch jobs

├── detectors/
│   ├── image/              # YOLOv8-based object detection
│   └── text/               # OCR via EasyOCR with preprocessing

├── jobs/
│   ├── actors/             # Actuators (e.g., attack, heal)
│   ├── watchers/           # Screen watchers (e.g., health, vision)
│   └── modes/              # Automation behaviors via state machine

├── scripts/                # Utility scripts for training and asset capture
│   ├── train_yolo_goblin.py
│   ├── screenshot_capture.py
│   └── convert_assets_to_yolo.py

├── visual/                 # Debug visualizations and dashboard
│   ├── debug.py
│   ├── panel.py
│   └── table.py
```

---

## 🚀 How to Run

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Start the bot:

```bash
cd app
python main.py
```

Or use the interactive menu:

```bash
python menu.py
```

---

## 🧩 Features

- Async reactive watchers running in parallel
- State-machine based automation modes
- Modular detection: health, stamina, enemies, resources
- Optimized OCR with preprocessing
- YOLOv8 detection with support for multiple classes
- Visual debugging (OpenCV) and terminal dashboard (rich)

---

## 🧠 Extensibility

This project is designed to be scalable and modular. To add a new automation mode:

- Create a new watcher in `jobs/watchers/`
- Create a new actor in `jobs/actors/`
- Add a mode to `jobs/modes/`
- Register the mode in `menu.py`

---

## 🗂 Dataset and Models

- Train your YOLOv8 model with `train_yolo_goblin.py`
- Use `screenshot_capture.py` and `convert_assets_to_yolo.py` to build and label datasets
- Place trained `.pt` models under `app/data/` (or adjust paths in config)

---

## 🧪 Testing and Debugging

- Use `debug=True` in detectors to enable bounding box preview
- Use `panel.py` to visualize the live state of the bot
- Use `cv2_debug()` to preview OpenCV frames

---

## 📜 License

This project is licensed under the Apache 2.0 License.
