# Résolution du Sudoku par satisfaction de contraintes

Projet Problem Solving — Groupe 5

Technique : backtracking avec propagation AC-3 et heuristique MRV.  
Implémentation : `main.py` .

Lancer les cinq cas de test :

```bash
python main.py
```

## 1. Formulation du problème

Le Sudoku est une grille de 9 lignes et 9 colonnes, partagée en neuf blocs de 3×3. Certaines cases contiennent déjà un chiffre de 1 à 9 ; les autres sont vides, notées 0. Il faut remplir toutes les cases vides en respectant trois règles, sans jamais modifier un chiffre initial : chaque ligne, chaque colonne et chaque bloc 3×3 contient les chiffres de 1 à 9, chacun une seule fois.

Le problème est un CSP, noté (X, D, C).

**Variables.** Chaque case est une variable Xᵢⱼ, avec i le numéro de ligne et j le numéro de colonne. La grille compte donc 81 variables.

**Domaines.** D(Xᵢⱼ) = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Si la grille initiale contient déjà la valeur v dans la case (i, j), le domaine est réduit à {v}.

**Contraintes.** Ce sont des contraintes binaires de différence :

- ligne : AllDiff(Xᵢⱼ, Xᵢₖ) dès que j ≠ k ;
- colonne : AllDiff(Xᵢⱼ, Xₖⱼ) dès que i ≠ k ;
- bloc : AllDiff(Xᵢⱼ, Xₖₗ) lorsque (i, j) et (k, l) sont deux cases distinctes du même bloc 3×3.

## 2. Formulation comme recherche

Le CSP est exploré comme un problème de recherche.

- **État initial.** Aucune case vide n’est encore affectée. Les cases déjà remplies restent fixées par un domaine singleton.
- **État.** Affectation partielle : certaines variables ont une valeur, les autres restent libres.
- **Fonction successeur.** Choisir une variable non affectée et lui attribuer une valeur encore présente dans son domaine, compatible avec les contraintes du CSP.
- **État but.** Affectation des 81 variables, complète et cohérente tout en respectant les contraintes du CSP.

La recherche commence à partir de l’état initial et construit progressivement une solution en 
affectant une valeur à une case vide à chaque étape. 

## 3. Algorithme

Le programme construit d’abord le graphe de voisinage : pour chaque case, les voisins sont les autres cases de sa ligne, de sa colonne et de son bloc. Toute contrainte de différence est un arc de ce graphe.

**Propagation AC-3.** À chaque nœud de recherche, AC-3 applique la cohérence d'arc afin de réduire les domaines et de détecter les contradictions. Pour un arc (Xᵢ, Xⱼ), une valeur v est retirée de D(Xᵢ) s’il n’existe aucune valeur de D(Xⱼ) différente de v. Si un domaine devient vide, la branche est un échec. Sinon, les arcs qui arrivent sur Xᵢ sont replacés dans la file, car leur support a pu disparaître. Exemple : si X₁,₁ est fixé à 5, alors 5 est retiré de D(X₁,₂).

**Choix de la variable (MRV).** Parmi les cases dont le domaine contient encore au moins deux valeurs, l’algorithme choisit celle dont le domaine est le plus petit. Une case déjà remplie a un domaine de taille 1 : elle n’est jamais choisie, donc jamais modifiée.

**Backtracking.**

1. Appliquer AC-3. Si un domaine est vide, retourner l’échec.
2. Si tous les domaines sont des singletons, retourner le succès.
3. Choisir une case par MRV.
4. Pour chaque valeur restante : sauvegarder les domaines, fixer la case à cette valeur, appeler le backtracking. En cas d’échec, restaurer les domaines et essayer la valeur suivante.
5. Si aucune valeur ne convient, retourner l’échec.

