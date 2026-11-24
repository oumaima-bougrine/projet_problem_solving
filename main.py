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
