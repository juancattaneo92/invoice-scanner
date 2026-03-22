"""
Invoice Scanner: Centralized logging configuration
This file sets up centralized logging for your entire application. 
This logger records what's happening, when it happened, and how serious it is.
"""
from loguru import logger
import sys
from src.shared.config import LOG_LEVEL

# Remove default logger
logger.remove()

# Add logger to terminal with custom format
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL
)

# Add logger to file with rotation and retention (Set to Debug for development, can be set to LOG_LEVEL.
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} - {message}",
    level="DEBUG",
    rotation="500 MB"
)

# Export logger for use in other modules
__all__ = ["logger"]