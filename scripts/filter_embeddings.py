"""
filter_embeddings.py — À LANCER UNE SEULE FOIS, EN LOCAL (pas dans GitHub Actions)

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
   python filter_embeddings.py chemin/vers/cc.fr.300.vec

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
    "abeille", "abricot", "acteur", "aigle", "aiguille", "ail", "air", "anniversaire",
    "appartement", "araignée", "arbre", "argent", "armoire", "assiette", "automne",
    "avion", "avocat", "aéroport", "bague", "baleine", "ballon", "banane", "banque",
    "bateau", "batterie", "beurre", "bibliothèque", "biche", "bijou", "billet", "bière",
    "bois", "botanique", "botte", "bouche", "boucher", "boulanger", "bouleau", "bouquet",
    "boîte", "branche", "bras", "brosse", "brouillard", "buisson", "bureau", "bus",
    "bœuf", "cadeau", "café", "cahier", "caméra", "canapé", "canard", "carotte", "carte",
    "casserole", "cave", "ceinture", "cerf", "cerise", "chaise", "chambre", "champ",
    "champignon", "chanson", "chanteur", "chapeau", "chat", "chaussette", "chaussure",
    "cheminée", "chemise", "cheval", "cheveux", "chien", "chocolat", "château", "chèvre",
    "chêne", "ciel", "ciseaux", "citron", "clavier", "clou", "clé", "cochon", "coiffeur",
    "colline", "coq", "corbeau", "corde", "cou", "couleur", "course", "coussin",
    "couteau", "couverture", "crabe", "crayon", "crevette", "crocodile", "cuillère",
    "cuisine", "cuisinier", "cœur", "danse", "dauphin", "dent", "dessin", "doigt", "dos",
    "désert", "eau", "escalier", "facteur", "farine", "fauteuil", "fenêtre", "ferme",
    "fermier", "feu", "feuille", "fil", "fleur", "fleuve", "flûte", "football", "forêt",
    "fougère", "four", "fourchette", "fourmi", "fraise", "frigo", "fromage", "fruit",
    "fumée", "fête", "gant", "garage", "gare", "genou", "girafe", "glace", "graine",
    "grenier", "grenouille", "grotte", "guitare", "gâteau", "herbe", "hibou", "hiver",
    "horloge", "huile", "hérisson", "hôpital", "hôtel", "imprimante", "infirmier",
    "ingénieur", "jambe", "jardin", "jonquille", "journal", "jupe", "jus", "kangourou",
    "lac", "lait", "lampe", "lapin", "lettre", "lion", "lit", "livre", "loup", "lumière",
    "lune", "légume", "lézard", "magasin", "main", "maison", "manteau", "marché",
    "marteau", "match", "melon", "mer", "miroir", "moineau", "montagne", "montre",
    "moto", "mouche", "mousse", "moustique", "mouton", "mur", "musicien", "musique",
    "musée", "mécanicien", "médecin", "métal", "métro", "natation", "nature", "neige",
    "nez", "nuage", "océan", "oie", "oignon", "oiseau", "ombre", "orage", "orange",
    "ordinateur", "oreille", "oreiller", "ours", "outil", "pain", "panier", "pantalon",
    "papier", "papillon", "parapluie", "parterre", "patate", "peau", "peigne", "peintre",
    "peinture", "pelouse", "photo", "piano", "pied", "pierre", "pigeon", "pingouin",
    "pivoine", "pièce", "placard", "place", "plage", "plastique", "pluie", "poire",
    "poisson", "poivre", "policier", "pollen", "pomme", "pompier", "pont", "porc",
    "port", "porte", "poule", "poulet", "poêle", "printemps", "professeur", "prune",
    "pull", "pâtes", "pétale", "pêche", "pêcheur", "racine", "radio", "raisin", "rat",
    "renard", "requin", "restaurant", "rideau", "rivière", "riz", "robe", "rocher",
    "rose", "route", "rue", "récolte", "sable", "sac", "salade", "salon", "sanglier",
    "sapin", "savon", "sculpture", "sel", "serpent", "serre", "serrure", "serviette",
    "singe", "soleil", "soupe", "souris", "stade", "stylo", "sucre", "table", "tambour",
    "tapis", "tarte", "tennis", "terre", "thé", "tigre", "tiroir", "toit", "tomate",
    "tonnerre", "tortue", "tour", "train", "tronc", "tulipe", "téléphone", "télévision",
    "tête", "usine", "vache", "vague", "valise", "vallée", "vase", "vent", "ventre",
    "verre", "vert", "veste", "viande", "victoire", "village", "ville", "vin",
    "vinaigre", "violon", "vis", "visage", "voiture", "volcan", "voyage", "vélo",
    "zèbre", "écharpe", "échelle", "éclair", "école", "écran", "écrivain", "écureuil",
    "église", "éléphant", "épaule", "équipe", "étagère", "étoile", "été", "île", "œil",
    "œuf",
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
        print("Usage : python filter_embeddings.py chemin/vers/cc.fr.300.vec")
        sys.exit(1)
    filtrer(sys.argv[1], "data/mots-source/vocabulaire.json")