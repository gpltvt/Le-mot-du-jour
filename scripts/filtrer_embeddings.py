"""
filtrer_embeddings.py — À LANCER UNE SEULE FOIS, EN LOCAL (pas dans GitHub Actions)

Ce script prend le fichier officiel de vecteurs français fastText (plusieurs
Go, impossible à stocker sur GitHub) et n'en garde que les mots qui nous
intéressent, pour produire un petit fichier (quelques Mo) qu'on committe
dans le dépôt. C'est ce petit fichier que le workflow GitHub Actions utilisera
ensuite chaque jour, sans jamais retélécharger le gros fichier original.

ÉTAPES (à faire une fois sur ton ordinateur) :

1. Télécharge les vecteurs français officiels (~1,3 Go compressé) :
   https://fasttext.cc/docs/en/crawl-vectors.html
   -> section "French", fichier "cc.fr.300.vec.gz"

2. Décompresse-le (ex. avec 7-Zip sous Windows, ou `gunzip cc.fr.300.vec.gz`).

3. Complète la liste MOTS_A_GARDER ci-dessous avec ton vocabulaire de jeu
   (les mots candidats pour être "mot du jour", + les mots courants qui
   serviront à calculer le classement de proximité — quelques milliers de
   mots suffisent, pas besoin des 2 millions du fichier original).

4. Lance :
   python filtrer_embeddings.py chemin/vers/cc.fr.300.vec

5. Le script produit data/mots-source/vocabulaire.json — committe-le dans
   le dépôt Git. C'est fait, tu n'auras plus jamais besoin de refaire cette
   étape (sauf si tu veux enrichir le vocabulaire plus tard).
"""

import json
import sys
from pathlib import Path

# TODO : remplace par ta vraie liste de mots (idéalement quelques milliers,
# noms communs concrets pour un jeu agréable à jouer). Exemple minimal :
MOTS_A_GARDER = {
    "tulipe", "fleur", "rose", "jardin", "jonquille", "pivoine", "bouquet",
    "pétale", "vase", "printemps", "pollen", "abeille", "parterre", "serre",
    "botanique", "couleur", "nature", "arbre", "vert", "maison", "voiture",
    "ordinateur", "hollande", "bulbe",
    # ... complète ici avec ton vocabulaire complet
}


def filtrer(chemin_vecteurs_bruts: str, chemin_sortie: str) -> None:
    vecteurs = {}
    with open(chemin_vecteurs_bruts, "r", encoding="utf-8") as fichier:
        premiere_ligne = fichier.readline()  # en-tête fastText : "nb_mots dimensions"
        for ligne in fichier:
            morceaux = ligne.rstrip().split(" ")
            mot = morceaux[0]
            if mot in MOTS_A_GARDER:
                vecteurs[mot] = [float(x) for x in morceaux[1:]]

    manquants = MOTS_A_GARDER - vecteurs.keys()
    if manquants:
        print(f"Attention, mots absents du fichier source : {sorted(manquants)}")

    Path(chemin_sortie).parent.mkdir(parents=True, exist_ok=True)
    with open(chemin_sortie, "w", encoding="utf-8") as fichier:
        json.dump(vecteurs, fichier, ensure_ascii=False)

    print(f"{len(vecteurs)} mots écrits dans {chemin_sortie}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python filtrer_embeddings.py chemin/vers/cc.fr.300.vec")
        sys.exit(1)
    filtrer(sys.argv[1], "data/mots-source/vocabulaire.json")