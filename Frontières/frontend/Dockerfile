# Dockerfile pour le frontend Nuxt.js - Millésime Sans Frontières
FROM node:20-alpine AS base

# Installer les dépendances système nécessaires
RUN apk add --no-cache libc6-compat

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./
COPY nuxt.config.ts ./
COPY tailwind.config.ts ./

# Installer les dépendances
RUN npm install && npm cache clean --force

# Copier le code source
COPY . .

# Construire l'application
RUN npm run build

# Étape de production
FROM node:20-alpine AS production

# Créer un utilisateur non-root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nuxtjs

# Installer les dépendances système
RUN apk add --no-cache libc6-compat

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et l'application construite
COPY --from=base --chown=nuxtjs:nodejs /app/package*.json ./
COPY --from=base --chown=nuxtjs:nodejs /app/node_modules ./node_modules
COPY --from=base --chown=nuxtjs:nodejs /app/.nuxt ./.nuxt
COPY --from=base --chown=nuxtjs:nodejs /app/.output ./.output
COPY --from=base --chown=nuxtjs:nodejs /app/public ./public

# Changer vers l'utilisateur non-root
USER nuxtjs

# Exposer le port
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

# Commande de démarrage
CMD ["npm", "run", "dev"]
