// donnees-jeu.js
//
// Façade d'accès aux données du jeu. C'est la SEULE partie du code qui doit
// changer le jour où le site passe d'un JSON précalculé à un vrai backend :
// le reste de l'application (jeu, archives...) n'appelle jamais fetch()
// directement, seulement les fonctions ci-dessous.
//
// Pour l'instant, on lit un unique fichier de mock (data/mots/mock.json)
// quel que soit le jour, en attendant le script Python qui génèrera un
// vrai fichier par date à partir des embeddings français.

const CHEMIN_MOCK = 'data/mots/mock.json'; // conservé en secours, voir plus bas

export function dateDuJourISO() {
    const aujourdhui = new Date();
    return aujourdhui.toISOString().slice(0, 10);
}

/**
 * Retourne les données du mot du jour : { motCible, classement }.
 * `classement` associe un mot en minuscules à son rang de proximité.
 */
export async function getMotDuJour() {
    const reponse = await fetch(`data/mots/${dateDuJourISO()}.json`);
    if (reponse.ok) {
        return reponse.json();
    }

    // Secours : si le fichier du jour n'existe pas encore (le workflow
    // GitHub Actions n'a pas encore tourné, ou test en local sans avoir
    // lancé le script), on retombe sur le mock pour ne pas casser la page.
    console.warn("Mot du jour introuvable, utilisation du mock de secours.");
    const reponseMock = await fetch(CHEMIN_MOCK);
    if (!reponseMock.ok) {
        throw new Error("Impossible de charger le mot du jour");
    }
    return reponseMock.json();
}

/**
 * Évalue un essai du joueur et retourne { mot, rang, trouve }.
 * rang vaut null si le mot n'apparaît pas dans le classement précalculé.
 */
export async function proposerMot(mot) {
    const motNormalise = mot.trim().toLowerCase();
    const { motCible, classement } = await getMotDuJour();

    if (motNormalise === motCible) {
        return { mot: motNormalise, rang: 1, trouve: true };
    }

    const rang = classement[motNormalise] ?? null;
    return { mot: motNormalise, rang, trouve: false };
}

/**
 * Retourne l'historique des mots précédents : [{ date, mot }, ...].
 * Pas encore utilisée (page archives.html à venir).
 */
export async function getMotsPrecedents() {
    const reponse = await fetch('data/historique.json');
    if (!reponse.ok) {
        throw new Error("Impossible de charger l'historique");
    }
    return reponse.json();
}