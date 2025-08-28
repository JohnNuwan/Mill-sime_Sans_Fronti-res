### **Définition des Endpoints API - Millésime Sans Frontières Backend**

**Version:** 1.0
**Date:** 27/08/2025

**1. Objectif**

Ce document détaille les endpoints de l'API RESTful exposés par le backend de Millésime Sans Frontières. Il spécifie les méthodes HTTP, les chemins d'accès, les paramètres de requête, les corps de requête et les structures de réponse pour chaque fonctionnalité.

**2. Principes Généraux**

*   **Versionning de l'API:** Tous les endpoints seront préfixés par `/v1/` (ex: `/v1/barrels`).
*   **Authentification:** Les endpoints nécessitant une authentification requièrent un JWT valide dans l'en-tête `Authorization: Bearer <token>`.
*   **Gestion des Erreurs:** Les erreurs seront retournées avec un code de statut HTTP approprié et un corps de réponse JSON standardisé, généralement sous la forme `{"detail": "Message d'erreur"}`.
*   **Validation des Données:** Toutes les données entrantes seront validées par Pydantic. Les erreurs de validation retourneront un statut `422 Unprocessable Entity`.

**3. Endpoints par Ressource**

---

#### **Ressource: Authentification et Utilisateurs (`/v1/auth`, `/v1/users`)**

##### **Endpoint: Enregistrement d'un nouvel utilisateur**

*   **Méthode:** `POST`
*   **Chemin:** `/v1/auth/register`
*   **Description:** Crée un nouveau compte utilisateur (B2C ou B2B).
*   **Authentification Requise:** Non
*   **Corps de Requête:**
    ```json
    {
      "email": "user@example.com",
      "password": "StrongPassword123",
      "first_name": "John",
      "last_name": "Doe",
      "role": "b2c" // ou "b2b"
    }
    ```
*   **Réponse (Succès - 201 Created):**
    ```json
    {
      "id": "uuid-utilisateur",
      "email": "user@example.com",
      "role": "b2c"
    }
    ```
*   **Réponse (Erreur - 400 Bad Request, 422 Unprocessable Entity):**
    ```json
    {"detail": "Email déjà enregistré"}
    ```

##### **Endpoint: Connexion de l'utilisateur**

*   **Méthode:** `POST`
*   **Chemin:** `/v1/auth/login`
*   **Description:** Authentifie l'utilisateur et retourne un JWT.
*   **Authentification Requise:** Non
*   **Corps de Requête:**
    ```json
    {
      "email": "user@example.com",
      "password": "StrongPassword123"
    }
    ```
*   **Réponse (Succès - 200 OK):**
    ```json
    {
      "access_token": "votre_jwt_token",
      "token_type": "bearer"
    }
    ```
*   **Réponse (Erreur - 401 Unauthorized):**
    ```json
    {"detail": "Identifiants invalides"}
    ```

##### **Endpoint: Obtenir le profil de l'utilisateur connecté**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/users/me`
*   **Description:** Retourne les informations du profil de l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Tout rôle)
*   **Réponse (Succès - 200 OK):**
    ```json
    {
      "id": "uuid-utilisateur",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "b2c",
      "company_name": null
    }
    ```

---

#### **Ressource: Fûts (`/v1/barrels`)**

