import streamlit as st
import cv2
import numpy as np
import time
import tempfile
import os
import pandas as pd
from detector import ObjectDetector
import config
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode
import av

# Configuration for WebRTC (STUN server for NAT traversal)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

def init_session_state():
    if 'detector' not in st.session_state:
        st.session_state.detector = ObjectDetector(config.DEFAULT_MODEL)
    if 'session_detections' not in st.session_state:
        st.session_state.session_detections = 0
    if 'current_objects' not in st.session_state:
        st.session_state.current_objects = 0
    if 'current_classes' not in st.session_state:
        st.session_state.current_classes = 0
    if 'current_avg_conf' not in st.session_state:
        st.session_state.current_avg_conf = 0.0
    if 'detection_history' not in st.session_state:
        st.session_state.detection_history = pd.DataFrame(columns=['Object', 'Confidence', 'Position (x,y)', 'Dimensions (w,h)'])

def update_metrics(detections):
    st.session_state.current_objects = len(detections)
    
    unique_classes = set()
    conf_sum = 0
    history_rows = []
    
    for d in detections:
        unique_classes.add(d['class_name'])
        conf_sum += d['confidence']
        st.session_state.session_detections += 1
        history_rows.append({
            'Object': d['class_name'],
            'Confidence': f"{d['confidence']:.2%}",
            'Position (x,y)': f"({d['bbox_x']}, {d['bbox_y']})",
            'Dimensions (w,h)': f"{d['bbox_w']}x{d['bbox_h']}"
        })
        
    st.session_state.current_classes = len(unique_classes)
    st.session_state.current_avg_conf = conf_sum / len(detections) if detections else 0.0
    
    if history_rows:
        st.session_state.detection_history = pd.DataFrame(history_rows)
    else:
        st.session_state.detection_history = pd.DataFrame(columns=['Object', 'Confidence', 'Position (x,y)', 'Dimensions (w,h)'])

