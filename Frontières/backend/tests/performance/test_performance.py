"""
Tests de performance pour l'API - Millésime Sans Frontières
"""

import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import statistics
import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.barrel import Barrel
from app.models.order import Order
from app.models.quote import Quote


class TestAPIPerformance:
    """Tests de performance pour l'API"""

    def test_homepage_response_time(self, client: TestClient):
        """Test du temps de réponse de la page d'accueil"""
        # Arrange
        expected_max_time = 0.1  # 100ms maximum
        
        # Act
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assert
        assert response.status_code == 200
        assert response_time < expected_max_time, f"Response time {response_time:.3f}s exceeds {expected_max_time}s"

    def test_health_check_response_time(self, client: TestClient):
        """Test du temps de réponse du health check"""
        # Arrange
        expected_max_time = 0.05  # 50ms maximum
        
        # Act
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assert
        assert response.status_code == 200
        assert response_time < expected_max_time, f"Response time {response_time:.3f}s exceeds {expected_max_time}s"

    def test_docs_response_time(self, client: TestClient):
        """Test du temps de réponse de la documentation"""
        # Arrange
        expected_max_time = 0.2  # 200ms maximum
        
        # Act
        start_time = time.time()
        response = client.get("/docs")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assert
        assert response.status_code == 200
        assert response_time < expected_max_time, f"Response time {response_time:.3f}s exceeds {expected_max_time}s"

    def test_openapi_schema_response_time(self, client: TestClient):
        """Test du temps de réponse du schéma OpenAPI"""
        # Arrange
        expected_max_time = 0.1  # 100ms maximum
        
        # Act
        start_time = time.time()
        response = client.get("/openapi.json")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assert
        assert response.status_code == 200
        assert response_time < expected_max_time, f"Response time {response_time:.3f}s exceeds {expected_max_time}s"


class TestDatabasePerformance:
    """Tests de performance pour la base de données"""

    def test_database_connection_time(self, db_session: Session):
        """Test du temps de connexion à la base de données"""
        # Arrange
        expected_max_time = 0.1  # 100ms maximum
        
        # Act
        start_time = time.time()
        
        # Test de connexion simple
        result = db_session.execute("SELECT 1")
        result.fetchone()
        
        end_time = time.time()
        
        connection_time = end_time - start_time
        
        # Assert
        assert connection_time < expected_max_time, f"Database connection time {connection_time:.3f}s exceeds {expected_max_time}s"

    def test_simple_query_performance(self, db_session: Session):
        """Test de performance d'une requête simple"""
        # Arrange
        expected_max_time = 0.05  # 50ms maximum
        
        # Act
        start_time = time.time()
        
        # Requête simple
        result = db_session.execute("SELECT COUNT(*) FROM users")
        count = result.scalar()
        
        end_time = time.time()
        
        query_time = end_time - start_time
        
        # Assert
        assert query_time < expected_max_time, f"Simple query time {query_time:.3f}s exceeds {expected_max_time}s"

    def test_complex_query_performance(self, db_session: Session):
        """Test de performance d'une requête complexe avec jointures"""
        # Arrange
        expected_max_time = 0.1  # 100ms maximum
        
        # Act
        start_time = time.time()
        
        # Requête complexe avec jointures
        result = db_session.execute("""
            SELECT u.email, COUNT(o.id) as order_count, SUM(oi.quantity * oi.unit_price) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY u.id, u.email
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        results = result.fetchall()
        
        end_time = time.time()
        
        query_time = end_time - start_time
        
        # Assert
        assert query_time < expected_max_time, f"Complex query time {query_time:.3f}s exceeds {expected_max_time}s"


class TestConcurrentRequests:
    """Tests de performance avec requêtes concurrentes"""

    def test_concurrent_homepage_requests(self, client: TestClient):
        """Test de performance avec requêtes concurrentes sur la page d'accueil"""
        # Arrange
        num_requests = 10
        expected_max_time = 0.5  # 500ms maximum pour toutes les requêtes
        
        # Act
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(client.get, "/")
                for _ in range(num_requests)
            ]
            
            responses = []
            for future in as_completed(futures):
                response = future.result()
                responses.append(response)
        
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Assert
        assert len(responses) == num_requests
        assert all(r.status_code == 200 for r in responses)
        assert total_time < expected_max_time, f"Total time for {num_requests} concurrent requests {total_time:.3f}s exceeds {expected_max_time}s"

    def test_concurrent_health_check_requests(self, client: TestClient):
        """Test de performance avec requêtes concurrentes sur le health check"""
        # Arrange
        num_requests = 20
        expected_max_time = 0.3  # 300ms maximum pour toutes les requêtes
        
        # Act
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(client.get, "/health")
                for _ in range(num_requests)
            ]
            
            responses = []
            for future in as_completed(futures):
                response = future.result()
                responses.append(response)
        
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Assert
        assert len(responses) == num_requests
        assert all(r.status_code == 200 for r in responses)
        assert total_time < expected_max_time, f"Total time for {num_requests} concurrent requests {total_time:.3f}s exceeds {expected_max_time}s"

    def test_concurrent_database_queries(self, db_session: Session):
        """Test de performance avec requêtes de base de données concurrentes"""
        # Arrange
        num_queries = 15
        expected_max_time = 0.2  # 200ms maximum pour toutes les requêtes
        
        # Act
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(lambda: db_session.execute("SELECT COUNT(*) FROM users").scalar())
                for _ in range(num_queries)
            ]
            
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Assert
        assert len(results) == num_queries
        assert all(isinstance(r, int) for r in results)
        assert total_time < expected_max_time, f"Total time for {num_queries} concurrent DB queries {total_time:.3f}s exceeds {expected_max_time}s"