##### **Endpoint: Lister tous les fûts**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/barrels`
*   **Description:** Retourne une liste paginée et filtrable de tous les fûts disponibles.
*   **Authentification Requise:** Non
*   **Paramètres de Requête (Query Params):**
    *   `skip`: `integer` (Optionnel, nombre d'éléments à ignorer, défaut 0)
    *   `limit`: `integer` (Optionnel, nombre max d'éléments à retourner, défaut 100)
    *   `origin_country`: `string` (Optionnel, filtre par pays d'origine)
    *   `previous_content`: `string` (Optionnel, filtre par contenu précédent)
    *   `min_volume`: `numeric` (Optionnel, volume minimum)
    *   `max_volume`: `numeric` (Optionnel, volume maximum)
*   **Réponse (Succès - 200 OK):**
    ```json
    [
      {
        "id": "uuid-fut-1",
        "name": "Fût Chêne Français Ex-Vin Rouge",
        "origin_country": "France",
        "volume_liters": 225,
        "price": 350.00,
        "stock_quantity": 5
      },
      // ... autres fûts
    ]
    ```

##### **Endpoint: Obtenir un fût par ID**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/barrels/{barrel_id}`
*   **Description:** Retourne les détails d'un fût spécifique.
*   **Authentification Requise:** Non
*   **Réponse (Succès - 200 OK):**
    ```json
    {
      "id": "uuid-fut-1",
      "name": "Fût Chêne Français Ex-Vin Rouge",
      "origin_country": "France",
      "previous_content": "Vin Rouge",
      "volume_liters": 225,
      "wood_type": "Chêne Français",
      "condition": "Usagé",
      "price": 350.00,
      "stock_quantity": 5,
      "description": "Fût de 225L ayant contenu du vin rouge de Bordeaux...",
      "image_urls": ["url_image_1", "url_image_2"]
    }
    ```
*   **Réponse (Erreur - 404 Not Found):**
    ```json
    {"detail": "Fût non trouvé"}
    ```

##### **Endpoint: Créer un nouveau fût (Admin)**

*   **Méthode:** `POST`
*   **Chemin:** `/v1/barrels`
*   **Description:** Ajoute un nouveau fût au catalogue.
*   **Authentification Requise:** Oui (Rôle: `admin`)
*   **Corps de Requête:** (similaire à la réponse GET, sans l'ID et les dates)
*   **Réponse (Succès - 201 Created):** (similaire à la réponse GET)

##### **Endpoint: Mettre à jour un fût existant (Admin)**

*   **Méthode:** `PUT`
*   **Chemin:** `/v1/barrels/{barrel_id}`
*   **Description:** Met à jour les informations d'un fût spécifique.
*   **Authentification Requise:** Oui (Rôle: `admin`)
*   **Corps de Requête:** (similaire à la réponse GET, avec les champs à modifier)
*   **Réponse (Succès - 200 OK):** (similaire à la réponse GET)

##### **Endpoint: Supprimer un fût (Admin)**

*   **Méthode:** `DELETE`
*   **Chemin:** `/v1/barrels/{barrel_id}`
*   **Description:** Supprime un fût du catalogue.
*   **Authentification Requise:** Oui (Rôle: `admin`)
*   **Réponse (Succès - 204 No Content):** (Aucun corps de réponse)

---

#### **Ressource: Commandes (`/v1/orders`)**

##### **Endpoint: Créer une nouvelle commande**

*   **Méthode:** `POST`
*   **Chemin:** `/v1/orders`
*   **Description:** Crée une nouvelle commande pour l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Tout rôle)
*   **Corps de Requête:**
    ```json
    {
      "shipping_address_id": "uuid-adresse-livraison",
      "billing_address_id": "uuid-adresse-facturation", // Optionnel
      "items": [
        {"barrel_id": "uuid-fut-1", "quantity": 1},
        {"barrel_id": "uuid-fut-2", "quantity": 2}
      ]
    }
    ```
*   **Réponse (Succès - 201 Created):**
    ```json
    {
      "id": "uuid-commande",
      "user_id": "uuid-utilisateur",
      "total_amount": 1050.00,
      "status": "pending",
      "order_date": "2025-08-27T10:00:00Z"
    }
    ```

##### **Endpoint: Lister les commandes de l'utilisateur**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/orders`
*   **Description:** Retourne la liste des commandes de l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Tout rôle)
*   **Réponse (Succès - 200 OK):** (Liste d'objets commande)

##### **Endpoint: Obtenir une commande par ID**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/orders/{order_id}`
*   **Description:** Retourne les détails d'une commande spécifique de l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Tout rôle)
*   **Réponse (Succès - 200 OK):** (Détails de la commande avec les `OrderItems`)

---

#### **Ressource: Devis (`/v1/quotes`)**

##### **Endpoint: Demander un devis**

*   **Méthode:** `POST`
*   **Chemin:** `/v1/quotes`
*   **Description:** Soumet une demande de devis pour des fûts.
*   **Authentification Requise:** Oui (Rôle: `b2b`)
*   **Corps de Requête:**
    ```json
    {
      "requested_items": [
        {"barrel_id": "uuid-fut-3", "quantity": 10},
        {"barrel_id": "uuid-fut-4", "quantity": 5}
      ],
      "notes": "Besoin pour un nouveau projet de distillerie."
    }
    ```
*   **Réponse (Succès - 201 Created):**
    ```json
    {
      "id": "uuid-devis",
      "user_id": "uuid-utilisateur-b2b",
      "status": "pending",
      "request_date": "2025-08-27T10:30:00Z"
    }
    ```

##### **Endpoint: Lister les devis de l'utilisateur**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/quotes`
*   **Description:** Retourne la liste des devis de l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Rôle: `b2b`)
*   **Réponse (Succès - 200 OK):** (Liste d'objets devis)

##### **Endpoint: Obtenir un devis par ID**

*   **Méthode:** `GET`
*   **Chemin:** `/v1/quotes/{quote_id}`
*   **Description:** Retourne les détails d'un devis spécifique de l'utilisateur authentifié.
*   **Authentification Requise:** Oui (Rôle: `b2b`)
*   **Réponse (Succès - 200 OK):** (Détails du devis)

---

**4. Prochaines Étapes**

*   Définition des endpoints d'administration (gestion des utilisateurs, gestion des commandes, gestion des devis).
*   Détail des schémas Pydantic pour chaque corps de requête et de réponse.
