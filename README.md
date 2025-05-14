# object-detection-speed-estimation
Deep learning-based highway object detection and speed estimation system using YOLO and R-CNN, with GUI, Docker deployment, and performance analysis.

## 🚀 Getting Started

Follow the steps below to set up and run the project locally.

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/Zain-Rizwan/object-detection-speed-estimation.git
cd object-detection-speed-estimation
```

### ⚙️ 2. [Optional - Windows Only] Allow Scripts to Run Temporarily
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
### 🐍 3. Create and Activate Virtual Environment

## On Windows:
```bash
python -m venv yolovenv
yolovenv\Scripts\activate
```
## On macOS/Linux:
```bash
python3 -m venv yolovenv
source yolovenv/bin/activate
```
### 📦 4. Install Required Dependencies
Once inside the virtual environment, install all dependencies using:

```bash
pip install -r requirements.txt
```

### ▶️ 5. Run the Application
There are two main entry points depending on the model you want to run:

## ✅ For YOLOv8-based Detection:
```bash
python main.py
```
## ✅ For R-CNN-based Detection:
```bash
python r_main.py
```