class TestMemoryUsage:
    """Tests d'utilisation de la mémoire"""

    def test_memory_usage_simple_requests(self, client: TestClient):
        """Test de l'utilisation de la mémoire pour des requêtes simples"""
        # Arrange
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Act
        for _ in range(100):
            response = client.get("/health")
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert
        # L'augmentation de mémoire ne devrait pas dépasser 50MB
        assert memory_increase < 50, f"Memory increase {memory_increase:.1f}MB exceeds 50MB"

    def test_memory_usage_large_queries(self, db_session: Session):
        """Test de l'utilisation de la mémoire pour des requêtes volumineuses"""
        # Arrange
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Act
        for _ in range(10):
            # Requête qui pourrait retourner beaucoup de données
            result = db_session.execute("SELECT * FROM users")
            rows = result.fetchall()
            # Libérer la mémoire
            del rows
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert
        # L'augmentation de mémoire ne devrait pas dépasser 100MB
        assert memory_increase < 100, f"Memory increase {memory_increase:.1f}MB exceeds 100MB"


class TestResponseTimeDistribution:
    """Tests de distribution des temps de réponse"""

    def test_response_time_consistency(self, client: TestClient):
        """Test de la cohérence des temps de réponse"""
        # Arrange
        num_requests = 50
        endpoint = "/health"
        
        # Act
        response_times = []
        for _ in range(num_requests):
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Calculer les statistiques
        mean_time = statistics.mean(response_times)
        std_dev = statistics.stdev(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        # Assert
        # Le temps moyen devrait être inférieur à 100ms
        assert mean_time < 0.1, f"Mean response time {mean_time:.3f}s exceeds 100ms"
        
        # L'écart-type devrait être inférieur à 50ms
        assert std_dev < 0.05, f"Response time standard deviation {std_dev:.3f}s exceeds 50ms"
        
        # La différence entre min et max ne devrait pas dépasser 100ms
        time_range = max_time - min_time
        assert time_range < 0.1, f"Response time range {time_range:.3f}s exceeds 100ms"

    def test_response_time_percentiles(self, client: TestClient):
        """Test des percentiles des temps de réponse"""
        # Arrange
        num_requests = 100
        endpoint = "/health"
        
        # Act
        response_times = []
        for _ in range(num_requests):
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Trier les temps de réponse
        response_times.sort()
        
        # Calculer les percentiles
        p50 = response_times[int(0.5 * len(response_times))]
        p90 = response_times[int(0.9 * len(response_times))]
        p95 = response_times[int(0.95 * len(response_times))]
        p99 = response_times[int(0.99 * len(response_times))]
        
        # Assert
        # P50 (médiane) devrait être inférieur à 50ms
        assert p50 < 0.05, f"P50 response time {p50:.3f}s exceeds 50ms"
        
        # P90 devrait être inférieur à 80ms
        assert p90 < 0.08, f"P90 response time {p90:.3f}s exceeds 80ms"
        
        # P95 devrait être inférieur à 100ms
        assert p95 < 0.1, f"P95 response time {p95:.3f}s exceeds 100ms"
        
        # P99 devrait être inférieur à 150ms
        assert p99 < 0.15, f"P99 response time {p99:.3f}s exceeds 150ms"


class TestScalability:
    """Tests de scalabilité"""

    def test_scalability_with_increasing_load(self, client: TestClient):
        """Test de scalabilité avec charge croissante"""
        # Arrange
        load_levels = [10, 25, 50, 100]
        endpoint = "/health"
        
        # Act
        results = {}
        for load in load_levels:
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=min(load, 20)) as executor:
                futures = [
                    executor.submit(client.get, endpoint)
                    for _ in range(load)
                ]
                
                responses = []
                for future in as_completed(futures):
                    response = future.result()
                    responses.append(response)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            results[load] = {
                "total_time": total_time,
                "requests_per_second": load / total_time,
                "all_successful": all(r.status_code == 200 for r in responses)
            }
        
        # Assert
        # Toutes les requêtes devraient réussir
        for load, result in results.items():
            assert result["all_successful"], f"Not all requests successful at load {load}"
        
        # Le débit devrait rester raisonnable même sous charge
        for load, result in results.items():
            assert result["requests_per_second"] > 50, f"Throughput too low at load {load}: {result['requests_per_second']:.1f} req/s"

    def test_database_scalability(self, db_session: Session):
        """Test de scalabilité de la base de données"""
        # Arrange
        query_counts = [10, 25, 50, 100]
        
        # Act
        results = {}
        for count in query_counts:
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=min(count, 20)) as executor:
                futures = [
                    executor.submit(lambda: db_session.execute("SELECT COUNT(*) FROM users").scalar())
                    for _ in range(count)
                ]
                
                query_results = []
                for future in as_completed(futures):
                    result = future.result()
                    query_results.append(result)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            results[count] = {
                "total_time": total_time,
                "queries_per_second": count / total_time,
                "all_successful": all(isinstance(r, int) for r in query_results)
            }
        
        # Assert
        # Toutes les requêtes devraient réussir
        for count, result in results.items():
            assert result["all_successful"], f"Not all queries successful at count {count}"
        
        # Le débit devrait rester raisonnable même avec beaucoup de requêtes
        for count, result in results.items():
            assert result["queries_per_second"] > 100, f"Database throughput too low at count {count}: {result['queries_per_second']:.1f} queries/s"


