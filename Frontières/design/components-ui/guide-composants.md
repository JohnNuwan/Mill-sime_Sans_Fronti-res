# Guide des Composants UI - Millésime Sans Frontières

## Système de Design

### **Grid System**
- **Base :** 8px
- **Breakpoints :** Mobile (320px), Tablet (768px), Desktop (1024px+)
- **Containers :** Max-width 1200px, padding 16px/24px/32px

### **Espacement**
- **XS :** 4px
- **S :** 8px
- **M :** 16px
- **L :** 24px
- **XL :** 32px
- **XXL :** 48px
- **XXXL :** 64px

## Composants de Base

### **1. Boutons (Buttons)**

#### **Bouton Principal**
```css
.btn-primary {
  background-color: var(--color-wine-red);
  color: var(--color-white);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--color-wine-red-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 38, 53, 0.3);
}
```

#### **Bouton Secondaire**
```css
.btn-secondary {
  background-color: transparent;
  color: var(--color-wine-red);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  border: 2px solid var(--color-wine-red);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: var(--color-wine-red);
  color: var(--color-white);
}
```

#### **Bouton d'Accent**
```css
.btn-accent {
  background-color: var(--color-whisky-gold);
  color: var(--color-very-dark-gray);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-accent:hover {
  background-color: var(--color-whisky-gold-dark);
  transform: translateY(-1px);
}
```

### **2. Cartes (Cards)**

#### **Carte Produit**
```css
.product-card {
  background-color: var(--color-white);
  border-radius: 12px;
  padding: var(--spacing-l);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid var(--color-very-light-gray);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.product-card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: var(--spacing-m);
}

.product-card__title {
  font-family: var(--font-headings);
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-very-dark-gray);
  margin-bottom: var(--spacing-s);
}

.product-card__price {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-wine-red);
  margin-bottom: var(--spacing-m);
}
```

#### **Carte de Section**
```css
.section-card {
  background-color: var(--color-off-white);
  border-radius: 16px;
  padding: var(--spacing-xl);
  text-align: center;
  border: 1px solid var(--color-light-gray);
  transition: all 0.3s ease;
}

.section-card:hover {
  background-color: var(--color-white);
  box-shadow: 0 8px 32px rgba(139, 115, 85, 0.1);
}
```

### **3. Formulaires (Forms)**

#### **Input de Base**
```css
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--color-light-gray);
  border-radius: 8px;
  font-family: var(--font-primary);
  font-size: var(--text-base);
  color: var(--color-very-dark-gray);
  background-color: var(--color-white);
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-wine-red);
  box-shadow: 0 0 0 3px rgba(139, 38, 53, 0.1);
}

.form-input::placeholder {
  color: var(--color-medium-gray);
}
```

#### **Label de Formulaire**
```css
.form-label {
  display: block;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-dark-gray);
  margin-bottom: var(--spacing-s);
}
```

#### **Groupe de Formulaire**
```css
.form-group {
  margin-bottom: var(--spacing-l);
}

.form-group--error .form-input {
  border-color: var(--color-error);
}

.form-group--error .form-error {
  color: var(--color-error);
  font-size: var(--text-sm);
  margin-top: var(--spacing-s);
}
```

### **4. Navigation (Navigation)**

#### **Header Principal**
```css
.main-header {
  background-color: var(--color-white);
  border-bottom: 1px solid var(--color-very-light-gray);
  padding: var(--spacing-m) 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
}

.nav-link {
  font-family: var(--font-primary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--color-dark-gray);
  text-decoration: none;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: var(--color-wine-red);
}

.nav-link--active {
  color: var(--color-wine-red);
  font-weight: var(--font-semibold);
}
```

#### **Menu Mobile (Hamburger)**
```css
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
  padding: var(--spacing-s);
}

.mobile-menu-toggle__line {
  width: 24px;
  height: 2px;
  background-color: var(--color-dark-gray);
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }
  
  .nav-menu {
    display: none;
  }
}
```

### **5. Modales et Overlays**

#### **Modal de Base**
```css
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(44, 42, 38, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.modal--active {
  opacity: 1;
  visibility: visible;
}

.modal__content {
  background-color: var(--color-white);
  border-radius: 16px;
  padding: var(--spacing-xl);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  transform: scale(0.9);
  transition: transform 0.3s ease;
}

.modal--active .modal__content {
  transform: scale(1);
}
```

### **6. Composants de Filtrage**

#### **Filtre de Recherche**
```css
.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-s);
  margin-bottom: var(--spacing-l);
}

.filter-label {
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-dark-gray);
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--color-light-gray);
  border-radius: 6px;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  background-color: var(--color-white);
  cursor: pointer;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: var(--spacing-s);
  cursor: pointer;
}

.filter-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--color-wine-red);
}
```

### **7. Composants de Feedback**

#### **Message de Succès**
```css
.message {
  padding: var(--spacing-m);
  border-radius: 8px;
  margin-bottom: var(--spacing-l);
  font-family: var(--font-primary);
  font-size: var(--text-base);
}

.message--success {
  background-color: rgba(40, 167, 69, 0.1);
  border: 1px solid var(--color-success);
  color: var(--color-success);
}

.message--error {
  background-color: rgba(220, 53, 69, 0.1);
  border: 1px solid var(--color-error);
  color: var(--color-error);
}

.message--warning {
  background-color: rgba(255, 140, 0, 0.1);
  border: 1px solid var(--color-warning);
  color: var(--color-warning);
}
```

#### **Loader/Spinner**
```css
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-light-gray);
  border-top: 2px solid var(--color-wine-red);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## Responsive Design

### **Breakpoints CSS**
```css
/* Mobile First */
.container {
  padding: var(--spacing-m);
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: var(--spacing-l);
    max-width: 720px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: var(--spacing-xl);
    max-width: 1200px;
  }
}
```

### **Grille Responsive**
```css
.grid {
  display: grid;
  gap: var(--spacing-l);
}

.grid--2-cols {
  grid-template-columns: 1fr;
}

.grid--3-cols {
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid--2-cols {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid--3-cols {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Accessibilité

### **Focus States**
```css
.btn:focus,
.form-input:focus,
.nav-link:focus {
  outline: 2px solid var(--color-wine-red);
  outline-offset: 2px;
}
```

### **Screen Reader Only**
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

*Dernière mise à jour : 27/08/2025*
