# Frontend - Millésime Sans Frontières

Frontend Nuxt.js moderne pour la plateforme e-commerce de fûts de vin "Millésime Sans Frontières".

## 🚀 Technologies

- **Framework :** Nuxt.js 3.8+
- **Langage :** TypeScript
- **Styling :** Tailwind CSS + CSS personnalisé
- **État :** Pinia
- **Validation :** Vee-validate + Yup
- **Icônes :** Heroicons
- **UI Components :** Headless UI
- **Notifications :** Vue3 Toastify

## 📋 Prérequis

- Node.js 18.0.0+
- npm 9.0.0+
- Docker (optionnel, pour le déploiement)

## 🛠️ Installation

### Développement local

1. **Cloner le projet**
   ```bash
   cd Frontières/frontend
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Configurer l'environnement**
   ```bash
   cp env.example .env
   # Éditer .env avec vos valeurs
   ```

4. **Lancer en mode développement**
   ```bash
   npm run dev
   ```

   L'application sera accessible sur `http://localhost:3000`

### Avec Docker

1. **Construire l'image**
   ```bash
   docker build -t millesime-frontend .
   ```

2. **Lancer le conteneur**
   ```bash
   docker run -p 3000:3000 millesime-frontend
   ```

## 🏗️ Structure du Projet

```
frontend/
├── assets/                 # Ressources statiques
│   ├── css/               # Styles CSS
│   │   ├── main.css      # Styles principaux
│   │   └── tailwind.css  # Configuration Tailwind
├── components/            # Composants Vue.js réutilisables
├── composables/           # Composables Nuxt.js
│   ├── useAuth.ts        # Gestion de l'authentification
│   └── useCart.ts        # Gestion du panier
├── layouts/               # Layouts de l'application
│   └── default.vue       # Layout principal
├── pages/                 # Pages de l'application
│   └── index.vue         # Page d'accueil
├── public/                # Fichiers publics
├── stores/                # Stores Pinia
├── types/                 # Types TypeScript
├── utils/                 # Utilitaires
├── nuxt.config.ts         # Configuration Nuxt.js
├── tailwind.config.ts     # Configuration Tailwind CSS
├── package.json           # Dépendances
└── Dockerfile             # Configuration Docker
```

## 🎨 Design System

### Couleurs

