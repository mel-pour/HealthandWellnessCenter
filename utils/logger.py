import logging
from pathlib import Path


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        project_folder = Path(__file__).resolve().parent.parent
        log_folder = project_folder / "logs"
        log_folder.mkdir(exist_ok=True)

        log_file = log_folder / "healthcare_center.log"

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger