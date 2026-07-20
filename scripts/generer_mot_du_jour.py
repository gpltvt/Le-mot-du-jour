"""
generer_mot_du_jour.py — exécuté chaque jour par le workflow GitHub Actions
(.github/workflows/mot-du-jour.yml). Peut aussi être lancé à la main pour
tester en local : `python scripts/generer_mot_du_jour.py`

Ce que fait ce script :
1. Charge le vocabulaire et ses vecteurs (data/mots-source/vocabulaire.json).
2. Choisit le mot du jour de façon déterministe à partir de la date, en
   excluant les mots déjà utilisés (data/historique.json) pour ne jamais
   se répéter.
3. Calcule la similarité cosinus entre le mot choisi et tous les autres
   mots du vocabulaire, puis en déduit un classement (rang 1 = le plus
   proche).
4. Écrit data/mots/AAAA-MM-JJ.json (le format attendu par js/donnees-jeu.js)
   et ajoute une entrée à data/historique.json.
"""

import json
import math
from datetime import date, timezone, datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CHEMIN_VOCABULAIRE = RACINE / "data" / "mots-source" / "vocabulaire.json"
CHEMIN_HISTORIQUE = RACINE / "data" / "historique.json"
DOSSIER_MOTS = RACINE / "data" / "mots"


def charger_json(chemin: Path, valeur_par_defaut):
    if chemin.exists():
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


def choisir_mot_du_jour(vocabulaire: dict, historique: list, aujourdhui: date) -> str:
    deja_utilises = {entree["mot"] for entree in historique}
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


def main():
    aujourdhui = datetime.now(timezone.utc).date()
    date_iso = aujourdhui.isoformat()

    vocabulaire = charger_json(CHEMIN_VOCABULAIRE, {})
    if not vocabulaire:
        raise RuntimeError(f"Vocabulaire introuvable ou vide : {CHEMIN_VOCABULAIRE}")

    historique = charger_json(CHEMIN_HISTORIQUE, [])

    chemin_du_jour = DOSSIER_MOTS / f"{date_iso}.json"
    if chemin_du_jour.exists():
        print(f"{chemin_du_jour} existe déjà, rien à faire.")
        return

    mot_cible = choisir_mot_du_jour(vocabulaire, historique, aujourdhui)
    classement = generer_classement(vocabulaire, mot_cible)

    DOSSIER_MOTS.mkdir(parents=True, exist_ok=True)
    with open(chemin_du_jour, "w", encoding="utf-8") as fichier:
        json.dump({"motCible": mot_cible, "classement": classement}, fichier, ensure_ascii=False)

    historique.append({"date": date_iso, "mot": mot_cible})
    with open(CHEMIN_HISTORIQUE, "w", encoding="utf-8") as fichier:
        json.dump(historique, fichier, ensure_ascii=False, indent=2)

    print(f"Mot du {date_iso} généré : {mot_cible} ({len(classement)} mots classés)")


if __name__ == "__main__":
    main()