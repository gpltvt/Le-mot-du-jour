// archives.js — logique de la page archives.html

import { getMotsPrecedents } from './donnees-jeu.js';

const corps = document.getElementById('corps-archives');
const messageVide = document.getElementById('message-vide');

function formaterDate(dateISO) {
    const [annee, mois, jour] = dateISO.split('-');
    return `${jour}/${mois}/${annee}`;
}

function creerLigne({ date: dateISO, mot }) {
    const ligne = document.createElement('tr');

    const celluleDate = document.createElement('td');
    celluleDate.className = 'archive-date';
    celluleDate.textContent = formaterDate(dateISO);

    const celluleMot = document.createElement('td');
    celluleMot.className = 'archive-mot';
    celluleMot.textContent = mot;

    ligne.append(celluleDate, celluleMot);
    return ligne;
}

async function afficherArchives() {
    try {
        const historique = await getMotsPrecedents();

        if (!historique.length) {
            messageVide.hidden = false;
            return;
        }

        const historiqueTrie = [...historique].sort((a, b) => b.date.localeCompare(a.date));
        historiqueTrie.forEach((entree) => corps.appendChild(creerLigne(entree)));
    } catch (erreur) {
        messageVide.hidden = false;
        messageVide.textContent = "L'historique n'a pas pu être chargé.";
        console.error(erreur);
    }
}

afficherArchives();