# Added by Judy >>>>>>>>>>>>>>>>>>>>

import logging
from pathlib import Path

# RAGFlow logger
ragflow_logger = logging.getLogger("ragflow")


def get_file_type(file: str | Path) -> str | None:
    """
    Return the file type with lowercase if it exists. Otherwise, return `None`.

    Args:
        file (str | Path): The file name or file path.

    Returns:
        ftype (str | None): The file type with lowercase or `None`.

    Examples:
        >>> get_file_type("example.txt")
        ".txt"
        >>> get_file_type("/user/example.png")
        ".png"
        >>> get_file_type("/user/example")
        None
    """

    try:
        ftype = t if ( t := Path(file).suffix.lower() ) else None
    except Exception:
        ftype = None

    ragflow_logger.info(f"Find out the file type is '{ftype}' from file name '{Path(file).name}'.")
    return ftype

# <<<<<<<<<<<<<<<<<<<< Added by Judy