- **Rouge Vin :** `#8B2635` (couleur principale)
- **Brun Chêne :** `#8B7355` (couleur secondaire)
- **Doré Whisky :** `#D4AF37` (couleur d'accent)
- **Palette neutre :** Blancs cassés et gris sophistiqués

### Typographie

- **Titres :** Playfair Display (élégant, sophistiqué)
- **Corps :** Inter (moderne, lisible)
- **Prix/Données :** JetBrains Mono (monospace)

### Composants

- **Boutons :** Primary, Secondary, Accent
- **Cartes :** Produits, Sections, Informations
- **Formulaires :** Inputs, Labels, Validation
- **Navigation :** Header, Footer, Mobile

## 🔧 Scripts Disponibles

```bash
# Développement
npm run dev          # Lancer en mode développement
npm run build        # Construire pour la production
npm run start        # Démarrer en mode production
npm run preview      # Prévisualiser la build

# Qualité du code
npm run lint         # Vérifier le code avec ESLint
npm run lint:fix     # Corriger automatiquement les erreurs
npm run type-check   # Vérifier les types TypeScript

# Installation
npm run postinstall  # Préparer l'environnement Nuxt.js
```

## 🌐 Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|---------|
| `API_BASE_URL` | URL de l'API backend | `http://localhost:8000` |
| `APP_NAME` | Nom de l'application | `Millésime Sans Frontières` |
| `APP_VERSION` | Version de l'application | `1.0.0` |
| `NODE_ENV` | Environnement d'exécution | `development` |

## 📱 Fonctionnalités

### ✅ Implémentées

- [x] Layout principal avec header/footer
- [x] Page d'accueil responsive
- [x] Système d'authentification
- [x] Gestion du panier
- [x] Design system complet
- [x] Configuration Tailwind CSS
- [x] Composables réutilisables
- [x] Support TypeScript
- [x] Configuration Docker

### 🚧 En Cours

- [ ] Page catalogue des fûts
- [ ] Page détail produit
- [ ] Processus de commande
- [ ] Espace utilisateur
- [ ] Espace B2B

### 📋 À Faire

- [ ] Système de recherche avancée
- [ ] Filtres et tri
- [ ] Système de devis
- [ ] Intégration paiement
- [ ] Gestion des commandes
- [ ] Notifications push
- [ ] Mode hors ligne (PWA)

## 🔐 Authentification

Le système d'authentification utilise JWT et gère :

- Connexion/Inscription
- Gestion des profils
- Rôles utilisateur (B2B/B2C/Admin)
- Persistance des sessions
- Validation des tokens

## 🛒 Panier

Le système de panier inclut :

- Ajout/Suppression d'articles
- Gestion des quantités
- Calcul automatique des totaux
- Frais de livraison
- Codes promo
- Export CSV/PDF
- Sauvegarde locale

## 📱 Responsive Design

- **Mobile First** approach
- **Breakpoints :** 320px, 768px, 1024px+
- **Grille flexible** avec CSS Grid
- **Navigation mobile** avec menu hamburger
- **Optimisations** pour tous les écrans

## ♿ Accessibilité

- **Contraste** minimum 4.5:1
- **Navigation clavier** complète
- **Screen readers** support
- **Focus visible** sur tous les éléments
- **Alt text** pour toutes les images
- **ARIA labels** appropriés

## 🧪 Tests

```bash
# Tests unitaires
npm run test:unit

# Tests d'intégration
npm run test:integration

# Tests E2E
npm run test:e2e

# Couverture de code
npm run test:coverage
```

## 🚀 Déploiement

### Production

```bash
# Construire l'application
npm run build

# Démarrer en production
npm run start
```

### Docker

```bash
# Construire l'image
docker build -t millesime-frontend .

# Lancer le conteneur
docker run -d -p 3000:3000 --name frontend millesime-frontend
```

### Docker Compose

```bash
# Lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f frontend
```

## 🔧 Configuration Avancée

### Tailwind CSS

Le fichier `tailwind.config.ts` contient :
- Couleurs personnalisées
- Typographie personnalisée
- Espacement personnalisé
- Composants personnalisés
- Breakpoints personnalisés

### Nuxt.js

Le fichier `nuxt.config.ts` configure :
- Modules et plugins
- Variables d'environnement
- Alias de chemins
- Configuration TypeScript
- Optimisations de build

## 📊 Performance

- **Lazy loading** des composants
- **Code splitting** automatique
- **Optimisation des images**
- **Cache des composants**
- **Bundle analyzer** intégré

## 🐛 Débogage

### Outils de développement

- **Nuxt DevTools** intégrés
- **Vue DevTools** support
- **Console de débogage**
- **Network monitoring**

### Logs

```bash
# Logs de développement
npm run dev

# Logs de production
npm run start

# Logs Docker
docker logs frontend
```

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature
3. **Commiter** vos changements
4. **Pousser** vers la branche
5. **Créer** une Pull Request

### Standards de code

- **ESLint** pour la qualité
- **Prettier** pour le formatage
- **TypeScript** strict mode
- **Conventions** Vue.js/Nuxt.js

## 📄 Licence

Ce projet est sous licence propriétaire. Tous droits réservés.

## 📞 Support

Pour toute question ou problème :

- **Issues GitHub** : [Créer une issue](https://github.com/...)
- **Email** : support@millesime-sans-frontieres.com
- **Documentation** : [Lien vers la doc](https://...)

---

**Dernière mise à jour :** 27/08/2025  
**Version :** 1.0.0  
**Auteur :** Équipe Millésime Sans Frontières
