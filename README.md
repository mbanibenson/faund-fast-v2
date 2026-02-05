# Benthic Megafauna AI Detector

A specialized UI for marine scientists to detect, count, and catalog seafloor megafauna from image surveys and ROV video footage.

This application provides a "point-and-click" dashboard for your trained YOLOv8 models. It is designed for ecological research, allowing you to process large datasets without writing code, while providing real-time abundance statistics and standardized data exports.

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
Clone the repository or download the ZIP and extract it to your preferred location (e.g., `Desktop/Benthic_AI`).

### 3. Setup the Environment
Open your terminal (Mac/Linux) or Anaconda Prompt (Windows), navigate to the folder, and run the following commands:

```bash
# Create the specialized environment
conda env create -f environment.yml

# Activate the environment
conda activate benthic_env
