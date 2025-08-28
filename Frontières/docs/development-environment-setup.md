### **Mise en Place de l'Environnement de Développement - Millésime Sans Frontières Backend**

**Version:** 1.0
**Date:** 27/08/2025

**1. Objectif**

Ce document fournit les instructions pas à pas pour configurer l'environnement de développement local du backend de Millésime Sans Frontières. Il couvre l'installation des prérequis, la configuration de la base de données et le lancement de l'application FastAPI.

**2. Prérequis**

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :

*   **Python 3.9+ :** Téléchargez depuis [python.org](https://www.python.org/downloads/).
*   **pip :** Généralement inclus avec Python.
*   **Docker Desktop :** Pour la gestion de la base de données PostgreSQL et d'autres services (ex: Redis pour Celery).
    *   Téléchargez depuis [docker.com](https://www.docker.com/products/docker-desktop).
*   **Git :** Pour cloner le dépôt du projet.
    *   Téléchargez depuis [git-scm.com](https://git-scm.com/downloads).
*   **Un éditeur de code :** Visual Studio Code (VS Code) est recommandé.
    *   Téléchargez depuis [code.visualstudio.com](https://code.visualstudio.com/).

**3. Configuration du Projet**

1.  **Cloner le dépôt Git :**
    Ouvrez votre terminal ou invite de commande et exécutez :
    ```bash
    git clone [URL_DU_DEPOT_GIT]
    cd millesime-sans-frontieres-backend # ou le nom du dossier du projet
    ```

2.  **Créer et activer un environnement virtuel :**
    Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.
    ```bash
    python -m venv venv
    # Sur Windows
    .\venv\Scripts\activate
    # Sur macOS/Linux
    source venv/bin/activate
    ```

3.  **Installer les dépendances Python :**
    Une fois l'environnement virtuel activé, installez toutes les bibliothèques requises :
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Le fichier `requirements.txt` sera créé lors du développement initial du projet.)*

**4. Configuration de la Base de Données (PostgreSQL avec Docker)**

1.  **Démarrer Docker Desktop :** Assurez-vous que Docker Desktop est en cours d'exécution sur votre machine.

2.  **Démarrer la base de données PostgreSQL :**
    Le projet inclura un fichier `docker-compose.yml` pour faciliter le démarrage des services nécessaires (base de données, Redis).
    ```bash
    docker-compose up -d postgres redis # ou simplement 'docker-compose up -d' si d'autres services sont définis
    ```
    *(Note: Les services exacts dépendront du `docker-compose.yml` final.)*

3.  **Exécuter les migrations de base de données :**
    Une fois la base de données démarrée, appliquez les migrations pour créer le schéma de la base de données.
    ```bash
    alembic upgrade head
    ```
    *(Note: `alembic` sera installé via `requirements.txt`.)*

**5. Lancement de l'Application Backend**

1.  **Définir les variables d'environnement :**
    Créez un fichier `.env` à la racine du projet et définissez les variables d'environnement nécessaires (ex: `DATABASE_URL`, `SECRET_KEY`). Un fichier `.env.example` sera fourni comme guide.
    ```ini
    # Exemple de contenu pour .env
    DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
    SECRET_KEY="votre_cle_secrete_jwt_tres_longue_et_complexe"
    # ... autres variables
    ```

2.  **Démarrer l'application FastAPI :**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *(Note: Le chemin `app.main:app` peut varier en fonction de la structure finale du projet.)*

    L'API sera accessible à l'adresse `http://localhost:8000`.

3.  **Accéder à la documentation de l'API :**
    *   **Swagger UI :** `http://localhost:8000/docs`
    *   **ReDoc :** `http://localhost:8000/redoc`

**6. Exécution des Tests**

*   Pour exécuter les tests unitaires et d'intégration :
    ```bash
    pytest
    ```

**7. Commandes de Développement Courantes**

*   **Linter (ex: Ruff) :**
    ```bash
    ruff check .
    ```
*   **Formateur de code (ex: Black) :**
    ```bash
    black .
    ```
*   **Arrêter les services Docker :**
    ```bash
    docker-compose down
    ```

