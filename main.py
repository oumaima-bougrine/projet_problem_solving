from collections import deque
import time


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

# Vérifier si les chiffres initiaux sont conservés
def verifier_chiffres_initiaux(grille, grille_resolue):

    for i in range(9):
        for j in range(9):
            if grille[i][j] != 0:
                if grille[i][j] != grille_resolue[i][j]:
                    return False

    return True


# Les 5 grilles Sudoku pour les tests

grilles_tests = [

    # TEST 1 : Sudoku déjà rempli
    [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ],

    # TEST 2 : Sudoku simple
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],

    # TEST 3 : Sudoku moyen
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],

    # TEST 4 : Sudoku difficile
    [
        [0, 0, 0, 0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 9, 5, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],

    # TEST 5 : Sudoku impossible (contradiction)
    [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
]


voisins = construire_voisins()

for numero, grille_test in enumerate(grilles_tests, start=1):

    print("TEST", numero)

    grille = [ligne.copy() for ligne in grille_test]

    print("\nSudoku initial :")
    for ligne in grille:
        print(ligne)

    # Initialisation des domaines
    domaines = initialiser_domaines(grille)

    print("\nDomaines avant AC-3 :")
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                print(f"Case ({i}, {j}) : {sorted(domaines[(i, j)])}")

    # Application de AC-3
    debut_ac3 = time.perf_counter()
    resultat_ac3 = AC3(domaines, voisins)
    fin_ac3 = time.perf_counter()

    print("\nAC-3 a réussi :", resultat_ac3)

    print("\nDomaines après AC-3 :")
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                print(f"Case ({i}, {j}) : {sorted(domaines[(i, j)])}")

    print("\nTemps d'exécution AC-3 :", round(fin_ac3 - debut_ac3, 6), "secondes")

    # Choix de la case avec MRV
    case = choisir_case(domaines)

    print("\nCase choisie par MRV :", case)

    if case is not None:
        print("Valeurs possibles :", sorted(domaines[case]))

    # Résolution avec Backtracking
    etats_explores = 0

    debut = time.perf_counter()
    resultat = backtracking()
    fin = time.perf_counter()

    temps_execution = fin - debut

    if resultat:
        print("\nSudoku résolu avec succès !")

        grille_resolue = [
            [next(iter(domaines[(i, j)])) for j in range(9)]
            for i in range(9)
        ]

        print("\nSudoku résolu :")
        for ligne in grille_resolue:
            print(ligne)

        print("Chiffres initiaux conservés :", verifier_chiffres_initiaux(grille, grille_resolue))

    else:
        print("\nAucune solution trouvée !")

    print("\nTemps total de résolution :", round(temps_execution, 6), "secondes")
    print("Nombre d'états explorés :", etats_explores)

print("\nFIN DES TESTS")