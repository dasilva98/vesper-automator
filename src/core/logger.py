import logging
import os
from datetime import datetime

def setup_logger(name, log_dir="."):
    """Sets up a logger that writes to console and a file."""
    
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a unique log filename based on time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"vesper_run_{timestamp}.log")

    # Configure the logging system
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),    # Write to file
            logging.StreamHandler()           # Write to terminal
        ]
    )

    logger = logging.getLogger(name)
    return logger