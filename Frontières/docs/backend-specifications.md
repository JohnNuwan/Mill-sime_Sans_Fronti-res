### **Spécifications du Backend - Millésime Sans Frontières**

**Version:** 1.3
**Date:** 27/08/2025

**Note sur le niveau de détail :** Ce document présente une vue d'ensemble des spécifications du backend. Chaque section pourra être approfondie et détaillée dans des documents ou des étapes ultérieures (ex: spécifications détaillées des API, schéma de base de données complet).

**1. Objectif**

Ce document décrit les spécifications techniques et fonctionnelles du backend pour le site e-commerce de fûts de vin "Millésime Sans Frontières". Le backend sera responsable de la gestion des données, de la logique métier, de l'authentification et de l'exposition des API nécessaires au fonctionnement du frontend.

**2. Technologies Clés**

*   **Langage de Programmation:** Python
*   **Framework Web API:** FastAPI
    *   *Avantages:* Haute performance, validation des données automatique (Pydantic), documentation interactive (Swagger UI/ReDoc).
*   **Base de Données:** PostgreSQL (recommandé pour sa robustesse et ses fonctionnalités avancées)
    *   *Alternative simple pour le développement initial:* SQLite (pour la rapidité de mise en place)
*   **ORM (Object-Relational Mapper):** SQLAlchemy (avec Alembic pour les migrations de base de données)
*   **Authentification:** JWT (JSON Web Tokens)
*   **Conteneurisation:** Docker (pour un déploiement et une gestion facilités)

**3. Responsabilités Principales du Backend**

Le backend gérera les fonctionnalités suivantes via des API RESTful :

*   **Gestion des Produits (Fûts):**
    *   Création, lecture, mise à jour, suppression (CRUD) des fûts.
    *   Gestion des stocks (quantités disponibles, statut).
    *   Recherche et filtrage des fûts.
*   **Gestion des Utilisateurs:**
    *   Enregistrement et connexion des utilisateurs (B2C et B2B).
    *   Gestion des profils utilisateurs (adresses, informations de contact).
    *   Gestion des rôles et permissions (administrateur, client B2B, client B2C).
*   **Gestion des Commandes:**
    *   Création et suivi des commandes.
    *   Mise à jour du statut des commandes.
    *   Historique des commandes par utilisateur.
*   **Gestion des Devis:**
    *   Création, suivi et gestion des demandes de devis B2B.
    *   Génération de devis personnalisés.
*   **Intégration des Paiements:**
    *   Interface avec des passerelles de paiement sécurisées (ex: Stripe, PayPal).
    *   Gestion des transactions et des remboursements.
*   **Logistique et Expédition:**
    *   Intégration potentielle avec des APIs de transporteurs pour le calcul des frais et le suivi.
    *   Génération de documents d'expédition.
*   **Gestion du Contenu (CMS léger):**
    *   API pour la gestion des pages statiques (About Us, Contact, FAQ) si non géré par un CMS externe.

**4. Modèle de Données (Haut Niveau)**

*   **`Users`:** `id`, `email`, `password_hash`, `role` (`admin`, `b2b`, `b2c`), `first_name`, `last_name`, `company_name` (pour B2B), `address_id`.
*   **`Addresses`:** `id`, `street`, `city`, `zip_code`, `country`.
*   **`Barrels`:** `id`, `name`, `origin_country`, `previous_content`, `volume_liters`, `wood_type`, `condition`, `price`, `stock_quantity`, `description`, `image_urls`.
*   **`Orders`:** `id`, `user_id`, `order_date`, `total_amount`, `status` (`pending`, `processing`, `shipped`, `delivered`, `cancelled`), `shipping_address_id`.
*   **`OrderItems`:** `id`, `order_id`, `barrel_id`, `quantity`, `price_at_purchase`.
*   **`Quotes`:** `id`, `user_id`, `request_date`, `status` (`pending`, `approved`, `rejected`), `requested_items` (JSON), `quoted_price`, `notes`.

**5. Sécurité et Authentification**

*   **Authentification:** Basée sur des JWT (JSON Web Tokens) pour sécuriser l'accès aux API.
*   **Autorisation:** Implémentation de rôles pour contrôler l'accès aux différentes ressources (ex: seuls les administrateurs peuvent créer/modifier des fûts).
*   **Validation des Données:** Utilisation de Pydantic pour la validation automatique des requêtes entrantes.
*   **Protection:** Contre les attaques courantes (SQL injection, XSS, CSRF) via les fonctionnalités intégrées de FastAPI et les bonnes pratiques.
*   **Chiffrement des données:** Les données sensibles (mots de passe, informations de paiement) seront chiffrées au repos et en transit.
*   **Limitation de Taux (Rate Limiting):** Mise en place de mécanismes pour prévenir les abus et les attaques par déni de service (DoS) sur les endpoints API.

