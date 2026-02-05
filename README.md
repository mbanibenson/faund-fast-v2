🌊 Benthic Megafauna AI Detector
A simple tool for marine scientists to detect, count, and catalog seafloor megafauna from image surveys and ROV video footage.

This application provides a "point-and-click" interface for your trained YOLOv8 model. It allows you to process entire folders of data and exports the results into a standardized CSV format for ecological analysis.

🛠 1. Getting Set Up (First Time Only)
We recommend using Miniconda to manage the software. This ensures that the AI libraries do not interfere with other software on your computer.

A. Install Miniconda
If you don't have it, download and install the version for your computer:

Windows/Mac/Linux: Download Miniconda here

B. Download this Project
Click the green Code button at the top of this GitHub page and select Download ZIP.

Extract the ZIP folder to a place you can find easily (e.g., your Desktop).

C. Create the Environment
Open your Terminal (on Mac/Linux) or Anaconda Prompt (on Windows).

Navigate to the folder you just extracted:

Bash

cd Desktop/benthic-megafauna-ui
Create the automatic environment:

Bash

conda env create -f environment.yml
Activate the environment:

Bash

conda activate benthic_env
🚀 2. How to Run the App
Every time you want to use the tool, follow these 3 simple steps:

Open your terminal/prompt.

Activate the environment:

Bash

conda activate benthic_env
Launch the dashboard:

Bash

streamlit run app.py
Your web browser will automatically open a new tab showing the dashboard.

🖥 3. Using the Dashboard
Step 1: Set Your Folders
Input Folder: Paste the full path to where your raw images (.jpg, .png) or videos (.mp4, .mov) are stored.

Output Folder: Paste the path where you want the results saved.

Note: The app will create a new sub-folder here named with today's date and time (e.g., Run_2026-02-05_14-30) so you never overwrite your work.

Step 2: Configure the AI
Confidence Threshold: Adjust how "sure" the AI must be before it logs a detection.

Lower (0.20): More detections, but may include some "false alarms" (rocks that look like sponges).

Higher (0.60): Fewer detections, but very reliable.

Video Stride: If processing video, setting this to 5 or 10 makes the process much faster by skipping frames where the ROV hasn't moved much.

Step 3: Start Detection
Click 🚀 Start Detection. You will see:

Live View: The most recent detection found by the AI.

Cumulative Counts: A running total of every species found in the entire folder so far.

📊 4. The Results (Output)
Once the bar hits 100%, check your Output Folder. Inside the timestamped run folder, you will find:

detection_report.csv: A spreadsheet containing every single detection, the species name, the AI's confidence, and the exact coordinates (x, y) where it was found.

Annotated Media: Copies of your images and videos with boxes drawn around the detected fauna.

❓ Troubleshooting
"Input folder not found": Ensure there are no quotes (") at the start or end of the path you pasted into the box.

"Model not found": Ensure your trained model file (e.g., best.pt) is placed inside the models/ folder within the project.

App is slow: If you are processing 4K video, increase the Video Stride to 10 or 15.
