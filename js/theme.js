// theme.js — bascule clair/sombre, partagée par toutes les pages.
// Chargé en <script> classique (pas en module) et placé tôt dans <head>
// pour appliquer le thème avant l'affichage et éviter un flash de thème clair.

(function () {
    const CLE_STOCKAGE = 'mdj-theme';

    function themeSauvegarde() {
        try {
            return localStorage.getItem(CLE_STOCKAGE);
        } catch {
            return null;
        }
    }

    function appliquerTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }

    // Thème choisi précédemment, sinon préférence système, sinon clair par défaut.
    const preferenceSysteme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'sombre'
        : 'clair';
    const themeInitial = themeSauvegarde() || preferenceSysteme;
    appliquerTheme(themeInitial);

    document.addEventListener('DOMContentLoaded', () => {
        const bouton = document.getElementById('bouton-theme');
        if (!bouton) return;

        function majIcone(theme) {
            bouton.textContent = theme === 'sombre' ? '☀️' : '🌙';
            bouton.setAttribute(
                'aria-label',
                theme === 'sombre' ? 'Passer au thème clair' : 'Passer au thème sombre'
            );
        }

        majIcone(document.documentElement.getAttribute('data-theme'));

        bouton.addEventListener('click', () => {
            const themeActuel = document.documentElement.getAttribute('data-theme');
            const nouveauTheme = themeActuel === 'sombre' ? 'clair' : 'sombre';
            appliquerTheme(nouveauTheme);
            majIcone(nouveauTheme);
            try {
                localStorage.setItem(CLE_STOCKAGE, nouveauTheme);
            } catch {
                // tant pis, le choix ne survivra pas au rechargement
            }
        });
    });
})();