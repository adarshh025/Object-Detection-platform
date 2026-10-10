# VisionTrack — Real-Time Multi-Object Detection

**Project Created By:** Adarsh Aher

## Project Overview
VisionTrack is a complete, functional, real-time computer vision web application that detects multiple objects simultaneously through image upload, video upload, or a live browser-based webcam. It draws bounding boxes around detected objects, allows users to configure detection settings, and displays real-time analytics through a premium modern dashboard.

## Features
- **Real-Time Object Detection**: Uses YOLOv8 for fast and accurate object recognition.
- **Multiple Sources**: Supports image uploads, video uploads, and WebRTC-based live webcam detection.
- **Configurable Settings**: Adjust confidence thresholds and filter by object classes.
- **Interactive Dashboard**: Built with Streamlit for live viewing and analytics with a premium dark theme.
- **Multi-Object Tracking**: Identifies and labels multiple objects in a single inference pass.
- **Analytics**: Session-level KPI metrics and charts for detection history.

## Technology Stack
- **Python**: Core application logic.
- **OpenCV**: Video processing and frame manipulation.
- **Ultralytics YOLO**: Pretrained object detection model (YOLOv8n).
- **Streamlit**: Web-based dashboard.
- **streamlit-webrtc**: Browser-based webcam streaming.
- **Pandas**: Data manipulation and analytics.

## Architecture
- `main.py`: Application entry point.
- `detector.py`: YOLO object detection engine.
- `ui.py`: Streamlit dashboard implementation.
- `config.py`: Configuration.

## Prerequisites
- Python 3.9 or higher
- A webcam (for live detection)

## Local Installation Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Set up a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **YOLO Model Setup:**
   The `yolov8n.pt` model will be downloaded automatically by the Ultralytics library on the first run. Ensure you have an active internet connection.

## Application Startup Commands

To launch the dashboard locally, run:
```powershell
streamlit run main.py
```

## Streamlit Community Cloud Deployment

This application is ready for deployment on Streamlit Community Cloud.

1. **Prepare GitHub Repository**: Push the complete source code to a public or private GitHub repository. Do not commit `.venv` or temporary files.
2. **Deploy on Streamlit**: Go to [share.streamlit.io](https://share.streamlit.io/), link your GitHub account, and select the repository.
3. **Configure App**: Set the main file path as `main.py`.
4. **Deploy**: Click Deploy. The platform will automatically install dependencies from `requirements.txt` and launch the app.
5. **Webcam Permissions**: In a deployed environment, the browser will ask for camera permissions to use the Live Webcam feature via WebRTC.

## Dashboard Usage Instructions
1. Open the URL provided by Streamlit in your web browser.
2. In the sidebar, select your detection mode (Image, Video, Live Webcam).
3. Adjust the Confidence Threshold and Object Classes if needed.
4. Upload your media or grant webcam permissions.
5. View the annotated feed and real-time metrics.
6. Check the "Detection Results" section for a table of detected objects and a class distribution chart.

## Testing Instructions
To run the automated test suite using `pytest`:
```powershell
pytest tests/
```

## Troubleshooting
- **Model Download Fails**: Check your internet connection. You can also manually download `yolov8n.pt` and place it in the project root.
- **WebRTC Connection Fails**: Ensure your network allows STUN/TURN connections if deploying on the cloud.

## Learning Outcomes
- Implementing state-of-the-art computer vision models (YOLO).
- Processing video streams with OpenCV and WebRTC.
- Designing premium, responsive web dashboards with Streamlit.
- Building AI applications suitable for cloud deployment.

## GitHub Repository
[adarshh025/Object-Detection-platform](https://github.com/adarshh025/Object-Detection-platform)
