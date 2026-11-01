import math
import time
import matplotlib.pyplot as plt

# 1.1
def evaluer_naif(coeffs, x):
    somme = 0
    for rang in range(len(coeffs)):
        somme = somme + coeffs[rang] * x ** rang
    return somme

poly = [4, -1, 0, 2]
print(evaluer_naif(poly, 3))
print(evaluer_naif(poly, 0))

# 2.1
def evaluer(P, x):
    acc = 0
    for c in reversed(P):
        acc = acc * x + c
    return acc

for point in (-3, 0, 1, 3, 7):
    print(point, evaluer_naif(poly, point), evaluer(poly, point))


# 2.2
# Selon moi, Horner sera plus rapide de 50%
for degre in (1500, 6000, 24000):
    coeffs = [1] * (degre + 1)

    depart = time.perf_counter()
    valeur_naive = evaluer_naif(coeffs, 1.0001)
    temps_naif = time.perf_counter() - depart

    depart = time.perf_counter()
    valeur_horner = evaluer(coeffs, 1.0001)
    temps_horner = time.perf_counter() - depart

    print(f"degre {degre:>6} : naif {temps_naif:.5f} s | horner {temps_horner:.5f} s "
          f"| rapport {temps_naif / temps_horner:.1f} | ecart {abs(valeur_naive - valeur_horner):.2e}")


# 2.3
for degre in (150, 300, 600):
    coeffs = [1] * (degre + 1)

    depart = time.perf_counter()
    valeur_naive = evaluer_naif(coeffs, 2)
    temps_naif = time.perf_counter() - depart

    depart = time.perf_counter()
    valeur_horner = evaluer(coeffs, 2)
    temps_horner = time.perf_counter() - depart

    print(f"degre {degre:>4} : rapport {temps_naif / temps_horner:.1f} | egaux : {valeur_naive == valeur_horner}")


# 3.1
def deriver(coeffs):
    return [rang * coeffs[rang] for rang in range(1, len(coeffs))]

print(deriver([4, -1, 0, 2]))
print(deriver([9]))


# 4.1
def dichotomie(f, a, b, tolerance=1e-12):
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent etre de signes opposes")
    while b - a > tolerance:
        milieu = (a + b) / 2
        if f(a) * f(milieu) <= 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2


def carre_moins_trois(x):
    return x * x - 3

racine_d = dichotomie(carre_moins_trois, 0, 2)
print(racine_d)
print(abs(racine_d - math.sqrt(3)) < 1e-9)


# 4.2
def newton(coeffs, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(coeffs)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(coeffs, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("tangente horizontale")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError(f"pas de convergence en {tours_max} tours")

cubique = [-2, -1, 0, 1]
racine_n, tours_n = newton(cubique, 1)
print(racine_n, "en", tours_n, "tours")
print(abs(evaluer(cubique, racine_n)) < 1e-10)


# 4.3
def newton_trace(coeffs, depart, nb_tours):
    derivee = deriver(coeffs)
    x = float(depart)
    chemin = [x]
    for _ in range(nb_tours):
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x = x - evaluer(coeffs, x) / pente
        chemin.append(x)
    return chemin

cyclique = [0, -5, 0, 1]
print(newton_trace(cyclique, 1, 8))
try:
    print(newton(cyclique, 1))
except RuntimeError as erreur:
    print("echec :", erreur)


# 4.4
for depart in (1.5, 3, 0.5):
    racine_d, tours_d = newton(cubique, depart)
    print(f"depart {depart:>4} : {tours_d:>2} tours, racine {racine_d:.9f}")


# Etape 5
abscisses = [i / 100 for i in range(-300, 301)]
ordonnees = [evaluer(cubique, x) for x in abscisses]
plt.figure()
plt.plot(abscisses, ordonnees, label="x^3 - x - 2")
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)
plt.ylim(-15, 15)
plt.xlabel("x")
plt.ylabel("P(x)")
plt.legend()
plt.title("Racine reelle unique")
plt.show()

# 5.1
# La courbe ne coupe l'axe des abscisses qu'une fois, vers x = 1.52, racine trouvée par Newton.
# Le polynôme est de degré 3 : les deux autres racines sont complexes conjuguées, invisibles sur un tracé réel.


# 6.1
def somme(p, q):
    longueur = max(len(p), len(q))
    p = p + [0] * (longueur - len(p))
    q = q + [0] * (longueur - len(q))
    return [p[i] + q[i] for i in range(longueur)]


def produit_poly(p, q):
    if not p or not q:
        return []
    res = [0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            res[i + j] = res[i + j] + p[i] * q[j]
    return res

print(somme([3, 0, 1], [5, 2]))
print(produit_poly([2, 1], [2, 1]))
print(produit_poly([-2, 1], [2, 1]))


# 6.2
binome = [1]
for _ in range(8):
    binome = produit_poly(binome, [1, 1])
print(binome)
print(sum(binome), 2 ** 8)


# 7.1
def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h

def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

exacte = math.exp(0.5)
for h in (1e-1, 1e-2, 1e-3, 1e-5, 1e-7, 1e-9, 1e-11, 1e-13):
    err_avant = abs(derivee_avant(math.exp, 0.5, h) - exacte)
    err_centree = abs(derivee_centree(math.exp, 0.5, h) - exacte)
    print(f"h = {h:.0e} : avant {err_avant:.1e} | centree {err_centree:.1e}")


# 8.1
def rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))

def trapezes(f, a, b, n):
    h = (b - a) / n
    milieu = sum(f(a + i * h) for i in range(1, n))
    return h * ((f(a) + f(b)) / 2 + milieu)

def simpson(f, a, b, n):
    if n % 2 == 1:
        n = n + 1
    h = (b - a) / n
    impairs = sum(f(a + i * h) for i in range(1, n, 2))
    pairs = sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + f(b) + 4 * impairs + 2 * pairs)

def cube(x):
    return x ** 3

for n in (20, 200, 2000):
    e_rect = abs(rectangles(cube, 0, 2, n) - 4)
    e_trap = abs(trapezes(cube, 0, 2, n) - 4)
    e_simp = abs(simpson(cube, 0, 2, n) - 4)
    print(f"n = {n:>4} : rectangles {e_rect:.1e} | trapezes {e_trap:.1e} | simpson {e_simp:.1e}")


# 8.2
def integrande_pi(x):
    return 4 / (1 + x * x)

pi_trap = trapezes(integrande_pi, 0, 1, 2000)
pi_simp = simpson(integrande_pi, 0, 1, 2000)
print(pi_trap, abs(pi_trap - math.pi))
print(pi_simp, abs(pi_simp - math.pi))