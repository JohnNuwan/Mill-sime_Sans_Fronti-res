### **Frontend Specifications - Millésime Sans Frontières**

**Version:** 1.0
**Date:** 08/27/2025

**1. Objective**

This document describes the technical and functional specifications for the frontend of the "Millésime Sans Frontières" wine barrel e-commerce site. The frontend will be the main user interface, allowing customers to browse the catalog, place orders, and interact with the company's services.

**2. Key Technologies**

*   **JavaScript Framework:** Nuxt.js (recommended)
    *   **Justification for choosing Nuxt.js over pure Vue.js:**
        *   **SSR (Server-Side Rendering) / Static Site Generation:** Essential for the SEO of an e-commerce site, allowing search engines to easily index content.
        *   **Automatic Routing:** Simplifies route management based on the file structure.
        *   **State Management (Vuex):** Facilitated integration for centralized data management.
        *   **Performance Optimizations:** Fast page loading and a better user experience.
        *   **Full-Stack Development:** Ability to add server-side features if necessary.
*   **Language:** JavaScript (with the possibility of TypeScript for better robustness if desired later).
*   **Package Manager:** npm or Yarn.
*   **Styling:** CSS (with a preprocessor like Sass/SCSS) or a CSS framework (e.g., Tailwind CSS, Bootstrap) for rapid development and responsive design.

**3. Design and UX (User Experience) Principles**

*   **Modern and Clean Design:** A visually appealing, intuitive, and easy-to-use interface.
*   **Fully Responsive (Mobile-First):** The site must adapt perfectly to all screen sizes (mobiles, tablets, desktops) with a "mobile-first" design approach.
*   **Intuitive Navigation:** Clear menus, logical navigation paths, effective search and filters.
*   **Performance:** Fast loading times, smooth animations.
*   **Accessibility:** Compliance with web accessibility standards (WCAG) to ensure use by everyone.
*   **Visual Consistency:** Consistent use of colors, typography, icons, and UI components throughout the entire site.

**4. Key Frontend Features**

*   **Static Pages:**
    *   Homepage: Presentation, featured products, calls to action.
    *   About Us: History, mission, team.
    *   Contact: Contact form, contact details.
    *   Legal Pages: Terms of Service, Privacy Policy, Shipping & Returns.
*   **Product Catalog (Barrels):**
    *   Display of barrels with images, names, prices.
    *   Advanced search and filtering features (by country of origin, previous content, volume, wood type, condition).
    *   Pagination and sorting of results.
*   **Product Detail Page:**
    *   Full display of barrel information (description, technical specifications, multiple images).
    *   "Add to Cart" or "Request a Quote" button.
*   **Shopping Cart:**
    *   Display of added items, quantities, prices.
    *   Ability to modify quantities or remove items.
    *   Subtotal calculation.
*   **Checkout Process:**
    *   Clear and secure multi-step process (shipping information, billing, payment).
    *   Real-time form validation.
    *   Integration with the backend's payment gateway.
*   **Authentication and User Profile:**
    *   Registration and login forms.
    *   User profile page: management of personal information, addresses.
    *   Order history with details.
    *   Order tracking.
*   **Professional Area (B2B):**
    *   Detailed quote request form.
    *   Tracking of submitted quotes.
    *   Access to specific information (B2B pricing, documents).

**5. Integration with the Backend (RESTful API)**

*   The frontend will communicate with the FastAPI backend via HTTP requests (GET, POST, PUT, DELETE).
*   Use of libraries like Axios or the native `fetch` API for requests.
*   Management of JWT tokens for request authentication.
*   API error handling and displaying relevant messages to the user.

**6. Deployment**

*   The frontend will be containerized with Docker for easy deployment via Docker Compose, alongside the backend and the database.

**7. Next Steps**

*   Creation of mockups and wireframes for key pages.
*   Definition of the graphic charter (colors, typography, logo).
*   Breakdown of UI/UX components.
*   Setting up the frontend development environment.