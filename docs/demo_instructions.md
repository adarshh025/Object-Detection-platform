# Demonstration Video Preparation Guide

**Project:** VisionTrack — Real-Time Multi-Object Detection
**Creator:** Adarsh Aher

## Recording Setup
1. Ensure your webcam is working and well-lit.
2. Launch the Streamlit application: `streamlit run main.py`.
3. Use a screen recording tool (e.g., OBS Studio, Windows Game Bar `Win + Alt + R`, or Zoom).

## Demonstration Script (1–2 Minutes)

* **0–15 seconds:** 
  - Show the Streamlit dashboard home screen.
  - Introduce the project: "Hello, this is VisionTrack, my Real-Time Multi-Object Detection platform, created by Adarsh Aher."
  - Point out the status indicator showing successful Model connection.

* **15–35 seconds:** 
  - Select the **Image** or **Video** mode and upload a file.
  - Demonstrate YOLO detecting multiple objects simultaneously and drawing bounding boxes.

* **35–55 seconds:** 
  - In the sidebar, change the **Confidence Threshold** (e.g., raise it to 0.8) and show how it affects detections.
  - Change the **Object Classes** filter to only detect "person" and show that other objects are ignored.

* **55–80 seconds:** 
  - Point to the **KPI metrics** (Objects Detected, Average Confidence).
  - Switch to the **Live Webcam** mode (if supported by your network/recording setup) and allow camera permissions.
  - Show real-time browser inference.

* **80–100 seconds:** 
  - Briefly show the Detection Results table and the bar chart generated from the session's detection history.
  - Show that no database is required to run this app.

* **100–120 seconds:** 
  - Briefly show the VS Code project structure or the GitHub repository page.
  - Conclude: "Thank you for watching."

## Post-Recording
1. Review the video to ensure it looks good.
2. Upload the video to Google Drive or YouTube (as an Unlisted video).
3. Add the video link to the `README.md` placeholder.
