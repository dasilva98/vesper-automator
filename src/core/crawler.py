import os
import logging

logger = logging.getLogger("vesper_automator")

def find_raw_files(root_folder):
    """
    Scans root_folder to find all .BIN files
    Returns a dictionary organizing files by sensor type(GPS, AUD, IMU)
    """

    logger.info(f"Scanning for files in: {root_folder}")

    files_map = {
        "gps": [],
        "aud": [],
        "imu": []
    }

    if not os.path.exists(root_folder):
        logger.error(f"Raw data folder not found: {root_folder}")
        return files_map
    

    count = 0
    # Recursively walk through every folder and subfolder
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.upper().endswith(".BIN"):
                full_path = os.path.join(dirpath, filename)

                # Simple logic to guess sensor type based on folder/file name
                #TODO we need to understand if we want to check all collar folder or just one specific(depends on what the user wants)
                lower_path = full_path.lower()
                if "gps" in lower_path:
                    files_map["gps"].append(full_path)
                elif "aud" in lower_path:
                    files_map["aud"].append(full_path)
                elif "imu" in lower_path:
                    files_map["imu"].append(full_path)
                else:
                    logger.warning(f"Unkown sensor type for files: {filename}")

                count += 1

    logger.info(f"Scan complete. Found {count} total binary files.")
    logger.info(f"  - GPS: {len(files_map['gps'])}")
    logger.info(f"  - IMU: {len(files_map['imu'])}")
    logger.info(f"  - Audio: {len(files_map['aud'])}")
    
    return files_map