**Arrêt.** L’algorithme s’arrête dès qu’une affectation complète et cohérente est obtenue, ou lorsque toutes les branches ont échoué. Un **état exploré** est un appel récursif. Ce nombre mesure la taille de l’arbre réellement parcouru. Le travail de propagation est inclus dans le nœud, et n’augmente pas ce compteur.

## 4. Explication du code

Le programme utilise Python pour résoudre des grilles de Sudoku en combinant trois algorithmes : AC-3, MRV et Backtracking.

### 4.1. Initialisation et contraintes

- `initialiser_domaines(grille)` : attribue à chaque case les valeurs possibles de 1 à 9. Les cases déjà remplies conservent uniquement leur valeur.
- `construire_voisins()` : identifie les cases situées sur la même ligne, la même colonne et dans le même bloc 3×3.
- `revise(domaines, xi, xj)` : supprime les valeurs incompatibles entre deux cases voisines.

### 4.2. Algorithmes de résolution

- `AC3(domaines, voisins)` : réduit les domaines en appliquant les contraintes. Si un domaine devient vide, une contradiction est détectée.
- `sudoku_resolu(domaines)` : vérifie si toutes les cases possèdent une seule valeur possible.
- `choisir_case(domaines)` : applique MRV pour sélectionner la case ayant le plus petit domaine avec plusieurs valeurs possibles.
- `backtracking()` : essaie les valeurs possibles, applique AC-3 et revient en arrière lorsqu'une tentative échoue. Il répète ce processus jusqu'à trouver une solution ou constater qu'aucune solution n'existe.

### 4.3. Vérification et tests

- `verifier_chiffres_initiaux()` : vérifie que les chiffres présents au départ sont conservés après la résolution.
- `grilles_tests` : contient cinq Sudoku de différents niveaux, dont un Sudoku impossible.
- La boucle finale exécute les cinq tests et affiche les résultats, le temps d'exécution et le nombre d'états explorés.

Le temps est mesuré avec `time.perf_counter()` et le compteur `etats_explores` permet de suivre le nombre d'appels récursifs à Backtracking.

## 5. Tests

Cinq grilles fixes ont été utilisées pour tester différentes situations : une grille déjà résolue, deux grilles incomplètes de difficulté différente, une grille très incomplète et une grille contradictoire.

Pour chaque test, le programme affiche la grille initiale, applique AC-3, puis utilise MRV et le backtracking si la propagation ne suffit pas. Lorsqu'une solution est trouvée, le programme vérifie que les chiffres initiaux sont conservés.

**T1 — Grille déjà résolue.**

La grille contient déjà les 81 chiffres. Tous les domaines sont des singletons. AC-3 réussit sans modification et MRV ne sélectionne aucune case (`None`). Le programme confirme que la grille est résolue en un seul état exploré. Les chiffres initiaux sont conservés.

**T2 — Grille facile.**

Cette grille contient plusieurs cases vides. Au départ, chaque case vide possède un domaine de neuf valeurs possibles. Après AC-3, tous les domaines deviennent des singletons. La propagation suffit donc à résoudre entièrement le Sudoku, sans branchement du backtracking. Le programme retrouve la solution et explore un seul état.

**T3 — Grille de difficulté intermédiaire.**

Cette troisième grille contient également plusieurs cases vides. AC-3 parvient à déterminer toutes les valeurs sans avoir besoin de recherche. Tous les domaines deviennent des singletons et MRV ne sélectionne aucune case. Le Sudoku est résolu avec succès en un seul état exploré.

**T4 — Grille très incomplète.**

Cette grille contient très peu d'indices. AC-3 réduit les domaines, mais ne parvient pas à déterminer toutes les cases.
MRV sélectionne notamment la case (0, 3), dont le domaine contient cinq valeurs possibles : 3, 4, 6, 7 et 8. Le backtracking essaie ensuite les différentes possibilités et relance AC-3 après chaque choix. Le programme trouve finalement une solution après 43 états explorés, en environ 0,073358 seconde.

**T5 — Grille contradictoire.**

