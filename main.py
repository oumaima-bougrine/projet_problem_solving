from sudoku import Sudoku
from collections import deque
import time

# Génerer un plateau Sudoku
puzzle = Sudoku(3).difficulty(0.5)

# Récuperer la grille
grille = puzzle.board

# Remplacer les cases vides par 0
grille = [
    [0 if valeur is None else valeur for valeur in ligne]
    for ligne in grille
]

# Afficher la grille
print("Sudoku initial :")

for ligne in grille:
    print(ligne)


# Initialiser les domaines
def initialiser_domaines(grille):
    domaines = {}

    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                domaines[(i, j)] = set(range(1, 10))
            else:
                domaines[(i, j)] = {grille[i][j]}

    return domaines


# Construire les voisins
def construire_voisins():
    voisins = {}

    for i in range(9):
        for j in range(9):
            case = (i, j)
            voisins[case] = set()

            # Cases de la même ligne et la même colonne
            for k in range(9):
                voisins[case].add((i, k))
                voisins[case].add((k, j))

            # Trouver le début du bloc 3x3
            debut_i = (i // 3) * 3
            debut_j = (j // 3) * 3

            # Ajouter les cases du bloc
            for x in range(debut_i, debut_i + 3):
                for y in range(debut_j, debut_j + 3):
                    voisins[case].add((x, y))

            # Supprimer la case elle-même
            voisins[case].discard(case)

    return voisins


# Réviser les domaines
def revise(domaines, xi, xj):

    modifie = False

    for valeur in domaines[xi].copy():

        # Vérifier s'il existe une valeur différente dans le domaine de la case voisine
        if not any(
            valeur != valeur_voisine
            for valeur_voisine in domaines[xj]
        ):

            domaines[xi].remove(valeur)
            modifie = True

    return modifie


# Algorithme AC-3
def AC3(domaines, voisins):

    # Initialiser la file des arcs
    file = deque()

    for xi in domaines:
        for xj in voisins[xi]:
            file.append((xi, xj))

    # Parcourir les arcs tant que la file n'est pas vide
    while file:

        xi, xj = file.popleft()

        # Réviser le domaine de xi par rapport à xj
        if revise(domaines, xi, xj):

            # Vérifier si le domaine est vide
            if len(domaines[xi]) == 0:
                return False

            # Ajouter les autres voisines dans la file
            for xk in voisins[xi]:
                if xk != xj:
                    file.append((xk, xi))

    return True


# Vérifier si le Sudoku est résolu
def sudoku_resolu(domaines):

    for case in domaines:
        if len(domaines[case]) != 1:
            return False

    return True


# Choisir la prochaine case (avec le plus petit domaine)
def choisir_case(domaines):

    meilleure_case = None
    taille_minimale = 10

    for case in domaines:

        taille_domaine = len(domaines[case])

        if 1 < taille_domaine < taille_minimale:
            taille_minimale = taille_domaine
            meilleure_case = case

    return meilleure_case



# Algorithme Backtracking avec AC-3
def backtracking():

    global domaines, voisins, etats_explores

    # Compter chaque appel à Backtracking
    etats_explores += 1

    # Appliquer AC-3
    if not AC3(domaines, voisins):
        return False

    # Vérifier si le Sudoku est résolu
    if sudoku_resolu(domaines):
        return True

    # Choisir une case
    case = choisir_case(domaines)

    # Essayer chaque valeur possible
    for valeur in domaines[case].copy():

        # Sauvegarder les domaines actuels
        anciens_domaines = {
            c: valeurs.copy()
            for c, valeurs in domaines.items()
        }

        # Affécter une valeur à la case choisie
        domaines[case] = {valeur}

        if backtracking():
            return True

        domaines = anciens_domaines

    return False




# Les tests

domaines = initialiser_domaines(grille)
voisins = construire_voisins()

# Tester la fonction initialiser_domaines et la fonction voisin construire_voisins
print("\nDomaines de la case (0, 1) :")
print(domaines[(0, 1)])

print("\nVoisins de la case (0, 1) :")
print(voisins[(0, 1)])


# Teste du AC-3
print("\nApplication de AC-3")
resultat = AC3(domaines, voisins)

if resultat:
    print("AC-3 terminé sans contradiction !")
else:
    print("Contradiction détectée !")

print("\nDomaines après AC-3 :")
for i in range(9):
    for j in range(9):
        if grille[i][j] == 0:
            print(f"Case ({i}, {j}) : {domaines[(i, j)]}")

case = choisir_case(domaines)

print("\nCase choisite:", case)

if case is not None:
    print("Valeurs possibles :", domaines[case])


# Vérifier si les valeurs initiales sont modifiées 
def verifier_chiffres_initiaux(grille_initiale, grille_resolue):
    for i in range(9):
        for j in range(9):

            # Vérifier uniquement les cases déjà remplies
            if grille_initiale[i][j] != 0:

                if grille_initiale[i][j] != grille_resolue[i][j]:
                    return False

    return True


# TEST DU BACKTRACKING

# Initialiser les domaines et les voisins
domaines = initialiser_domaines(grille)
voisins = construire_voisins()

print("TEST DU BACKTRACKING")

print("\nApplication de AC-3 et Backtracking")

# Initialiser le compteur
etats_explores = 0

# Démarrer le chronomètre
debut = time.perf_counter()

# Lancer la résolution
resultat = backtracking()

# Arrêter le chronomètre
fin = time.perf_counter()

# Calculer le temps d'exécution
temps_execution = fin - debut

if resultat:

    print("\nSudoku résolu avec succès !")

    # Transformer les domaines en grille Sudoku
    grille_resolue = []

    for i in range(9):
        ligne = []

        for j in range(9):
            valeur = next(iter(domaines[(i, j)]))
            ligne.append(valeur)

        grille_resolue.append(ligne)

    # Afficher le Sudoku final
    print("\nSudoku résolu :")

    for ligne in grille_resolue:
        print(ligne)

    # Vérifier les chiffres initiaux
    if verifier_chiffres_initiaux(grille, grille_resolue):
        print("Les chiffres initiaux sont conservés !")
    else:
        print("Erreur : un chiffre initial a été modifié !")

else:
    print("\nAucune solution trouvée !")

# Afficher les performances
print("EVALUATION DES PERFORMANCES")

print("Temps d'exécution :", round(temps_execution, 6), "secondes")
print("Nombre d'états explorés :", etats_explores)
