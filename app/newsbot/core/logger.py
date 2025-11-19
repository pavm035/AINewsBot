import logging


def setup_logger(level: int = logging.INFO):
    """Sets up a logger with the specified logging level.

    Args:
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
    """

    #
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.hasHandlers():
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        root_logger.addHandler(ch)

    print(
        f"Root logger ID: {id(root_logger)} with level: {logging.getLevelName(root_logger.level)}"
    )
    print(f"Root logger handlers: {root_logger.handlers}")