class TestStressTesting:
    """Tests de stress"""

    def test_stress_test_health_endpoint(self, client: TestClient):
        """Test de stress sur l'endpoint de santé"""
        # Arrange
        num_requests = 500
        max_workers = 50
        expected_success_rate = 0.95  # 95% de succès minimum
        
        # Act
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(client.get, "/health")
                for _ in range(num_requests)
            ]
            
            responses = []
            for future in as_completed(futures):
                try:
                    response = future.result()
                    responses.append(response)
                except Exception as e:
                    responses.append({"error": str(e)})
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculer le taux de succès
        successful_responses = [r for r in responses if hasattr(r, 'status_code') and r.status_code == 200]
        success_rate = len(successful_responses) / len(responses)
        
        # Assert
        assert success_rate >= expected_success_rate, f"Success rate {success_rate:.2%} below expected {expected_success_rate:.2%}"
        assert total_time < 30, f"Stress test took too long: {total_time:.1f}s"

    def test_stress_test_database(self, db_session: Session):
        """Test de stress sur la base de données"""
        # Arrange
        num_queries = 1000
        max_workers = 50
        expected_success_rate = 0.95  # 95% de succès minimum
        
        # Act
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(lambda: db_session.execute("SELECT COUNT(*) FROM users").scalar())
                for _ in range(num_queries)
            ]
            
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculer le taux de succès
        successful_results = [r for r in results if isinstance(r, int)]
        success_rate = len(successful_results) / len(results)
        
        # Assert
        assert success_rate >= expected_success_rate, f"Success rate {success_rate:.2%} below expected {expected_success_rate:.2%}"
        assert total_time < 60, f"Database stress test took too long: {total_time:.1f}s"


class TestPerformanceMonitoring:
    """Tests de monitoring des performances"""

    def test_performance_metrics_collection(self, client: TestClient):
        """Test de collecte des métriques de performance"""
        # Arrange
        num_requests = 100
        endpoint = "/health"
        
        # Act
        metrics = {
            "response_times": [],
            "status_codes": [],
            "errors": []
        }
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = client.get(endpoint)
                end_time = time.time()
                
                response_time = end_time - start_time
                metrics["response_times"].append(response_time)
                metrics["status_codes"].append(response.status_code)
                
            except Exception as e:
                metrics["errors"].append(str(e))
        
        # Calculer les métriques
        if metrics["response_times"]:
            avg_response_time = statistics.mean(metrics["response_times"])
            max_response_time = max(metrics["response_times"])
            min_response_time = min(metrics["response_times"])
            
            # Assert
            assert avg_response_time < 0.1, f"Average response time {avg_response_time:.3f}s too high"
            assert max_response_time < 0.2, f"Max response time {max_response_time:.3f}s too high"
            assert min_response_time < 0.05, f"Min response time {min_response_time:.3f}s too high"
        
        # Vérifier le taux d'erreur
        error_rate = len(metrics["errors"]) / num_requests
        assert error_rate < 0.05, f"Error rate {error_rate:.2%} too high"

    def test_performance_regression_detection(self, client: TestClient):
        """Test de détection de régression de performance"""
        # Arrange
        baseline_requests = 50
        current_requests = 50
        endpoint = "/health"
        regression_threshold = 1.5  # 50% de dégradation maximum
        
        # Collecter les données de référence
        baseline_times = []
        for _ in range(baseline_requests):
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            assert response.status_code == 200
            baseline_times.append(end_time - start_time)
        
        baseline_avg = statistics.mean(baseline_times)
        
        # Collecter les données actuelles
        current_times = []
        for _ in range(current_requests):
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            assert response.status_code == 200
            current_times.append(end_time - start_time)
        
        current_avg = statistics.mean(current_times)
        
        # Calculer le ratio de performance
        performance_ratio = current_avg / baseline_avg
        
        # Assert
        assert performance_ratio < regression_threshold, f"Performance regression detected: ratio {performance_ratio:.2f} exceeds threshold {regression_threshold}"
