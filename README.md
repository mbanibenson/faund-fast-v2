# Benthic Megafauna AI Detector

An AI platform designed for marine scientists to detect, count, and catalog benthic megafauna from seafloor image surveys and ROV video footage.

This application provides an intuitive dashboard interface to make predictions based on your fine-tuned YOLOv8 models. It is designed for ecological research, allowing you to process large visual datasets without writing code, while providing real-time abundance statistics and standardized data exports.

## Features

* **OS Agnostic:** Runs natively on Windows, macOS, and Linux/WSL.
* **Dual Media Support:** Process folders containing both static images (`.jpg`, `.png`) and high-resolution videos (`.mp4`, `.avi`, `.mov`).
* **Real-time Dashboard:** Watch a live feed of detections and track cumulative species abundance as the batch processes.
* **Scientific Export:** Automatically generates a detailed `detection_report.csv` containing species names, confidence scores, and frame/coordinate metadata.
* **Safe-Save Mode:** Every run creates a new timestamped folder, ensuring you never accidentally overwrite previous survey results.

---

## Installation (Recommended: Conda)

We recommend using Miniconda to manage the software. This keeps the AI libraries isolated so they don't interfere with your other computer applications.

### 1. Prerequisite: Install Miniconda
If you don't have it, download and install the version for your OS from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html).

### 2. Download this Project
Clone the repository (or download the ZIP and extract it) to your preferred location (e.g., `Desktop/Benthic_AI`).

```
git clone https://github.com/mbanibenson/faund-fast-v2.git
```

### 3. Setup the Environment
Open your terminal, navigate to the folder, and run the following commands:


#### Create the specialized environment
```
conda env create -f environment.yml
```

#### Activate the environment
```
conda activate benthic_env
```

## How to Launch the Tool

Every time you want to use the tool:

1.  Open your Terminal.
2.  Navigate to your project folder using `cd`.
3.  Run the following commands:

```
conda activate benthic_env
```
```
streamlit run app.py
```

## Using the Dashboard

1.  **Select Folders:** Paste the path to your Input folder (raw data) and Output folder (where results go).
2.  **Set Confidence:** Adjust the slider to determine how strict the AI should be.
    * **Low (0.25):** More likely to catch everything, but may have some false detections.
    * **High (0.50):** Very strict; only logs detections it is "sure" about.
3.  **Optimize Video:** For faster video processing, increase the Frame Stride (e.g., to 5 or 10) to skip identical frames while the ROV is moving slowly.
4.  **Click Start:** Watch the live feed. Once complete, your data will be waiting in the output folder.

## Understanding Your Output

Inside your timestamped results folder (e.g., `Run_2026-02-05_14-30`), you will find:

* **detection_report.csv:** A master spreadsheet for your statistical analysis.
* **Annotated Media:** Copies of your input files with boxes and labels drawn around the detected megafauna.
