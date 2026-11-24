from sudoku import Sudoku

# Generer un plateau Sudoku
puzzle = Sudoku(3).difficulty(0.5)

# Recuperer la grille
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

def initialiser_domaines(grille):
    domaines = {}

    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                domaines[(i, j)] = set(range(1, 10))
            else:
                domaines[(i, j)] = {grille[i][j]}

    return domaines

    def construire_voisins():
    voisins = {}

    for i in range(9):
        for j in range(9):
            case = (i, j)
            voisins[case] = set()

            for k in range(9):
                voisins[case].add((i, k))
                voisins[case].add((k, j))

            debut_i = (i // 3) * 3
            debut_j = (j // 3) * 3

            for x in range(debut_i, debut_i + 3):
                for y in range(debut_j, debut_j + 3):
                    voisins[case].add((x, y))

            voisins[case].discard(case)

    return voisins