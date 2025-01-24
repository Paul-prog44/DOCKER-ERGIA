# Étape 1 : Construire l'application Angular
FROM node:18 AS build

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application
COPY . .

# Construire l'application en mode production
RUN npm run build --prod

# Étape 2 : Utiliser Nginx pour servir l'application
FROM nginx:alpine

# Copier le fichier de configuration nginx si nécessaire (facultatif)
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copier les fichiers construits dans le répertoire nginx
COPY --from=build /app/dist/ergiafront/browser /usr/share/nginx/html

# Commande par défaut pour démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
