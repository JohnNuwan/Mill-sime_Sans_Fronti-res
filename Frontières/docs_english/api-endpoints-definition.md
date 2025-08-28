### **API Endpoint Definitions - Millésime Sans Frontières Backend**

**Version:** 1.0
**Date:** 08/27/2025

**1. Purpose**

This document details the RESTful API endpoints exposed by the Millésime Sans Frontières backend. It specifies the HTTP methods, paths, query parameters, request bodies, and response structures for each feature.

**2. General Principles**

*   **API Versioning:** All endpoints will be prefixed with `/v1/` (e.g., `/v1/barrels`).
*   **Authentication:** Endpoints requiring authentication need a valid JWT in the `Authorization: Bearer <token>` header.
*   **Error Handling:** Errors will be returned with an appropriate HTTP status code and a standardized JSON response body, generally in the format `{"detail": "Error message"}`.
*   **Data Validation:** All incoming data will be validated by Pydantic. Validation errors will return a `422 Unprocessable Entity` status.

**3. Endpoints by Resource**

---

#### **Resource: Authentication and Users (`/v1/auth`, `/v1/users`)**

##### **Endpoint: Register a new user**

*   **Method:** `POST`
*   **Path:** `/v1/auth/register`
*   **Description:** Creates a new user account (B2C or B2B).
*   **Authentication Required:** No
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "StrongPassword123",
      "first_name": "John",
      "last_name": "Doe",
      "role": "b2c" // or "b2b"
    }
    ```
*   **Response (Success - 201 Created):**
    ```json
    {
      "id": "user-uuid",
      "email": "user@example.com",
      "role": "b2c"
    }
    ```
*   **Response (Error - 400 Bad Request, 422 Unprocessable Entity):**
    ```json
    {"detail": "Email already registered"}
    ```

##### **Endpoint: User login**

*   **Method:** `POST`
*   **Path:** `/v1/auth/login`
*   **Description:** Authenticates the user and returns a JWT.
*   **Authentication Required:** No
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "StrongPassword123"
    }
    ```
*   **Response (Success - 200 OK):**
    ```json
    {
      "access_token": "your_jwt_token",
      "token_type": "bearer"
    }
    ```
*   **Response (Error - 401 Unauthorized):**
    ```json
    {"detail": "Invalid credentials"}
    ```

##### **Endpoint: Get the connected user's profile**

*   **Method:** `GET`
*   **Path:** `/v1/users/me`
*   **Description:** Returns the profile information of the authenticated user.
*   **Authentication Required:** Yes (Any role)
*   **Response (Success - 200 OK):**
    ```json
    {
      "id": "user-uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "b2c",
      "company_name": null
    }
    ```

---

#### **Resource: Barrels (`/v1/barrels`)**

##### **Endpoint: List all barrels**

*   **Method:** `GET`
*   **Path:** `/v1/barrels`
*   **Description:** Returns a paginated and filterable list of all available barrels.
*   **Authentication Required:** No
*   **Query Parameters (Query Params):**
    *   `skip`: `integer` (Optional, number of items to skip, default 0)
    *   `limit`: `integer` (Optional, max number of items to return, default 100)
    *   `origin_country`: `string` (Optional, filter by country of origin)
    *   `previous_content`: `string` (Optional, filter by previous content)
    *   `min_volume`: `numeric` (Optional, minimum volume)
    *   `max_volume`: `numeric` (Optional, maximum volume)
*   **Response (Success - 200 OK):**
    ```json
    [
      {
        "id": "barrel-uuid-1",
        "name": "French Oak Barrel Ex-Red Wine",
        "origin_country": "France",
        "volume_liters": 225,
        "price": 350.00,
        "stock_quantity": 5
      },
      // ... other barrels
    ]
    ```

##### **Endpoint: Get a barrel by ID**

*   **Method:** `GET`
*   **Path:** `/v1/barrels/{barrel_id}`
*   **Description:** Returns the details of a specific barrel.
*   **Authentication Required:** No
*   **Response (Success - 200 OK):**
    ```json
    {
      "id": "barrel-uuid-1",
      "name": "French Oak Barrel Ex-Red Wine",
      "origin_country": "France",
      "previous_content": "Red Wine",
      "volume_liters": 225,
      "wood_type": "French Oak",
      "condition": "Used",
      "price": 350.00,
      "stock_quantity": 5,
      "description": "225L barrel having contained red wine from Bordeaux...",
      "image_urls": ["image_url_1", "image_url_2"]
    }
    ```