def render_kpi_cards():
    st.markdown("""
        <style>
        div[data-testid="metric-container"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 5% 5% 5% 10%;
            border-radius: 5px;
            color: white;
            overflow-wrap: break-word;
        }
        div[data-testid="metric-container"] > div > div > div > p {
            font-size: 1.1rem;
            color: #94a3b8;
        }
        div[data-testid="metric-container"] > div > div > div > div {
            font-size: 1.8rem;
            color: #00e5ff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Objects Detected", st.session_state.current_objects)
    with col2:
        st.metric("Classes Found", st.session_state.current_classes)
    with col3:
        st.metric("Average Confidence", f"{st.session_state.current_avg_conf:.1%}")
    with col4:
        st.metric("Session Detections", st.session_state.session_detections)

def process_and_display_image(image_bytes, conf_threshold, selected_classes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        st.error("Invalid image file.")
        return
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    with st.spinner("Processing image..."):
        processed_frame, detections = st.session_state.detector.process_frame(
            frame_rgb, 
            conf_threshold=conf_threshold, 
            selected_classes=selected_classes
        )
    
    update_metrics(detections)
    
    st.image(processed_frame, channels="RGB", use_container_width=True)
    
    # Download button
    processed_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
    ret, buffer = cv2.imencode('.png', processed_bgr)
    if ret:
        st.download_button(
            label="Download Annotated Image",
            data=buffer.tobytes(),
            file_name="annotated_image.png",
            mime="image/png",
            type="primary"
        )

def process_and_display_video(video_file, conf_threshold, selected_classes):
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    tfile.close()
    
    cap = cv2.VideoCapture(tfile.name)
    if not cap.isOpened():
        st.error("Error opening video file.")
        os.remove(tfile.name)
        return

    frame_placeholder = st.empty()
    stop_button = st.button("Stop Video Processing", type="secondary")
    
    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame, detections = st.session_state.detector.process_frame(
            frame_rgb, 
            conf_threshold=conf_threshold, 
            selected_classes=selected_classes
        )
        
        update_metrics(detections)
        
        # Display the frame
        frame_placeholder.image(processed_frame, channels="RGB", use_container_width=True)
        
        # We render metrics in a separate placeholder in the main function
        time.sleep(0.01) # Small delay to prevent locking
        
    cap.release()
    os.remove(tfile.name)
    if not stop_button:
        st.success("Video processing completed.")

def render_dashboard():
    init_session_state()
    
    # Title and Header
    st.markdown("<h1 style='text-align: center; color: #00e5ff;'>VisionTrack</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #f1f5f9;'>Real-Time Multi-Object Detection</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-style: italic;'>Real-time intelligence. Multiple objects. One visual workspace.</p>", unsafe_allow_html=True)
    
    # Status indicator
    if st.session_state.detector.is_model_loaded():
        st.markdown("<div style='text-align: center;'><span style='color: #4ade80;'>●</span> Model Ready</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center;'><span style='color: #ef4444;'>●</span> Model Not Loaded</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Layout
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_sidebar:
        st.header("Settings")
        mode = st.radio("Detection Mode", ["Image", "Video", "Live Webcam"])
        
        st.markdown("---")
        st.subheader("Configuration")
        conf_threshold = st.slider("Confidence Threshold", 0.1, 0.95, config.CONFIDENCE_THRESHOLD, 0.05)
        
        classes_options = ["All"] + config.COCO_CLASSES
        selected_classes = st.multiselect("Object Classes", options=classes_options, default=["All"])
        
        if st.button("Reset Session Stats", type="secondary", use_container_width=True):
            st.session_state.session_detections = 0
            st.session_state.current_objects = 0
            st.session_state.current_classes = 0
            st.session_state.current_avg_conf = 0.0
            st.session_state.detection_history = pd.DataFrame(columns=['Object', 'Confidence', 'Position (x,y)', 'Dimensions (w,h)'])
            st.rerun()
            
        st.markdown("---")
        st.markdown("<div style='text-align: center; color: #94a3b8;'><small>Made by Adarsh Aher</small></div>", unsafe_allow_html=True)

    with col_main:
        kpi_placeholder = st.empty()
        
        # Display KPIs first so they update
        with kpi_placeholder.container():
            render_kpi_cards()
            
        st.markdown("### Workspace")
        
        if mode == "Image":
            img_file = st.file_uploader("Upload an Image", type=['jpg', 'jpeg', 'png', 'webp'])
            if img_file is not None:
                process_and_display_image(img_file.read(), conf_threshold, selected_classes)
                # Re-render KPIs after processing
                with kpi_placeholder.container():
                    render_kpi_cards()
            else:
                st.info("Please upload an image to start detection.")
                
        elif mode == "Video":
            video_file = st.file_uploader("Upload a Video", type=['mp4', 'mov', 'avi'])
            if video_file is not None:
                if st.button("Start Processing", type="primary"):
                    process_and_display_video(video_file, conf_threshold, selected_classes)
                    with kpi_placeholder.container():
                        render_kpi_cards()
            else:
                st.info("Please upload a video to start processing.")
                
        elif mode == "Live Webcam":
            st.write("Use your browser's webcam for real-time detection.")
            
            def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
                img = frame.to_ndarray(format="bgr24")
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                processed_frame, detections = st.session_state.detector.process_frame(
                    img_rgb, 
                    conf_threshold=conf_threshold, 
                    selected_classes=selected_classes
                )
                
                # We can't update Streamlit UI elements directly from this callback easily 
                # without using session state and a separate polling loop, but we can draw the bounding boxes.
                
                processed_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                return av.VideoFrame.from_ndarray(processed_bgr, format="bgr24")
            
            webrtc_streamer(
                key="visiontrack",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                video_frame_callback=video_frame_callback,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )
            
            st.info("Note: Live webcam mode processes frames in the browser. Session metrics may not update continuously during WebRTC stream.")

        # Results Table
        st.markdown("### Detection Results")
        if not st.session_state.detection_history.empty:
            st.dataframe(st.session_state.detection_history, use_container_width=True, hide_index=True)
            
            # Simple chart for counts per class
            st.markdown("#### Objects by Class")
            counts = st.session_state.detection_history['Object'].value_counts()
            st.bar_chart(counts)
        else:
            st.info("No detections yet.")

if __name__ == "__main__":
    render_dashboard()
