# Plan de Création des Maquettes - Millésime Sans Frontières

## Vue d'ensemble

Ce document détaille le plan de travail pour créer toutes les maquettes visuelles nécessaires au projet. Les maquettes seront créées en utilisant Figma (recommandé) ou un outil similaire.

## Phase 1 : Maquettes de Base (Semaine 1-2)

### **1.1 Page d'Accueil (Homepage)**
- **Priorité :** Élevée
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Header avec navigation
  - Hero section avec image de fond
  - Sections mises en avant (3 cartes)
  - Section statistiques
  - Témoignages clients
  - CTA final
  - Footer complet

**Éléments visuels à créer :**
- [ ] Mockup d'image hero (chai avec fûts)
- [ ] Icônes pour les statistiques
- [ ] Images des sections mises en avant
- [ ] Logo de l'entreprise

### **1.2 Page Catalogue**
- **Priorité :** Élevée
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Filtres de recherche (pays, contenu, volume, bois, état)
  - Grille de produits
  - Pagination
  - Tri des résultats
  - Breadcrumbs

**Éléments visuels à créer :**
- [ ] Mockups de fûts pour les cartes produits
- [ ] Icônes pour les filtres
- [ ] État des filtres actifs/inactifs

### **1.3 Page Produit**
- **Priorité :** Élevée
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Galerie d'images du fût
  - Informations détaillées
  - Prix et stock
  - Boutons d'action
  - Description technique
  - Fûts similaires

**Éléments visuels à créer :**
- [ ] Mockups de fûts sous différents angles
- [ ] Icônes pour les caractéristiques techniques
- [ ] État du stock (disponible, épuisé, etc.)

## Phase 2 : Maquettes Fonctionnelles (Semaine 3-4)

### **2.1 Panier d'Achat**
- **Priorité :** Moyenne
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Liste des articles
  - Quantités et prix
  - Sous-total et total
  - Boutons de modification
  - CTA vers checkout

### **2.2 Processus de Commande (Checkout)**
- **Priorité :** Moyenne
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Étapes du processus (3-4 étapes)
  - Formulaires de livraison et facturation
  - Sélection du mode de paiement
  - Récapitulatif de la commande
  - Confirmation

### **2.3 Espace Client**
- **Priorité :** Moyenne
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Tableau de bord
  - Historique des commandes
  - Profil utilisateur
  - Adresses sauvegardées
  - Suivi des commandes

## Phase 3 : Maquettes Spécialisées (Semaine 5-6)

### **3.1 Espace B2B**
- **Priorité :** Moyenne
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - Formulaire de demande de devis
  - Catalogue B2B avec prix spéciaux
  - Gestion des commandes en gros
  - Documents et factures
  - Support dédié

### **3.2 Pages Informatives**
- **Priorité :** Faible
- **Responsive :** Desktop, Tablet, Mobile
- **Composants :**
  - À propos de nous
  - Contact et support
  - FAQ
  - Pages légales (CGV, etc.)

## Phase 4 : Composants et États (Semaine 7-8)

### **4.1 Bibliothèque de Composants**
- **Priorité :** Moyenne
- **Composants :**
  - Boutons (tous les états)
  - Formulaires (validation, erreurs)
  - Navigation (mobile, desktop)
  - Modales et overlays
  - Messages de feedback
  - Loaders et spinners

### **4.2 États des Composants**
- **Priorité :** Moyenne
- **États à couvrir :**
  - Normal, Hover, Focus, Active
  - Disabled, Loading, Error
  - Success, Warning, Info

## Outils et Ressources

### **Outil Principal : Figma**
- **Avantages :** Collaboration en temps réel, composants réutilisables, export facile
- **Fonctionnalités clés :** Auto-layout, Design tokens, Prototyping

### **Ressources Graphiques**
- **Images :** Unsplash, Pexels pour les mockups
- **Icônes :** Feather Icons, Heroicons, ou création personnalisée
- **Illustrations :** Undraw, ou création personnalisée

### **Organisation des Fichiers Figma**
```
📁 Millésime Sans Frontières
├── 🎨 Design System
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   └── Components
├── 📱 Pages
│   ├── Homepage
│   ├── Catalog
│   ├── Product
│   ├── Cart
│   ├── Checkout
│   └── Account
├── 🧩 Components
│   ├── Buttons
│   ├── Forms
│   ├── Cards
│   ├── Navigation
│   └── Feedback
└── 📱 Responsive
    ├── Desktop (1440px)
    ├── Tablet (768px)
    └── Mobile (375px)
```

## Standards de Qualité

### **Design**
- Respect strict de la charte graphique
- Cohérence visuelle entre toutes les pages
- Hiérarchie visuelle claire
- Accessibilité (contraste, tailles, etc.)

### **Responsive**
- Mobile-first approach
- Breakpoints cohérents
- Adaptation des composants
- Performance sur mobile

### **Accessibilité**
- Ratio de contraste minimum 4.5:1
- Tailles de police lisibles
- États de focus visibles
- Support des lecteurs d'écran

## Livrables

### **Fichiers Figma**
- [ ] Design System complet
- [ ] Maquettes de toutes les pages
- [ ] Composants réutilisables
- [ ] Prototypes interactifs

### **Exports**
- [ ] Images PNG/JPG des maquettes
- [ ] PDF des wireframes
- [ ] Spécifications CSS
- [ ] Guide d'implémentation

### **Documentation**
- [ ] Guide des composants
- [ ] Spécifications techniques
- [ ] Guide responsive
- [ ] Checklist d'accessibilité

## Planning Détaillé

| Semaine | Phase | Tâches | Livrables |
|---------|-------|---------|-----------|
| 1 | 1.1 | Homepage Desktop | Maquette Homepage Desktop |
| 1 | 1.1 | Homepage Tablet | Maquette Homepage Tablet |
| 2 | 1.1 | Homepage Mobile | Maquette Homepage Mobile |
| 2 | 1.2 | Catalogue Desktop | Maquette Catalogue Desktop |
| 3 | 1.2 | Catalogue Responsive | Maquettes Catalogue Tablet/Mobile |
| 3 | 1.3 | Page Produit | Maquettes Page Produit Responsive |
| 4 | 2.1-2.2 | Panier & Checkout | Maquettes Panier & Checkout |
| 5 | 2.3 | Espace Client | Maquettes Espace Client |
| 6 | 3.1 | Espace B2B | Maquettes Espace B2B |
| 7 | 4.1 | Composants | Bibliothèque de Composants |
| 8 | 4.2 | États & Finalisation | Maquettes Finales + Documentation |

## Prochaines Étapes

1. **Validation du plan** par l'équipe
2. **Création du Design System** dans Figma
3. **Début des maquettes** de la page d'accueil
4. **Révision et itération** continue
5. **Tests utilisateurs** sur les maquettes
6. **Finalisation** et livraison

---

*Dernière mise à jour : 27/08/2025*