*   **Response (Error - 404 Not Found):**
    ```json
    {"detail": "Barrel not found"}
    ```

##### **Endpoint: Create a new barrel (Admin)**

*   **Method:** `POST`
*   **Path:** `/v1/barrels`
*   **Description:** Adds a new barrel to the catalog.
*   **Authentication Required:** Yes (Role: `admin`)
*   **Request Body:** (similar to the GET response, without the ID and dates)
*   **Response (Success - 201 Created):** (similar to the GET response)

##### **Endpoint: Update an existing barrel (Admin)**

*   **Method:** `PUT`
*   **Path:** `/v1/barrels/{barrel_id}`
*   **Description:** Updates the information of a specific barrel.
*   **Authentication Required:** Yes (Role: `admin`)
*   **Request Body:** (similar to the GET response, with the fields to be modified)
*   **Response (Success - 200 OK):** (similar to the GET response)

##### **Endpoint: Delete a barrel (Admin)**

*   **Method:** `DELETE`
*   **Path:** `/v1/barrels/{barrel_id}`
*   **Description:** Deletes a barrel from the catalog.
*   **Authentication Required:** Yes (Role: `admin`)
*   **Response (Success - 204 No Content):** (No response body)

---

#### **Resource: Orders (`/v1/orders`)**

##### **Endpoint: Create a new order**

*   **Method:** `POST`
*   **Path:** `/v1/orders`
*   **Description:** Creates a new order for the authenticated user.
*   **Authentication Required:** Yes (Any role)
*   **Request Body:**
    ```json
    {
      "shipping_address_id": "shipping-address-uuid",
      "billing_address_id": "billing-address-uuid", // Optional
      "items": [
        {"barrel_id": "barrel-uuid-1", "quantity": 1},
        {"barrel_id": "barrel-uuid-2", "quantity": 2}
      ]
    }
    ```
*   **Response (Success - 201 Created):**
    ```json
    {
      "id": "order-uuid",
      "user_id": "user-uuid",
      "total_amount": 1050.00,
      "status": "pending",
      "order_date": "2025-08-27T10:00:00Z"
    }
    ```

##### **Endpoint: List user's orders**

*   **Method:** `GET`
*   **Path:** `/v1/orders`
*   **Description:** Returns the list of orders for the authenticated user.
*   **Authentication Required:** Yes (Any role)
*   **Response (Success - 200 OK):** (List of order objects)

##### **Endpoint: Get an order by ID**

*   **Method:** `GET`
*   **Path:** `/v1/orders/{order_id}`
*   **Description:** Returns the details of a specific order for the authenticated user.
*   **Authentication Required:** Yes (Any role)
*   **Response (Success - 200 OK):** (Order details with `OrderItems`)

---

#### **Resource: Quotes (`/v1/quotes`)**

##### **Endpoint: Request a quote**

*   **Method:** `POST`
*   **Path:** `/v1/quotes`
*   **Description:** Submits a quote request for barrels.
*   **Authentication Required:** Yes (Role: `b2b`)
*   **Request Body:**
    ```json
    {
      "requested_items": [
        {"barrel_id": "barrel-uuid-3", "quantity": 10},
        {"barrel_id": "barrel-uuid-4", "quantity": 5}
      ],
      "notes": "Needed for a new distillery project."
    }
    ```
*   **Response (Success - 201 Created):**
    ```json
    {
      "id": "quote-uuid",
      "user_id": "b2b-user-uuid",
      "status": "pending",
      "request_date": "2025-08-27T10:30:00Z"
    }
    ```

##### **Endpoint: List user's quotes**

*   **Method:** `GET`
*   **Path:** `/v1/quotes`
*   **Description:** Returns the list of quotes for the authenticated user.
*   **Authentication Required:** Yes (Role: `b2b`)
*   **Response (Success - 200 OK):** (List of quote objects)

##### **Endpoint: Get a quote by ID**

*   **Method:** `GET`
*   **Path:** `/v1/quotes/{quote_id}`
*   **Description:** Returns the details of a specific quote for the authenticated user.
*   **Authentication Required:** Yes (Role: `b2b`)
*   **Response (Success - 200 OK):** (Quote details)

---

**4. Next Steps**

*   Definition of administration endpoints (user management, order management, quote management).
*   Detail of Pydantic schemas for each request and response body.