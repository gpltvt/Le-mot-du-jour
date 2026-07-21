// jeu.js — logique de la page jouer.html

import { proposerMot, getMotDuJour, dateDuJourISO } from './donnees-jeu.js';

const formulaire = document.getElementById('formulaire-essai');
const champMot = document.getElementById('champ-mot');
const message = document.getElementById('message-jeu');
const listeEssais = document.getElementById('liste-essais');

const PREFIXE_STOCKAGE = 'mdj-essais-';
const cleStockageAujourdhui = PREFIXE_STOCKAGE + dateDuJourISO();

const essaisJoues = new Map(); // mot -> résultat
let partieTrouvee = false;

// ---------- Sauvegarde locale (survit à un rafraîchissement de page) ----------

// Empreinte simple du contenu du mot du jour : permet de détecter si les
// essais sauvegardés correspondent à un mot du jour différent de celui
// actuellement chargé (ex. bascule du mock vers le vrai fichier du jour),
// et dans ce cas d'ignorer la sauvegarde périmée plutôt que de la restaurer.
function signatureDuJour(donneesMotDuJour) {
    const chaine = JSON.stringify(donneesMotDuJour);
    let hash = 0;
    for (let i = 0; i < chaine.length; i++) {
        hash = (hash * 31 + chaine.charCodeAt(i)) | 0;
    }
    return hash;
}

async function sauvegarderEssais() {
    try {
        const motDuJourActuel = await getMotDuJour();
        localStorage.setItem(cleStockageAujourdhui, JSON.stringify({
            signature: signatureDuJour(motDuJourActuel),
            essais: [...essaisJoues.values()],
        }));
    } catch (erreur) {
        // navigation privée, quota plein, etc. : on continue sans bloquer le jeu
        console.warn("Sauvegarde locale impossible :", erreur);
    }
}

function nettoyerAnciennesSauvegardes() {
    try {
        Object.keys(localStorage)
            .filter((cle) => cle.startsWith(PREFIXE_STOCKAGE) && cle !== cleStockageAujourdhui)
            .forEach((cle) => localStorage.removeItem(cle));
    } catch {
        // rien de grave si on ne peut pas nettoyer
    }
}

async function restaurerEssais() {
    let sauvegarde;
    try {
        sauvegarde = localStorage.getItem(cleStockageAujourdhui);
    } catch {
        return;
    }
    if (!sauvegarde) return;

    let donneesSauvegardees;
    try {
        donneesSauvegardees = JSON.parse(sauvegarde);
    } catch (erreur) {
        console.warn("Sauvegarde locale illisible, on repart de zéro :", erreur);
        return;
    }

    try {
        const motDuJourActuel = await getMotDuJour();
        if (signatureDuJour(motDuJourActuel) !== donneesSauvegardees.signature) {
            // Le mot du jour a changé depuis cette sauvegarde : elle est périmée.
            try { localStorage.removeItem(cleStockageAujourdhui); } catch { /* tant pis */ }
            return;
        }
    } catch (erreur) {
        console.warn("Vérification de la sauvegarde impossible, on repart de zéro :", erreur);
        return;
    }

    donneesSauvegardees.essais.forEach((resultat) => essaisJoues.set(resultat.mot, resultat));
    reafficherEssais();

    const resultatTrouve = [...essaisJoues.values()].find((resultat) => resultat.trouve);
    if (resultatTrouve) {
        partieTrouvee = true;
        const nbEssais = essaisJoues.size;
        message.textContent = `Bravo, vous avez trouvé "${resultatTrouve.mot}" en ${nbEssais} essai${nbEssais > 1 ? 's' : ''} !`;
        message.className = 'message-jeu trouve';
        champMot.disabled = true;
    }
}

// ---------- Affichage ----------

function categorie(rang, trouve) {
    if (trouve) return 'trouve';
    if (rang !== null && rang <= 10) return 'chaud';
    if (rang !== null && rang <= 100) return 'tiede';
    return null; // froid = style par défaut, pas de modificateur de classe
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
    spanRang.textContent = trouve ? '🏆' : (rang !== null ? `${rang}ᵉ` : '—');

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
        sauvegarderEssais();
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

nettoyerAnciennesSauvegardes();
restaurerEssais();