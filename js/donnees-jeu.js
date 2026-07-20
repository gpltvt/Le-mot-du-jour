const CHEMIN_MOCK = 'data/mots/mock.json';

function dateDuJourISO() {
    const aujourdhui = new Date();
    return aujourdhui.toISOString().slice(0, 10);
}

export async function getMotDuJour() {
    const reponse = await fetch(CHEMIN_MOCK);
    if (!reponse.ok) {
        throw new Error("Impossible de charger le mot du jour");
    }
    return reponse.json();
}

export async function proposerMot(mot) {
    const motNormalise = mot.trim().toLowerCase();
    const { motCible, classement } = await getMotDuJour();

    if (motNormalise === motCible) {
        return { mot: motNormalise, rang: 1, trouve: true };
    }

    const rang = classement[motNormalise] ?? null;
    return { mot: motNormalise, rang, trouve: false };
}

export async function getMotsPrecedents() {
    const reponse = await fetch('data/historique.json');
    if (!reponse.ok) {
        throw new Error("Impossible de charger l'historique");
    }
    return reponse.json();
}