Cette grille reprend la grille facile, mais les deux premières cases de la première ligne contiennent toutes les deux le chiffre 5. AC-3 détecte cette contradiction dès la propagation initiale et renvoie `False`. Le programme ne trouve aucune solution et s'arrête après un seul état exploré.

## 6. Évaluation des performances

Les mesures suivantes proviennent de l'exécution du programme :

| Test | Situation | Résultat | États explorés | Temps du backtracking |
|---|---|---|---:|---:|
| T1 | Grille déjà résolue | Succès | 1 | 0,000651 s |
| T2 | Grille facile | Succès | 1 | 0,000697 s |
| T3 | Grille intermédiaire | Succès | 1 | 0,000697 s |
| T4 | Grille très incomplète | Succès | 43 | 0,073358 s |
| T5 | Grille contradictoire | Échec détecté | 1 | 0,000103 s |

Les résultats montrent que T1, T2 et T3 sont entièrement résolus grâce à AC-3. Dans ces trois cas, aucun branchement n'est nécessaire et le compteur reste à un seul état exploré.

T4 démontre l'utilité de combiner AC-3, MRV et backtracking. La propagation seule ne suffit pas à résoudre la grille. MRV permet de choisir une case parmi les plus contraintes, tandis que le backtracking explore les possibilités restantes. AC-3 détecte les contradictions et permet d'abandonner les branches impossibles. La solution est obtenue après 43 états explorés.

Enfin, T5 montre que l'algorithme peut détecter rapidement une contradiction présente dès le départ, sans explorer de nombreuses possibilités.

Le nombre d'états explorés correspond au nombre d'appels récursifs à la fonction `backtracking`. Il ne représente donc pas le nombre total de valeurs testées. Les temps d'exécution et le nombre d'états mesurent deux aspects différents du travail effectué par le programme.

Les temps indiqués correspondent à une seule exécution de chaque test et peuvent varier légèrement selon la machine et les conditions d'exécution.

## 7. Pourquoi la solution respecte les contraintes

Le programme considère un Sudoku comme résolu lorsque les 81 domaines contiennent chacun une seule valeur et qu'AC-3 n'a détecté aucune contradiction.

**Conservation des indices initiaux.** Chaque chiffre déjà présent dans la grille reçoit un domaine contenant uniquement sa valeur initiale. La fonction MRV sélectionne uniquement les cases dont le domaine contient plusieurs valeurs possibles. Ainsi, les chiffres initiaux ne sont jamais modifiés. La fonction `verifier_chiffres_initiaux` permet de vérifier que tous les chiffres de départ sont conservés dans les quatre grilles résolues.

**Respect des lignes, colonnes et blocs.** Chaque case est reliée aux autres cases de sa ligne, de sa colonne et de son bloc de 3×3. AC-3 supprime les valeurs qui ne possèdent pas de support dans les domaines des cases voisines. À la fin, chaque domaine contient une seule valeur. Deux cases voisines ne peuvent pas conserver la même valeur dans leurs domaines singleton : une telle affectation serait incompatible avec la contrainte de différence et serait détectée par AC-3.

**Détection des contradictions.** Dans T5, les deux premières cases de la première ligne contiennent toutes les deux le chiffre 5. Comme elles sont voisines, elles ne peuvent pas conserver simultanément cette valeur. AC-3 détecte cette situation et renvoie `False`, ce qui empêche le programme de produire une fausse solution.

**Vérification finale.** Les grilles obtenues pour T1, T2, T3 et T4 conservent leurs indices initiaux. Le respect des contraintes est assuré par AC-3 et le backtracking pendant la résolution. La fonction `verifier_chiffres_initiaux` confirme que les chiffres de départ sont conservés.

Ces tests montrent que l'association d'AC-3, de MRV et du backtracking permet de résoudre différentes grilles, de limiter les recherches inutiles et de détecter les situations impossibles.
