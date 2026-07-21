import json
import sys
from pathlib import Path

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
        premiere_ligne = fichier.readline()
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