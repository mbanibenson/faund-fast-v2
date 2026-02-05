import streamlit as st
from ultralytics import YOLO
from pathlib import Path
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Benthic AI Dashboard", layout="wide", page_icon="🌊")

# --- 2. SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.title("🎛️ Control Panel")
    
    st.info("Instructions:\n1. Copy folder paths.\n2. Set confidence.\n3. Click Start.")
    
    st.header("1. Data Configuration")
    # OS-agnostic path inputs (works on Windows/Mac/Linux)
    input_str = st.text_input(
        "📂 Input Folder:", 
        placeholder="Path to folder with images/videos",
        help="Full path to the folder containing raw media."
    )
    output_str = st.text_input(
        "💾 Output Folder:", 
        placeholder="Path to save results",
        help="A new timestamped folder will be created here for every run."
    )

    st.header("2. Model Settings")
    default_model = Path("best.pt")
    model_path_str = st.text_input("Model File (.pt):", value=str(default_model))
    
    conf_threshold = st.slider(
        "Confidence Threshold", 
        min_value=0.0, max_value=1.0, value=0.25, step=0.05,
        help="Lower = more detections (but maybe more errors). Higher = stricter."
    )
    
    # Video Specific Settings
    st.header("3. Video Optimization")
    frame_stride = st.slider(
        "Frame Stride (Video Only)", 
        min_value=1, max_value=30, value=5,
        help="Process every Nth frame. 1 = Process All (Slow). 5 = Process every 5th (Faster)."
    )
    
    st.divider()
    start_btn = st.button("🚀 Start Detection", type="primary", use_container_width=True)

# --- 3. MAIN DASHBOARD LAYOUT ---
st.title("🌊 Benthic Live Dashboard")

# Status Container (Top of main area)
status_container = st.container()
with status_container:
    # This text updates dynamically to show what the model is doing
    status_text = st.empty()
    status_text.info("👋 Ready. Supports Images (.jpg, .png) and Videos (.mp4, .avi, .mov).")
    progress_bar = st.progress(0)

st.divider()

# Split Layout: Viewer (Left) and Stats (Right)
col_viewer, col_stats = st.columns([2, 1])

with col_viewer:
    st.subheader("👁️ Live Detection View")
    image_placeholder = st.empty()
    image_placeholder.caption("Live detection feed will appear here.")

with col_stats:
    st.subheader("📊 Cumulative Mission Counts")
    table_placeholder = st.empty()

# --- 4. PROCESSING LOGIC ---
def process_media():
    # Setup Paths
    input_path = Path(input_str)
    base_output_path = Path(output_str)
    model_path = Path(model_path_str)

    # --- Validation ---
    if not input_path.exists():
        status_text.error(f"❌ Input folder not found: {input_path}")
        return
    
    if not model_path.exists():
        status_text.error(f"❌ Model file not found: {model_path}")
        return

    # --- Create Timestamped Output Folder ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_dir = base_output_path / f"Run_{timestamp}"
    
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        status_text.info(f"📂 Output folder created: {save_dir.name}")
    except Exception as e:
        status_text.error(f"❌ Output Error: {e}")
        return

    # --- Load Model ---
    try:
        model = YOLO(str(model_path))
    except Exception as e:
        status_text.error(f"❌ Model Load Error: {e}")
        return

    # --- Find Files ---
    valid_exts = {'.jpg', '.png', '.jpeg', '.bmp', '.tif', '.mp4', '.avi', '.mov', '.mkv'}
    files = [f for f in input_path.iterdir() if f.suffix.lower() in valid_exts]
    
    if not files:
        status_text.warning("⚠️ No compatible media found in input directory.")
        return

    # --- Initialize Metrics ---
    all_detections = []
    total_mission_counts = {} # Cumulative counts for the whole batch
    
    # --- PROCESSING LOOP ---
    for i, file_path in enumerate(files):
        # Update Progress
        progress_bar.progress(i / len(files))
        status_text.info(f"🚀 Processing ({i+1}/{len(files)}): {file_path.name}")
        
        is_video = file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']
        
        # Native Ultralytics Stream
        # This handles reading images AND videos efficiently
        results_generator = model.predict(
            source=str(file_path),
            conf=conf_threshold,
            vid_stride=frame_stride, # Skips frames for speed
            stream=True,             # Generator mode (essential for live UI)
            save=True,               # Ultralytics handles saving images/videos to disk
            project=str(save_dir),   # Save inside our timestamped folder
            name=".",                # No extra subfolders
            exist_ok=True,
            verbose=False
        )
        
        frame_counter = 0
        
        for result in results_generator:
            # For video, this loop runs once per processed frame
            # For image, this loop runs exactly once
            frame_counter += 1
            
            # Check if we found anything
            if len(result.boxes) > 0:
                # 1. Update Global Counts & CSV Data
                for box in result.boxes:
                    name = result.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    
                    # Increment total count
                    total_mission_counts[name] = total_mission_counts.get(name, 0) + 1
                    
                    # Log for CSV
                    all_detections.append({
                        "File": file_path.name,
                        "Type": "Video" if is_video else "Image",
                        "Species": name,
                        "Confidence": round(conf, 4),
                        # Store roughly which frame (useful for video cross-ref)
                        "Frame_Index": frame_counter * frame_stride if is_video else "NA"
                    })
                
                # 2. Update Stats Table (Right Panel)
                # We create a DataFrame from the CUMULATIVE dictionary
                df = pd.DataFrame(list(total_mission_counts.items()), columns=["Species", "Total Count"])
                df = df.sort_values(by="Total Count", ascending=False)
                table_placeholder.dataframe(
                    df, 
                    hide_index=True, 
                    use_container_width=True, 
                    height=300
                )

                # 3. Update Image Viewer (Left Panel)
                annotated_frame = result.plot()
                # Convert BGR to RGB for Streamlit
                image_placeholder.image(
                    annotated_frame[..., ::-1], 
                    caption=f"Processing: {file_path.name}", 
                    use_container_width=True
                )

    # --- FINALIZE ---
    progress_bar.progress(100)
    status_text.success(f"✅ Batch Complete! Saved to: {save_dir.name}")
    
    if all_detections:
        # Save CSV
        csv_path = save_dir / "detection_report.csv"
        pd.DataFrame(all_detections).to_csv(csv_path, index=False)
        
        st.divider()
        st.success(f"📊 Detailed CSV report saved to: {csv_path}")
        
        # Final Summary Charts
        st.subheader("📈 Mission Summary")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Total Species Abundance**")
            st.bar_chart(pd.Series(total_mission_counts))
        with c2:
            st.write("**Detections by Media Type**")
            df_full = pd.DataFrame(all_detections)
            st.bar_chart(df_full['Type'].value_counts())
    else:
        status_text.warning("No benthic fauna detected in this batch.")

# --- 5. EXECUTION ---
if start_btn:
    if input_str and output_str:
        process_media()
    else:
        st.sidebar.error("⚠️ Please define both Input and Output folders.")