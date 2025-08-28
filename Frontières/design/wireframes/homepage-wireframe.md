# Wireframe - Page d'Accueil (Homepage)

## Structure Générale

```
┌─────────────────────────────────────────────────────────────────┐
│                        HEADER                                   │
├─────────────────────────────────────────────────────────────────┤
│ Logo | Navigation: Home | Our Barrels | About | B2B | Contact  │
│                    | Search Bar | Cart | Login/Register        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    HERO SECTION                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  [Image: Chai avec fûts]                               │   │
│  │                                                         │   │
│  │  "Quality Wine Barrels from Around the World"          │   │
│  │  (H1 - Playfair Display, 48px)                         │   │
│  │                                                         │   │
│  │  "Discover our exclusive collection of premium barrels │   │
│  │   for wine aging, decoration, and professional use"    │   │
│  │  (Body Large - Inter, 18px)                            │   │
│  │                                                         │   │
│  │  [Primary Button] "Explore Our Barrels"                │   │
│  │  [Secondary Button] "Professional Inquiries"           │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    FEATURED SECTIONS                           │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │             │  │             │  │             │           │
│  │  [Image]    │  │  [Image]    │  │  [Image]    │           │
│  │             │  │             │  │             │           │
│  │  Nouveautés │  │  Origine    │  │  Ex-Bourbon │           │
│  │  (H3)       │  │  France     │  │  Casks      │           │
│  │             │  │  (H3)       │  │  (H3)       │           │
│  │  Découvrez  │  │  Tradition  │  │  Caractère  │           │
│  │  nos derniers│  │  française  │  │  unique     │           │
│  │  arrivages  │  │  garantie   │  │  américain  │           │
│  │             │  │             │  │             │           │
│  │  [Button]   │  │  [Button]   │  │  [Button]   │           │
│  │  Voir plus  │  │  Explorer   │  │  Découvrir  │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    STATISTICS SECTION                          │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │             │  │             │  │             │           │
│  │    500+     │  │    25+      │  │    50+      │           │
│  │  Fûts       │  │  Pays       │  │  Clients    │           │
│  │  Disponibles│  │  d'Origine  │  │  Satisfaits │           │
│  │             │  │             │  │             │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    TESTIMONIALS SECTION                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  "Excellent quality barrels, perfect for our           │   │
│  │   winery. Fast international shipping!"                │   │
│  │                                                         │   │
│  │  - Jean Dupont, Château de Bordeaux                    │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    CTA SECTION                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  "Ready to Start Your Barrel Collection?"              │   │
│  │  (H2 - Playfair Display, 36px)                         │   │
│  │                                                         │   │
│  │  [Primary Button] "Browse Catalog"                     │   │
│  │  [Secondary Button] "Contact Sales Team"               │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                        FOOTER                                   │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │             │  │             │  │             │           │
│  │  Company    │  │  Products   │  │  Support    │           │
│  │  About Us   │  │  Barrels    │  │  Contact    │           │
│  │  Our Story  │  │  Categories │  │  FAQ        │           │
│  │  Team       │  │  New        │  │  Shipping   │           │
│  │             │  │  Arrivals   │  │  Returns    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  Newsletter: [Email Input] [Subscribe Button]          │   │
│  │                                                         │   │
│  │  Social Media: [Facebook] [Instagram] [LinkedIn]       │   │
│  │                                                         │   │
│  │  © 2025 Millésime Sans Frontières. All rights reserved.│   │
│  │  Terms & Conditions | Privacy Policy                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Composants Clés

### **Header**
- Logo à gauche
- Navigation principale centrée
- Barre de recherche, panier et connexion à droite
- Design sticky pour rester visible

### **Hero Section**
- Image de fond impactante (chai avec fûts)
- Titre principal accrocheur
- Sous-titre explicatif
- Deux boutons d'action (CTA principal et secondaire)

### **Featured Sections**
- Trois cartes en grille
- Images représentatives
- Titres courts et descriptifs
- Boutons d'action pour chaque section

### **Statistics Section**
- Trois statistiques clés
- Chiffres mis en avant
- Descriptions courtes
- Design épuré et impactant

### **Testimonials**
- Témoignage client mis en avant
- Citation inspirante
- Nom et entreprise du client
- Design élégant avec guillemets

### **CTA Final**
- Appel à l'action final
- Deux options d'action
- Design centré et impactant

### **Footer**
- Liens organisés par catégories
- Newsletter signup
- Réseaux sociaux
- Informations légales

## Responsive Design

### **Mobile (< 768px)**
- Navigation en hamburger menu
- Grille des sections en colonne unique
- Boutons empilés verticalement
- Espacement réduit

### **Tablet (768px - 1024px)**
- Navigation adaptée
- Grille des sections en 2 colonnes
- Espacement intermédiaire

### **Desktop (> 1024px)**
- Navigation complète visible
- Grille des sections en 3 colonnes
- Espacement généreux

## Notes de Design

- Utilisation de la palette de couleurs définie
- Typographie hiérarchique claire
- Espacement cohérent (8px grid system)
- Focus sur l'expérience utilisateur
- Design moderne et professionnel
- Optimisation pour la conversion

---

*Dernière mise à jour : 27/08/2025*
