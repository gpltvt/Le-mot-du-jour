"""
generer_mot_du_jour.py — exécuté chaque jour par le workflow GitHub Actions
(.github/workflows/mot-du-jour.yml). Peut aussi être lancé à la main pour
tester en local : `python scripts/generer_mot_du_jour.py`

Ce que fait ce script :
1. Charge le vocabulaire et ses vecteurs (data/mots-source/vocabulaire.json).
2. Choisit le mot du jour de façon déterministe à partir de la date, en
   excluant tous les mots déjà utilisés les jours précédents (déduits des
   fichiers data/mots/*.json existants) pour ne jamais se répéter.
3. Calcule la similarité cosinus entre le mot choisi et tous les autres
   mots du vocabulaire, puis en déduit un classement (rang 1 = le plus
   proche).
4. Écrit data/mots/AAAA-MM-JJ.json (le format attendu par js/donnees-jeu.js).
5. Publie dans data/historique.json le mot d'HIER (jamais celui du jour même
   qui est encore en cours de partie) — c'est ce qui empêche archives.html
   de révéler la réponse du jour en cours.
"""

import json
import math
from datetime import date, timedelta, timezone, datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CHEMIN_VOCABULAIRE = RACINE / "data" / "mots-source" / "vocabulaire.json"
CHEMIN_HISTORIQUE = RACINE / "data" / "historique.json"
DOSSIER_MOTS = RACINE / "data" / "mots"


def charger_json(chemin: Path, valeur_par_defaut):
    if chemin.exists() and chemin.stat().st_size > 0:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    return valeur_par_defaut


def similarite_cosinus(vecteur_a, vecteur_b) -> float:
    produit_scalaire = sum(a * b for a, b in zip(vecteur_a, vecteur_b))
    norme_a = math.sqrt(sum(a * a for a in vecteur_a))
    norme_b = math.sqrt(sum(b * b for b in vecteur_b))
    if norme_a == 0 or norme_b == 0:
        return 0.0
    return produit_scalaire / (norme_a * norme_b)


def mots_deja_generes() -> set:
    """Scanne data/mots/*.json (tous les jours déjà générés, y compris
    aujourd'hui s'il existe déjà) pour ne jamais reproposer un mot cible."""
    deja = set()
    if DOSSIER_MOTS.exists():
        for fichier in DOSSIER_MOTS.glob("*.json"):
            if fichier.name == "mock.json":
                continue
            contenu = charger_json(fichier, {})
            if contenu.get("motCible"):
                deja.add(contenu["motCible"])
    return deja


def choisir_mot_du_jour(vocabulaire: dict, deja_utilises: set, aujourdhui: date) -> str:
    candidats = sorted(m for m in vocabulaire if m not in deja_utilises)

    if not candidats:
        raise RuntimeError(
            "Tous les mots du vocabulaire ont déjà été utilisés : "
            "il faut en ajouter de nouveaux dans vocabulaire.json."
        )

    # Choix déterministe : même résultat pour tout le monde ce jour-là,
    # mais qui change automatiquement chaque jour.
    seed = int(aujourdhui.strftime("%Y%m%d"))
    return candidats[seed % len(candidats)]


def generer_classement(vocabulaire: dict, mot_cible: str) -> dict:
    vecteur_cible = vocabulaire[mot_cible]
    scores = []
    for mot, vecteur in vocabulaire.items():
        if mot == mot_cible:
            continue
        scores.append((mot, similarite_cosinus(vecteur_cible, vecteur)))

    # Similarité la plus haute = rang 1
    scores.sort(key=lambda item: item[1], reverse=True)
    return {mot: rang + 1 for rang, (mot, _score) in enumerate(scores)}


def publier_mot_de_la_veille(aujourdhui: date) -> None:
    """Ajoute à l'historique le mot d'hier (jamais celui du jour même),
    une fois que sa journée est terminée."""
    hier = aujourdhui - timedelta(days=1)
    hier_iso = hier.isoformat()

    chemin_hier = DOSSIER_MOTS / f"{hier_iso}.json"
    if not chemin_hier.exists():
        return  # rien à publier (par ex. tout premier jour du site)

    historique = charger_json(CHEMIN_HISTORIQUE, [])
    deja_publie = any(entree["date"] == hier_iso for entree in historique)
    if deja_publie:
        return

    contenu_hier = charger_json(chemin_hier, {})
    mot_hier = contenu_hier.get("motCible")
    if not mot_hier:
        return

    historique.append({"date": hier_iso, "mot": mot_hier})
    with open(CHEMIN_HISTORIQUE, "w", encoding="utf-8") as fichier:
        json.dump(historique, fichier, ensure_ascii=False, indent=2)

    print(f"Historique mis à jour avec le mot du {hier_iso} : {mot_hier}")


def main():
    aujourdhui = datetime.now(timezone.utc).date()
    date_iso = aujourdhui.isoformat()

    vocabulaire = charger_json(CHEMIN_VOCABULAIRE, {})
    if not vocabulaire:
        raise RuntimeError(f"Vocabulaire introuvable ou vide : {CHEMIN_VOCABULAIRE}")

    chemin_du_jour = DOSSIER_MOTS / f"{date_iso}.json"
    if not chemin_du_jour.exists():
        deja_utilises = mots_deja_generes()
        mot_cible = choisir_mot_du_jour(vocabulaire, deja_utilises, aujourdhui)
        classement = generer_classement(vocabulaire, mot_cible)

        DOSSIER_MOTS.mkdir(parents=True, exist_ok=True)
        with open(chemin_du_jour, "w", encoding="utf-8") as fichier:
            json.dump({"motCible": mot_cible, "classement": classement}, fichier, ensure_ascii=False)

        print(f"Mot du {date_iso} généré : {mot_cible} ({len(classement)} mots classés)")
    else:
        print(f"{chemin_du_jour} existe déjà, rien à régénérer.")

    # Que le mot du jour vienne d'être généré ou existait déjà, on en profite
    # pour vérifier si le mot d'hier peut être publié dans l'historique.
    publier_mot_de_la_veille(aujourdhui)


if __name__ == "__main__":
    main()