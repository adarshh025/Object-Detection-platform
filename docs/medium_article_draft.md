# Building a Real-Time Object Detection Web App Using Python, YOLO, OpenCV, and Streamlit WebRTC

*By Adarsh Aher*

## 1. Introduction
Computer vision is transforming how we interact with the world. From self-driving cars to security systems, the ability for machines to "see" and understand objects is powerful. I decided to build a complete Real-Time Object Detection Web App, VisionTrack, from scratch.

## 2. Project Objectives
The goal was to create a functional, robust application that could:
1. Detect multiple objects simultaneously via image upload, video upload, or live webcam.
2. Provide a premium, responsive dashboard for configuration.
3. Be deployed easily to a cloud platform like Streamlit Community Cloud.

## 3. Learning OpenCV and Computer Vision
OpenCV is the backbone of video processing in Python. I used it to capture frames, convert color spaces (BGR to RGB), and draw bounding boxes and text labels for the detected objects. 

## 4. Understanding YOLO Object Detection
I integrated Ultralytics YOLOv8 (specifically `yolov8n.pt`, the nano model) for object detection. It is incredibly fast and lightweight, making it perfect for running on cloud environments without requiring a high-end GPU. YOLO processes the frame and returns bounding box coordinates, class labels, and confidence scores for multiple objects in a single pass.

## 5. Designing a Modular Python Architecture
Instead of writing a single monolithic script, I separated the code into modular files:
- `detector.py`: Handles YOLO and OpenCV inference.
- `ui.py`: Contains the Streamlit dashboard logic, state management, and media handling.
- `config.py`: Stores constants.
- `main.py`: The entry point.

## 6. Streamlit and WebRTC
To make the app truly accessible, I removed all dependencies on local hardware and databases. Using `streamlit-webrtc`, I implemented a live webcam mode that streams frames from the user's browser securely using WebRTC and processes them with YOLO.

## 7. Building the Premium Dashboard
I designed the UI to look like a modern AI workstation. With custom CSS in Streamlit, I applied a midnight navy theme with cyan accents, interactive KPI metric cards, and a history table of all detections.

## 8. Challenges Encountered and Solutions
*(Adarsh Aher: Add a personal challenge here. For example: Figuring out how to configure STUN servers for WebRTC, or managing Streamlit session state correctly to persist detection history without a database.)*

## 9. Testing and Validation
I wrote automated tests using `pytest` to validate detector initialization, handling of empty images, and verifying that no heavy database dependencies were creeping into the project.

## 10. Key Learning Outcomes
This project bridged the gap between machine learning and web development. I learned how to handle real-time data streams in the browser, optimize YOLO for CPU inference, and deploy a full-stack Python application to the cloud.

## 11. Project Results and Limitations
The application runs smoothly in the cloud. A current limitation is that the `yolov8n` model can struggle with very small objects. In the future, I plan to add support for larger models and exporting analytics to CSV.

## 12. GitHub Repository and Demonstration Links
- **GitHub Repository**: [adarshh025/Object-Detection-platform](https://github.com/adarshh025/Object-Detection-platform)
- **Demo Video**: [Insert URL]

## 13. Conclusion
Building this platform was a fantastic learning experience. It proves that with the right Python libraries, building complex AI-integrated software is more accessible than ever.
