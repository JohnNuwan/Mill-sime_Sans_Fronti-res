# Guide Typographique - Millésime Sans Frontières

## Familles de Polices

### **Police Principale : Inter**
- **Justification :** Moderne, lisible, excellente pour le web
- **Fallback :** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Usage :** Corps de texte, navigation, boutons

### **Police de Titres : Playfair Display**
- **Justification :** Élégante, sophistiquée, parfaite pour l'univers du vin
- **Fallback :** `Georgia, 'Times New Roman', serif`
- **Usage :** Titres principaux, accroches, éléments de marque

### **Police Monospace : JetBrains Mono**
- **Justification :** Excellente lisibilité pour le code et les données techniques
- **Fallback :** `'Courier New', Courier, monospace`
- **Usage :** Prix, dimensions, codes produits

## Hiérarchie Typographique

### **H1 - Titre Principal**
- **Police :** Playfair Display
- **Taille :** 48px (desktop) / 36px (tablet) / 28px (mobile)
- **Poids :** 700 (Bold)
- **Hauteur de ligne :** 1.2
- **Couleur :** `#2C2A26` (Gris Très Sombre)
- **Usage :** Titre de page, accroche principale

### **H2 - Titre de Section**
- **Police :** Playfair Display
- **Taille :** 36px (desktop) / 28px (tablet) / 24px (mobile)
- **Poids :** 600 (Semi-Bold)
- **Hauteur de ligne :** 1.3
- **Couleur :** `#2C2A26` (Gris Très Sombre)
- **Usage :** Sections principales, catégories

### **H3 - Titre de Sous-section**
- **Police :** Inter
- **Taille :** 24px (desktop) / 20px (tablet) / 18px (mobile)
- **Poids :** 600 (Semi-Bold)
- **Hauteur de ligne :** 1.4
- **Couleur :** `#2C2A26` (Gris Très Sombre)
- **Usage :** Sous-sections, cartes produits

### **H4 - Titre de Composant**
- **Police :** Inter
- **Taille :** 20px (desktop) / 18px (tablet) / 16px (mobile)
- **Poids :** 600 (Semi-Bold)
- **Hauteur de ligne :** 1.4
- **Couleur :** `#2C2A26` (Gris Très Sombre)
- **Usage :** Titres de cartes, labels de formulaires

### **Body Large - Texte Important**
- **Police :** Inter
- **Taille :** 18px (desktop) / 16px (tablet) / 16px (mobile)
- **Poids :** 400 (Regular)
- **Hauteur de ligne :** 1.6
- **Couleur :** `#6B655C` (Gris Sombre)
- **Usage :** Descriptions importantes, textes d'introduction

### **Body - Texte Principal**
- **Police :** Inter
- **Taille :** 16px (desktop) / 16px (tablet) / 14px (mobile)
- **Poids :** 400 (Regular)
- **Hauteur de ligne :** 1.6
- **Couleur :** `#6B655C` (Gris Sombre)
- **Usage :** Corps de texte principal, paragraphes

### **Body Small - Texte Secondaire**
- **Police :** Inter
- **Taille :** 14px (desktop) / 14px (tablet) / 12px (mobile)
- **Poids :** 400 (Regular)
- **Hauteur de ligne :** 1.5
- **Couleur :** `#B8B3A8` (Gris Moyen)
- **Usage :** Métadonnées, informations secondaires

### **Caption - Légendes**
- **Police :** Inter
- **Taille :** 12px (desktop) / 12px (tablet) / 11px (mobile)
- **Poids :** 400 (Regular)
- **Hauteur de ligne :** 1.4
- **Couleur :** `#B8B3A8` (Gris Moyen)
- **Usage :** Légendes d'images, notes de bas de page

## Styles Spéciaux

### **Prix**
- **Police :** JetBrains Mono
- **Taille :** 24px (desktop) / 20px (tablet) / 18px (mobile)
- **Poids :** 700 (Bold)
- **Couleur :** `#8B2635` (Rouge Vin)
- **Usage :** Affichage des prix des fûts

### **Labels de Filtres**
- **Police :** Inter
- **Taille :** 14px
- **Poids :** 500 (Medium)
- **Couleur :** `#6B655C` (Gris Sombre)
- **Usage :** Labels des filtres de recherche

### **Boutons**
- **Police :** Inter
- **Taille :** 16px
- **Poids :** 600 (Semi-Bold)
- **Couleur :** Selon le type de bouton
- **Usage :** Texte des boutons d'action

## Responsive Typography

### **Breakpoints**
- **Mobile :** < 768px
- **Tablet :** 768px - 1024px
- **Desktop :** > 1024px

### **Règles de Scaling**
- Les tailles de police s'adaptent proportionnellement
- Maintien des ratios de contraste sur tous les écrans
- Optimisation de la lisibilité sur mobile

## Accessibilité

### **Contraste**
- Tous les textes respectent un ratio de contraste minimum de 4.5:1
- Les textes de grande taille (18px+) peuvent utiliser un ratio de 3:1

### **Taille Minimale**
- Taille de police minimale : 12px
- Possibilité d'augmenter la taille via les paramètres du navigateur

### **Espacement**
- Espacement vertical suffisant entre les lignes (minimum 1.4)
- Espacement horizontal suffisant entre les lettres (minimum 0.12em)

## Codes CSS

```css
/* Import des polices */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

/* Variables CSS pour les polices */
:root {
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-headings: 'Playfair Display', Georgia, 'Times New Roman', serif;
  --font-mono: 'JetBrains Mono', 'Courier New', Courier, monospace;
  
  /* Tailles de police */
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 36px;
  --text-4xl: 48px;
  
  /* Poids de police */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

/* Classes utilitaires */
.text-h1 {
  font-family: var(--font-headings);
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: 1.2;
  color: var(--color-very-dark-gray);
}

.text-body {
  font-family: var(--font-primary);
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: 1.6;
  color: var(--color-dark-gray);
}

.text-price {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-wine-red);
}
```

---

*Dernière mise à jour : 27/08/2025*
