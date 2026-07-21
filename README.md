# Le Mot du Jour

> **Un mot caché, une réponse par jour.**  
> Un jeu de devinette sémantique quotidien, développé en JavaScript Vanilla.

**Démo en ligne :** [https://gpltvt.github.io/Le-mot-du-jour/](https://gpltvt.github.io/Le-mot-du-jour/)

## À propos du projet

**Le Mot du Jour** est un jeu quotidien où le joueur doit deviner un mot secret en proposant des essais successifs. À chaque tentative, l'application fournit un score de proximité (rang sémantique, jauges visuelles et indicateurs de température) pour guider le joueur vers la solution.

### Fonctionnalités clés

- **Défi quotidien :** Un nouveau mot à deviner chaque jour.
- **Proximité sémantique :** Classement dynamique des propositions avec jauges de progression et indicateurs de température (*Froid*, *Tiède*, *Chaud*, *Trouvé*).
- **Sauvegarde automatique :** Vos essais du jour sont conservés localement (`localStorage`) pour ne pas perdre votre progression en cas de rafraîchissement de la page.
- **Design soigné :** Interface épurée au style éditorial (palette ivoire chaud, vert forêt et finitions or) développée sur-mesure sans framework CSS.
- **Responsive & Accessible :** Adapté à tous les écrans (mobiles, tablettes, ordinateurs) avec prise en compte des préférences de mouvement réduit (`prefers-reduced-motion`).
- **Archives & Règles :** Pages dédiées pour consulter les règles du jeu et revoir les mots des jours précédents.

## Aperçu visuel & DA

Le jeu se distingue par son identité visuelle personnalisée :
- **Typographies :** *Great Vibes* (titres principaux), *Cormorant Garamond* (sous-titres) et *Poppins* (corps de texte).
- **Palette chromatique :** Ivoire chaud (`#f7f2e6`), Vert forêt profond (`#2e4126`) et touches Dorées (`#b3892f`).

## Stack technique

- **Frontend :** HTML5, CSS3 (Variables CSS, Flexbox, CSS Grid, Animations).
- **JavaScript :** ES6+ Vanilla (Modules JS, `async/await`, API `fetch`, `localStorage`).
- **Données :** Fichiers JSON précalculés par date avec fallback automatique vers un jeu de données mock.
- **Hébergement :** GitHub Pages.

## Structure du projet

```text
Le-mot-du-jour/
├── index.html              # Page d'accueil et présentation
├── jouer.html              # Page principale du jeu
├── regles.html             # Explications et règles
├── archives.html           # Historique des mots passés
├── mentions_legales.html   # Informations légales
├── css/
│   └── style.css           # Feuille de style unique et responsive
├── js/
│   ├── donnees-jeu.js      # Façade d'accès aux données (Fetch & Fallback JSON)
│   └── jeu.js              # Logique de jeu, interface & sauvegarde locale
└── data/
    ├── historique.json     # Archive des anciens mots
    └── mots/               # Données des mots quotidiens (format YYYY-MM-DD.json)
        └── mock.json       # Données de secours en local