**6. Principes de Conception des API**

*   **RESTful:** Utilisation des méthodes HTTP standard (GET, POST, PUT, DELETE) et des codes de statut appropriés.
*   **Clarté et Cohérence:** Noms de ressources clairs et cohérents.
*   **Documentation:** Génération automatique de la documentation API (Swagger UI/ReDoc) pour faciliter l'intégration frontend.
*   **Gestion des Erreurs:** Réponses d'erreur claires et informatives.
*   **Versionning des API:** Utilisation d'un schéma de versionning (ex: `/v1/barrels`) pour permettre l'évolution de l'API sans casser la compatibilité avec les clients existants.

**7. Déploiement**

*   Le backend sera conteneurisé avec Docker pour assurer la portabilité et la reproductibilité de l'environnement.
*   Déploiement envisagé sur un service cloud (ex: AWS, Google Cloud, Azure) ou un VPS.

**8. Conformité et Réglementation**

*   **RGPD (Règlement Général sur la Protection des Données) :** Le backend sera conçu en conformité avec les principes de la RGPD, notamment :
    *   **Minimisation des données :** Collecte uniquement des données nécessaires.
    *   **Droit des personnes :** Mise en place de mécanismes pour permettre aux utilisateurs d'exercer leurs droits (accès, rectification, suppression, portabilité de leurs données).
    *   **Sécurité des données :** Mesures techniques et organisationnelles appropriées pour protéger les données personnelles.
    *   **Consentement :** Gestion du consentement pour la collecte et le traitement des données.
*   **Autres réglementations :** Prise en compte des réglementations spécifiques au commerce international et à la vente de produits liés à l'alcool (si applicable à la vente de fûts).

**9. Aspects Techniques Détaillés**

*   **Gestion des Logs et Monitoring :**
    *   Implémentation d'un système de logging structuré (ex: JSON logs) pour faciliter l'analyse.
    *   Définition de niveaux de logs (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    *   Intégration avec des outils de monitoring (ex: Prometheus, Grafana) pour la surveillance des performances et des erreurs en production.
*   **Gestion des Erreurs :**
    *   Définition d'exceptions personnalisées pour les erreurs métier spécifiques.
    *   Mise en place d'un gestionnaire d'erreurs global pour uniformiser les réponses d'erreur de l'API.
    *   Enregistrement des erreurs critiques dans les logs.
*   **Stratégie de Tests :**
    *   **Tests Unitaires :** Pour valider le bon fonctionnement des fonctions et classes individuelles.
    *   **Tests d'Intégration :** Pour vérifier l'interaction entre les différents composants (ex: API et base de données).
    *   **Tests End-to-End (E2E) :** Pour simuler des scénarios utilisateur complets (potentiellement avec un framework de test comme Playwright ou Selenium si le frontend est intégré).
*   **Gestion de la Configuration :**
    *   Utilisation de variables d'environnement pour les configurations sensibles (clés API, identifiants de base de données).
    *   Chargement des configurations via des bibliothèques comme `python-dotenv` ou `Dynaconf`.
*   **Tâches en Arrière-plan (Background Tasks) :**
    *   Utilisation d'un système de file d'attente de tâches (ex: Celery avec Redis ou RabbitMQ) pour les opérations longues ou asynchrones (envoi d'emails de confirmation, traitement de commandes complexes, génération de rapports).
*   **Mise en Cache (Caching) :**
    *   Mise en place d'un mécanisme de cache (ex: Redis) pour les données fréquemment accédées afin d'améliorer les performances de l'API et réduire la charge sur la base de données.
*   **Reporting et Analyse de Données :**
    *   **Web Analytics :** Intégration avec des outils d'analyse web (ex: Google Analytics) pour suivre le comportement des utilisateurs sur le site (pages vues, clics, parcours utilisateur, taux de conversion).
    *   **Rapports Métier (Business Intelligence) :**
        *   Génération de rapports à partir des données du backend (ventes, stock, clients, devis, performance des produits).
        *   Possibilité de créer des tableaux de bord personnalisés pour les administrateurs.
        *   Exportation des données pour des analyses plus poussées (ex: CSV, Excel).

**10. Prochaines Étapes**

*   Conception détaillée du schéma de base de données.
*   Définition précise de chaque endpoint API (URL, méthodes HTTP, paramètres, réponses).
*   Mise en place de l'environnement de développement.