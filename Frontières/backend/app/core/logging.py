"""
Logging - Millésime Sans Frontières
Configuration du système de logging
"""

import logging
import logging.config
from typing import Optional
from fastapi import FastAPI


def setup_logging(app: FastAPI, level: str = "INFO") -> None:
    """Configure le logging de l'application"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def setup_logging_with_custom_level(app: FastAPI, level: str = "INFO") -> None:
    """Configure le logging avec un niveau personnalisé"""
    setup_logging(app, level)


def get_logger(name: str) -> logging.Logger:
    """Récupère un logger configuré"""
    return logging.getLogger(name)


def log_request(request: dict, level: str = "INFO") -> None:
    """Log une requête HTTP"""
    logger = get_logger("http")
    log_level = getattr(logger, level.lower())
    log_level(f"Request: {request}")


def log_response(response: dict, level: str = "INFO") -> None:
    """Log une réponse HTTP"""
    logger = get_logger("http")
    log_level = getattr(logger, level.lower())
    log_level(f"Response: {response}")


def log_error(error: Exception, context: str = "") -> None:
    """Log une erreur avec contexte"""
    logger = get_logger("error")
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_performance(operation: str, duration: float, level: str = "INFO") -> None:
    """Log les performances d'une opération"""
    logger = get_logger("performance")
    log_level = getattr(logger, level.lower())
    log_level(f"Operation '{operation}' took {duration:.3f}s")
