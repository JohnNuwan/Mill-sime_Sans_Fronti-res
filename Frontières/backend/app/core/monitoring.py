"""
Monitoring - Millésime Sans Frontières
Configuration du système de monitoring
"""

from fastapi import FastAPI
import time
from collections import defaultdict
from typing import Dict, Any, Optional


class MetricsCollector:
    """Collecteur de métriques simple"""
    
    def __init__(self):
        self.metrics = defaultdict(int)
        self.timings = defaultdict(list)
    
    def increment(self, metric_name: str, value: int = 1) -> None:
        """Incrémente une métrique"""
        self.metrics[metric_name] += value
    
    def record_timing(self, operation: str, duration: float) -> None:
        """Enregistre le temps d'une opération"""
        self.timings[operation].append(duration)
    
    def get_metric(self, metric_name: str) -> int:
        """Récupère la valeur d'une métrique"""
        return self.metrics[metric_name]
    
    def get_timing_stats(self, operation: str) -> Dict[str, float]:
        """Récupère les statistiques de timing d'une opération"""
        timings = self.timings[operation]
        if not timings:
            return {"count": 0, "avg": 0.0, "min": 0.0, "max": 0.0}
        
        return {
            "count": len(timings),
            "avg": sum(timings) / len(timings),
            "min": min(timings),
            "max": max(timings)
        }
    
    def reset(self) -> None:
        """Réinitialise toutes les métriques"""
        self.metrics.clear()
        self.timings.clear()


# Instance globale du collecteur de métriques
metrics_collector = MetricsCollector()


def setup_monitoring(app: FastAPI, metrics: Dict[str, Any] = None) -> None:
    """Configure le monitoring de l'application"""
    # Configuration basique du monitoring
    if metrics:
        for metric_name, value in metrics.items():
            metrics_collector.increment(metric_name, value)


def setup_monitoring_with_custom_metrics(app: FastAPI, metrics: Dict[str, Any] = None) -> None:
    """Configure le monitoring avec des métriques personnalisées"""
    if metrics:
        for metric_name, value in metrics.items():
            metrics_collector.increment(metric_name, value)


def record_request_metric(endpoint: str, method: str, status_code: int, duration: float) -> None:
    """Enregistre les métriques d'une requête"""
    metrics_collector.increment(f"requests_total")
    metrics_collector.increment(f"requests_{method.lower()}")
    metrics_collector.increment(f"requests_{status_code}")
    metrics_collector.record_timing(f"request_duration_{endpoint}", duration)


def record_database_metric(operation: str, duration: float, success: bool) -> None:
    """Enregistre les métriques de base de données"""
    metrics_collector.increment(f"db_operations_total")
    metrics_collector.increment(f"db_operations_{operation}")
    if success:
        metrics_collector.increment(f"db_operations_{operation}_success")
    else:
        metrics_collector.increment(f"db_operations_{operation}_error")
    metrics_collector.record_timing(f"db_duration_{operation}", duration)


def get_metrics_summary() -> Dict[str, Any]:
    """Récupère un résumé des métriques"""
    return {
        "total_requests": metrics_collector.get_metric("requests_total"),
        "db_operations": metrics_collector.get_metric("db_operations_total"),
        "timing_stats": {
            operation: metrics_collector.get_timing_stats(operation)
            for operation in metrics_collector.timings.keys()
        }
    }


def reset_metrics() -> None:
    """Réinitialise toutes les métriques"""
    metrics_collector.reset()
