import yaml
import os
from src.core.logger import setup_logger
from src.core.crawler import find_raw_files
from src.parsers.imu_parser import parse_imu_file

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
    
    # Crawl files
    raw_folder = config.get("raw_data_folder")
    files_map = find_raw_files(raw_folder)

    #TODO temporary testing prints
    print("\n--- TEST RESULTS ---")
    print(f"GPS Files: {len(files_map['gps'])}")
    print(f"Audio Files: {len(files_map['aud'])}")
    print(f"IMU Files: {len(files_map['imu'])}")
    print("--------------------\n")

    #TODO test IMU parser
    if files_map['imu']:
        logger.info("--- Testing IMU Parser ---")
        # Grab the first file found to test
        test_file = files_map['imu'][0]

        # Run the parser
        result = parse_imu_file(test_file)

        if result is not None:
            print(f"\nSUCCESS: Parsed {os.path.basename(test_file)}")
            print(f"Shape: {result.shape}") # type: ignore 
            print(f"First 15 Readings (X, Y, Z): \n{result[:15]}")
            print("------------------------------------------\n")
    else:
        logger.warning("No IMU files foud to test.")

if __name__ == "__main__":
    main()