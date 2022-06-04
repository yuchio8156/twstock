# -*- coding: utf-8 -*-

import logging
import logging.handlers

from datetime import datetime


def get_logger(
        name: str, 
        level: int=logging.INFO, 
        ) -> logging.RootLogger: 
    """
    Manage logs
    
    Args:
        name (dict): log name
        level (int): log level
            
    Returns:
        logger (logging.RootLogger): log manager
    """
    
    today = datetime.today().strftime("%Y%m%d")
    filename = f"./{today}.log"
    
    # create handler
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename)
    
    # create formatter
    console_format = logging.Formatter("%(name)s %(levelname)s: %(message)s")
    file_format = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)8s: %(message)s")
    
    # add formatter to handler
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # logger
    logging.root.setLevel(level)
    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__": 
    logger = get_logger(name="test", level=logging.WARNING)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")