import random
import time
from fractions import Fraction
import numpy as np


# 1.1
def transposee(M):
    nb_lignes = len(M)
    nb_colonnes = len(M[0])
    return [[M[i][j] for i in range(nb_lignes)] for j in range(nb_colonnes)]

print(transposee([[1, 2], [3, 4], [5, 6]]))
print(transposee([[7, 8, 9, 10]]))


# 2.1
def produit(M, N):
    n, p = len(M), len(M[0])
    if len(N) != p:
        raise ValueError("dimensions incompatibles")
    q = len(N[0])
    res = [[0] * q for _ in range(n)]
    for i in range(n):
        for j in range(q):
            acc = 0
            for k in range(p):
                acc = acc + M[i][k] * N[k][j]
            res[i][j] = acc
    return res

unite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
exemple = [[2, -1, 4], [0, 3, 5], [1, 1, -2]]
print(produit(exemple, unite) == exemple)
print(produit([[0, 2], [5, 1]], [[3, 0], [1, 4]]))


# 2.2
random.seed(11)

def matrice_aleatoire(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

for taille in (30, 60, 90):
    X = matrice_aleatoire(taille)
    Y = matrice_aleatoire(taille)
    depart = time.perf_counter()
    produit(X, Y)
    print(f"n = {taille:>3} : {time.perf_counter() - depart:.4f} s")


# 3.1
taille = 90
X = matrice_aleatoire(taille)
Y = matrice_aleatoire(taille)

depart = time.perf_counter()
produit(X, Y)
temps_python = time.perf_counter() - depart

Xn, Yn = np.array(X), np.array(Y)
depart = time.perf_counter()
Xn @ Yn
temps_numpy = time.perf_counter() - depart

print(f"python pur {temps_python:.4f} s")
print(f"numpy      {temps_numpy:.6f} s")
print("rapport :", round(temps_python / max(temps_numpy, 1e-9)))


# 4.1
def resoudre(M, second, tolerance=1e-14):
    n = len(M)
    aug = [list(M[i]) + [second[i]] for i in range(n)]

    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(aug[i][k]))
        if abs(aug[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")
        aug[k], aug[meilleure] = aug[meilleure], aug[k]

        for i in range(k + 1, n):
            coeff = aug[i][k] / aug[k][k]
            for j in range(k, n + 1):
                aug[i][j] = aug[i][j] - coeff * aug[k][j]

    sol = [0.0] * n
    for i in range(n - 1, -1, -1):
        reste = aug[i][n]
        for j in range(i + 1, n):
            reste = reste - aug[i][j] * sol[j]
        sol[i] = reste / aug[i][i]
    return sol

S = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
second = [8, -11, -3]
solution = resoudre(S, second)
print([round(v, 10) for v in solution])
controle = [sum(S[i][j] * solution[j] for j in range(3)) for i in range(3)]
print([round(v, 10) for v in controle])


# 4.2
random.seed(3)
dim = 40
G = matrice_aleatoire(dim)
d = [random.random() for _ in range(dim)]
ma_solution = resoudre(G, d)
solution_numpy = np.linalg.solve(np.array(G), np.array(d))
ecart = max(abs(ma_solution[i] - solution_numpy[i]) for i in range(dim))
print("ecart maximal :", ecart)
print(ecart < 1e-9)


# Etape 5
def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

ordre = 10
Hn = hilbert(ordre)
x_reel = np.ones(ordre)
rhs = Hn @ x_reel

x_avec_solve = np.linalg.solve(Hn, rhs)
x_avec_inv = np.linalg.inv(Hn) @ rhs

print("erreur avec solve   :", float(np.max(np.abs(x_avec_solve - x_reel))))
print("erreur avec inv @ b :", float(np.max(np.abs(x_avec_inv - x_reel))))
print("conditionnement     : {:.3e}".format(float(np.linalg.cond(Hn))))

# 5.1
# solve donne une solution plus proche de la vraie que inv @ b, mais aucune des deux n'est exacte.
# Le conditionnement très élevé (de l'ordre de 1e13 ici) signifie que les erreurs d'arrondi sont fortement amplifiées :
# c'est le problème qui est mal posé, pas l'algorithme. On écrit donc solve(A, b), jamais inv(A) @ b.


# Etape 6
def rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])


# 6.1
gauche = rotation(np.pi / 3) @ rotation(np.pi / 4)
droite = rotation(7 * np.pi / 12)
print(np.allclose(gauche, droite))
print(np.round(droite, 10))


# 7.1
def determinant(M):
    n = len(M)
    copie = [list(ligne) for ligne in M]
    det = 1.0
    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(copie[i][k]))
        if abs(copie[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            copie[k], copie[meilleure] = copie[meilleure], copie[k]
            det = -det
        det = det * copie[k][k]
        for i in range(k + 1, n):
            coeff = copie[i][k] / copie[k][k]
            for j in range(k, n):
                copie[i][j] = copie[i][j] - coeff * copie[k][j]
    return det

T4 = [[3, 1, 0, 2], [1, 4, 1, 0], [0, 2, 5, 1], [2, 0, 1, 6]]
print(determinant(T4), float(np.linalg.det(np.array(T4, dtype=float))))
print(determinant([[1, 2, 3], [2, 4, 6], [1, 0, 1]]))


# 8.1
def hilbert_exacte(n):
    return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]

n_exact = 14
Hex = hilbert_exacte(n_exact)
second_exact = [sum(ligne) for ligne in Hex]

try:
    resoudre(Hex, second_exact)
except ValueError as erreur:
    print("premier essai :", erreur)

x_exacte = resoudre(Hex, second_exact, tolerance=0)
print(x_exacte)
print(all(v == 1 for v in x_exacte))


# 9.1
def translation(tx, ty):
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]])


def rotation_h(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0.0],
                     [s, c, 0.0],
                     [0.0, 0.0, 1.0]])

p = np.array([2.0, 1.0, 1.0])
Tr = translation(4, -2)
Ro = rotation_h(np.pi / 2)

print(np.round(Ro @ Tr @ p, 10))
print(np.round(Tr @ Ro @ p, 10))
