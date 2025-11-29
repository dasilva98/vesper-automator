# Vesper Automator

A specialized tool for automating the decoding, processing, and organization of multi-sensor data from Vesper Wildlife Tags.

## 🚀 Quick Start

### 1. Prerequisites

- **Windows 10/11** (Required for VesperApp and GeoTag.exe integration).
    
- **Python 3.12+** installed.
    
- **VesperApp** installed (default path assumed).
    

### 2. Installation

Clone the repository:

```
git clone https://github.com/dasilva98/vesper-automator
cd vesper-automator
```

Set up the virtual environment:

```
# Create environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

### 3. Configuration

1. Open `config.yaml`.
    
2. Update the `vesper_app_path` and `gps_cli_path` to match the actual installation paths on your machine.
    
3. Set your raw data folder path.
    

### 4. Running the Tool

To run the main pipeline:

```
python -m src.main
```

## 📂 Project Structure

```
vesper-automator/
├── config.yaml              # Global settings and paths
├── data/                    # Data storage (Ignored by Git)
│   ├── raw/                 # Input .BIN files
│   └── processed/           # Final Output files
├── src/
│   ├── core/                # Crawler, Logger, Finisher logic
│   ├── parsers/             # Native Python decoders (IMU/Audio)
│   └── wrappers/            # External tool wrappers (GPS CLI, GUI Automator)
└── tests/                   # Unit tests
```

## 🤝 Contribution Guidelines

We follow **Conventional Commits**. By formatting commit messages as follows:

- `Feat: Add IMU parser logic`
    
- `Fix: Resolve path error in config`
    
- `Docs: Update installation steps`
    
- `Refactor: Clean up crawler loop`

- `Chore: Update project config`
    
**Do not commit raw data files (`.BIN`, `.DAT`) or the virtual environment (`.venv/`)**.