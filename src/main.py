import yaml
import logging
import os
from src.core.logger import setup_logger
from src.core.crawler import find_raw_files

def load_config(config_path="config.yaml"):
    """Loads configuration from the YAML file"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main():
    
    # Setup Logging
    logger = setup_logger("vesper_automator", log_dir="./logs")
    logger.info("Vesper Automator started.")

    # Load Config
    try:
        config = load_config()
        logger.info("Configuration loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return
    
    #TODO testing file crawler
    raw_folder = config.get("raw_data_folder")
    files_map = find_raw_files(raw_folder)

    #TODO temporary testing prints
    print("\n--- TEST RESULTS ---")
    print(f"GPS Files: {len(files_map['gps'])}")
    print(f"Audio Files: {len(files_map['aud'])}")
    print(f"IMU Files: {len(files_map['imu'])}")
    print("--------------------\n")

    logging.warning('Watch Out!')

if __name__ == "__main__":
    main()