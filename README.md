> **DISCLAIMER** This is an unofficial, independent research tool developed by students at the University of Göttingen for the German Primate Center (DPZ). It is **not** affiliated with, authorized, or endorsed by A.S.D. (Alexander Schwartz Developments). All product names are property of their respective owners and are used here solely for identification and compatibility purposes.

🐒 ⚙️ WildlifeTag Automator
=====================

A specialized automation pipeline for decoding, processing, and organizing multi-sensor data from Vesper Wildlife Tags.

> **Update (Alpha v0.1):** This tool now features custom reverse-engineered parsers for **IMU** (`.BIN`), **Audio** (`.BIN`), and **GPS** (`.BIN`) data. It significantly reduces dependency on proprietary software by natively handling binary decoding, artifact removal, and timestamp synchronization.

🛠️ Build & Quick Start
-----------------------

### 1\. Prerequisites

*   **Python 3.12+**
*   **Vesper GeoTag.exe** (Required _only_ for the final step of converting processed `.DAT` files into coordinates).
*   **Windows 10/11** (Recommended if using legacy GPS tools).

### 2\. Installation

Clone the repository:

    git clone https://github.com/dasilva98/wildlifetag-automator
    cd wildlifetag-automator

Set up the virtual environment:

    # Create environment
    python -m venv .venv
    
    # Activate (Windows)
    .venv\Scripts\activate
    
    # Activate (Linux/Mac)
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

### 3\. Configuration

1.  Open `config.yaml`.
2.  Update `raw_data_folder` to point to your input directory.
3.  Update `processed_folder` to point to where you want the results.

### 4\. Running the Tool

To run the main processing pipeline:

    python -m src.main

🧰 Diagnostic Tools
-------------------

We include standalone analyzers for inspecting raw binary files and diagnosing signal integrity issues.

### 1\. Metadata & Header Analyzer (IMU/General)

    # Check metadata and hidden timestamps
    python src/utils/bin_analyzer.py data/raw/00M.BIN
    
    # Inspect header hex dump (first 200 bytes)
    python src/utils/bin_analyzer.py data/raw/00M.BIN --hex

### 2\. Audio Signal Diagnostics

    # Diagnose signal discontinuities and periodicity
    python src/utils/audio_diagnose.py data/raw/0U.BIN

📂 Project Structure
--------------------

    wildlifetag-automator/
    ├── config.yaml              # Global settings and paths
    ├── LICENSE                  # GNU GPLv3 License
    ├── build_exe.py             # PyInstaller script for standalone builds
    ├── data/                    # Data storage (Ignored by Git)
    │   ├── raw/                 # Input .BIN files
    │   └── processed/           # Final Output files (WAV, CSV, Metadata)
    ├── src/
    │   ├── main.py              # Pipeline entry point
    │   ├── core/                # Crawler, Logger, Finisher logic
    │   ├── utils/               # Shared utilities
    │   │   └── bin_analyzer.py  # Binary format inspector & debugger
    │   ├── parsers/             # Native Python decoders
    │   │   ├── imu_parser.py    # Decodes 10-DOF sensor data to CSV
    │   │   ├── audio_parser.py  # Decodes PCM Audio + Artifact Removal
    │   │   └── gps_parser.py    # Decodes GPS Binary to Snapshot (.DAT)
    │   └── wrappers/            # External tool wrappers
    └── tests/                   # Unit tests

🧪 Technical Features
---------------------

The native parsers automatically handle specific hardware quirks found in the raw binary files:

### IMU Processing

*   Converts raw binary directly to Legacy CSV Format (split columns) for compatibility with existing research workflows.
*   Calculates precise millisecond timestamps using vectorized operations.

### Audio Processing

*   **Startup Pop Removal:** Trims the initial ~17ms of sensor wake-up noise.
*   **Click Removal:** Surgically removes the 14-byte metadata footers inserted every 64KB, ensuring seamless audio.

### GPS Processing

*   Parses header data and performs bitwise "Word Swapping" on I/Q data to generate valid Snapshot files.

🤝 Contribution Guidelines
--------------------------

We follow Conventional Commits. Please format commit messages as follows:

*   `Feat: Add native Audio parser`
*   `Fix: Resolve 64KB block clicking noise`
*   `Docs: Update tools usage`
*   `Refactor: Optimize file crawler`

**Important:** Do not commit raw data files (.BIN, .DAT) or the virtual environment (.venv/).

⚖️ Legal Notice & Disclaimer
----------------------------

WildlifeTag Automator (the "Software") is an unofficial, independent, open-source tool.

**1\. Non-Affiliation:** This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with A.S.D. (Alexander Schwartz Developments), or any of its subsidiaries. The official A.S.D. website can be found at [asd-tech.com](https://asd-tech.com).

**2\. Trademarks:** The names Vesper, VesperTag, and VesperApp are registered trademarks of A.S.D. Use of these names within this project is strictly for nominative purposes to identify the specific hardware data formats this tool is designed to process.

**3\. Independent Implementation:** While public documentation and legacy references were consulted to understand data structures, this Software was built from scratch. The processing architecture was independently developed using modern data science libraries to ensure high performance and data integrity. No source code was translated or ported from the original manufacturer's software.
