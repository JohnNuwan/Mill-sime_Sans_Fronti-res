# Backend FastAPI - Millésime Sans Frontières

## 🚀 **Démarrage Rapide**

### **Prérequis**
- Python 3.9+
- Docker et Docker Compose
- pip (gestionnaire de paquets Python)

### **Installation et Démarrage**

#### **Option 1 : Avec Docker (Recommandé)**
```bash
# Depuis la racine du projet
docker-compose up -d postgres redis
docker-compose up backend
```

#### **Option 2 : Développement Local**
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
.\venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application
python -m app.main
```

## 📁 **Structure du Projet**

```
backend/
├── app/
│   ├── api/           # Routes API
│   ├── core/          # Configuration et base de données
│   ├── models/        # Modèles SQLAlchemy
│   ├── schemas/       # Schémas Pydantic
│   ├── services/      # Logique métier
│   └── main.py        # Point d'entrée
├── requirements.txt    # Dépendances Python
├── Dockerfile         # Configuration Docker
└── README.md          # Ce fichier
```

## 🔧 **Configuration**

### **Variables d'Environnement**
Créez un fichier `.env` à la racine du projet :

```env
# Base de données
DATABASE_URL=postgresql://millesime_user:millesime_password@localhost:5432/millesime_db

# Sécurité
SECRET_KEY=votre-cle-secrete-tres-longue-et-complexe

# Mode développement
DEBUG=true
```

### **Base de Données**
- **PostgreSQL** : Port 5432
- **Redis** : Port 6379
- **Backend API** : Port 8000

## 🌐 **Endpoints API**

### **Documentation Interactive**
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### **Endpoints Principaux**
- `GET /` : Page d'accueil de l'API
- `GET /health` : Vérification de l'état
- `GET /v1/barrels` : Liste des fûts
- `POST /v1/auth/register` : Inscription utilisateur
- `POST /v1/auth/login` : Connexion utilisateur

## 🗄️ **Modèles de Base de Données**

### **Users**
- Gestion des comptes (B2C, B2B, Admin)
- Authentification JWT
- Profils utilisateurs

### **Barrels**
- Catalogue des fûts
- Gestion des stocks
- Images et descriptions

### **Orders**
- Commandes des clients
- Gestion des statuts
- Historique des achats

### **Addresses**
- Adresses de livraison
- Adresses de facturation
- Gestion des pays

## 🧪 **Tests**

```bash
# Exécuter tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_models.py
```

## 📊 **Monitoring et Logs**

### **Logs Structurés**
- Format JSON pour faciliter l'analyse
- Niveaux : DEBUG, INFO, WARNING, ERROR, CRITICAL

### **Métriques**
- Endpoint `/health` pour la surveillance
- Logs de performance des requêtes

## 🔒 **Sécurité**

- **Authentification JWT** pour les utilisateurs connectés
- **Validation des données** avec Pydantic
- **CORS configuré** pour le frontend
- **Hachage des mots de passe** avec bcrypt

## 🚀 **Déploiement**

### **Production**
```bash
# Build de l'image Docker
docker build -t millesime-backend .

# Démarrage des services
docker-compose -f docker-compose.prod.yml up -d
```

### **Variables de Production**
- `DEBUG=false`
- `SECRET_KEY` sécurisée
- Base de données PostgreSQL externe
- Redis externe

## 🐛 **Dépannage**

### **Problèmes Courants**

#### **Erreur de connexion à la base de données**
```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps postgres

# Vérifier les logs
docker-compose logs postgres
```

#### **Port déjà utilisé**
```bash
# Changer le port dans docker-compose.yml
ports:
  - "8001:8000"  # Au lieu de "8000:8000"
```

#### **Dépendances manquantes**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

## 📚 **Documentation Technique**

- **Architecture** : FastAPI + SQLAlchemy + PostgreSQL
- **Authentification** : JWT avec python-jose
- **Validation** : Pydantic pour les schémas
- **Base de données** : PostgreSQL avec migrations Alembic
- **Cache** : Redis pour les sessions et données temporaires

## 🤝 **Contribution**

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 **Support**

Pour toute question ou problème :
- Vérifier la documentation API : http://localhost:8000/docs
- Consulter les logs de l'application
- Ouvrir une issue sur le repository

---

*Dernière mise à jour : 27/08/2025*
