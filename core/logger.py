# app/core/logger.py

import logging

def get_logger(name: str = "school_api") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if re-imported
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger

# Default logger instance
logger = get_logger()
