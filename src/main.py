import yaml
import os
from tqdm import tqdm
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

    # Process IMU files with progress bar
    imu_files = files_map['imu']

    #TODO test IMU parser
    if imu_files:
        logger.info(f"Starting IMU Parser on {len(imu_files)} files...")
        
        results = []

        # Start tqdm loop
        for filepath in tqdm(imu_files, desc="IMU Parsing", unit="file"):
            try:
                # Run the parser
                data = parse_imu_file(filepath)
                if data is not None:
                    results.append(data)
                    # TODO: Here we would normally save 'data' to a CSV (file_finisher section to be implemented) to avoid filling up RAM
            except Exception as e:
                logger.error(f"Error processing {filepath}: {e}")

        if results is not None:
            print(f"\nSuccessfully parsed {len(results)}/{len(imu_files)} IMU files.")
            print(f"Shape: {results[0].shape}")
            #print(f"First 15 Readings (X, Y, Z): \n{results[0][:15]}")
            #print("------------------------------------------\n")
    else:
        logger.warning("No IMU files foud.")

if __name__ == "__main__":
    main()