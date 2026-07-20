import { proposerMot } from './donnees-jeu.js';

const formulaire = document.getElementById('formulaire-essai');
const champMot = document.getElementById('champ-mot');
const message = document.getElementById('message-jeu');
const listeEssais = document.getElementById('liste-essais');

const essaisJoues = new Map();
let partieTrouvee = false;

function categorie(rang, trouve) {
    if (trouve) return 'trouve';
    if (rang !== null && rang <= 10) return 'chaud';
    if (rang !== null && rang <= 100) return 'tiede';
    return null;
}

function pourcentage(rang, trouve) {
    if (trouve) return 100;
    if (rang === null) return 2;
    return Math.max(3, Math.round(100 / (1 + rang / 50)));
}

function libelle(rang, trouve) {
    if (trouve) return 'trouvé';
    if (rang === null) return 'hors classement';
    if (rang <= 10) return 'chaud';
    if (rang <= 100) return 'tiède';
    return 'froid';
}

function creerLigne({ mot, rang, trouve }) {
    const ligne = document.createElement('div');
    const cat = categorie(rang, trouve);
    ligne.className = 'demo-ligne' + (cat ? ` demo-ligne--${cat}` : '');

    const spanRang = document.createElement('span');
    spanRang.className = 'demo-rang';
    spanRang.textContent = trouve ? 'Gagné!' : (rang !== null ? `${rang}ᵉ` : '—');

    const spanMot = document.createElement('span');
    spanMot.className = 'demo-mot';
    spanMot.textContent = mot;

    const jauge = document.createElement('span');
    jauge.className = 'demo-jauge';
    const remplissage = document.createElement('span');
    remplissage.className = 'demo-jauge-remplissage';
    remplissage.style.setProperty('--valeur', `${pourcentage(rang, trouve)}%`);
    jauge.appendChild(remplissage);

    const spanEtat = document.createElement('span');
    spanEtat.className = 'demo-froid';
    spanEtat.textContent = libelle(rang, trouve);

    ligne.append(spanRang, spanMot, jauge, spanEtat);
    return ligne;
}

function reafficherEssais() {
    listeEssais.innerHTML = '';
    const essaisTries = [...essaisJoues.values()].sort((a, b) => {
        if (a.trouve) return -1;
        if (b.trouve) return 1;
        const rangA = a.rang ?? Infinity;
        const rangB = b.rang ?? Infinity;
        return rangA - rangB;
    });
    essaisTries.forEach((resultat) => listeEssais.appendChild(creerLigne(resultat)));
}

formulaire.addEventListener('submit', async (evenement) => {
    evenement.preventDefault();
    if (partieTrouvee) return;

    const mot = champMot.value.trim().toLowerCase();
    if (!mot) return;

    if (essaisJoues.has(mot)) {
        message.textContent = `Vous avez déjà proposé "${mot}".`;
        message.className = 'message-jeu';
        champMot.value = '';
        return;
    }

    try {
        const resultat = await proposerMot(mot);
        essaisJoues.set(mot, resultat);
        reafficherEssais();
        champMot.value = '';

        if (resultat.trouve) {
            partieTrouvee = true;
            const nbEssais = essaisJoues.size;
            message.textContent = `Bravo, vous avez trouvé "${mot}" en ${nbEssais} essai${nbEssais > 1 ? 's' : ''} !`;
            message.className = 'message-jeu trouve';
            champMot.disabled = true;
        } else {
            message.textContent = '';
            message.className = 'message-jeu';
        }
    } catch (erreur) {
        message.textContent = "Le mot du jour n'a pas pu être chargé.";
        message.className = 'message-jeu';
        console.error(erreur);
    }

    champMot.focus();
});