import time

# La fonction durée qui se trouve juste avant l'exo 3.1
def duree(fonction, argument):
    debut = time.perf_counter()
    fonction(argument)
    return time.perf_counter() - debut


# 1.1
def diviseurs(n):
    liste = []
    for candidat in range(1, n + 1):
        if n % candidat == 0:
            liste.append(candidat)
    return liste

print(diviseurs(60))
print(diviseurs(101))


# 2.1
def pgcd_naif(a, b):
    meilleur = 1
    for candidat in range(1, min(a, b) + 1):
        if a % candidat == 0 and b % candidat == 0:
            meilleur = candidat
    return meilleur

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print(pgcd_naif(1260, 198), pgcd(1260, 198))
print(pgcd_naif(391, 289), pgcd(391, 289))


# Fonctions d'étape 3
def est_premier_naif(n):
    if n < 2:
        return False
    for candidat in range(2, n):
        if n % candidat == 0:
            return False
    return True

def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    candidat = 3
    while candidat * candidat <= n:
        if n % candidat == 0:
            return False
        candidat = candidat + 2
    return True


# 3.1
for p in (10_009, 100_019, 1_000_033):
    t_naif = duree(est_premier_naif, p)
    t_racine = duree(est_premier, p)
    print(f"{p:>9} : naif {t_naif:.5f} s | racine {t_racine:.6f} s")


# Fonction de l'étape 4
def crible(limite):
    marques = [True] * (limite + 1)
    marques[0] = False
    if limite >= 1:
        marques[1] = False
    d = 2
    while d * d <= limite:
        if marques[d]:
            for multiple in range(d * d, limite + 1, d):
                marques[multiple] = False
        d = d + 1
    return [k for k in range(limite + 1) if marques[k]]


# 4.1
debut = time.perf_counter()
premiers = crible(50_000)
t_crible = time.perf_counter() - debut

debut = time.perf_counter()
denombrement = sum(1 for k in range(50_001) if est_premier(k))
t_un_par_un = time.perf_counter() - debut

print(len(premiers), denombrement)
print(f"crible {t_crible:.4f} s | un par un {t_un_par_un:.4f} s")


# 5.1
def facteurs(n):
    decomposition = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            decomposition.append(d)
            n = n // d
        d = d + 1
    if n > 1:
        decomposition.append(n)
    return decomposition

liste_facteurs = facteurs(504)
print(liste_facteurs)
produit = 1
for f in liste_facteurs:
    produit = produit * f
print(produit)


# Fonction de l'étape 6
def fibonacci_recursif(n):
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)

# 6.1
for rang in (18, 22, 26):
    print(f"F({rang}) : {duree(fibonacci_recursif, rang):.4f} s")

nombre_appels = {}


# 6.2
def fibonacci_compte(n):
    nombre_appels[n] = nombre_appels.get(n, 0) + 1
    if n < 2:
        return n
    return fibonacci_compte(n - 1) + fibonacci_compte(n - 2)

valeur = fibonacci_compte(24)
print("F(24) =", valeur)
print("appels a F(1) :", nombre_appels[1])
print("appels en tout :", sum(nombre_appels.values()))


# 6.3
def fibonacci(n):
    avant, courant = 0, 1
    for _ in range(n):
        avant, courant = courant, avant + courant
    return avant

print(all(fibonacci(k) == fibonacci_recursif(k) for k in range(22)))
print(f"F(26) en {duree(fibonacci, 26):.6f} s")
enorme = fibonacci(5000)
print(len(str(enorme)), "chiffres")


# 7.1
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v

g, u, v = euclide_etendu(240, 46)
print(g, u, v, 240 * u + 46 * v == g)
g2, u2, v2 = euclide_etendu(7, 40)
print(g2, u2, u2 % 40, (7 * (u2 % 40)) % 40)


# 7.2
def puissance_mod_naive(base, exposant, modulo):
    resultat = 1
    for _ in range(exposant):
        resultat = resultat * base % modulo
    return resultat

def puissance_mod(base, exposant, modulo):
    resultat = 1
    base = base % modulo
    while exposant > 0:
        if exposant % 2 == 1:
            resultat = resultat * base % modulo
        base = base * base % modulo
        exposant = exposant // 2
    return resultat

b, e, m = 3, 3_000_000, 1_000_033
print(puissance_mod(b, e, m), pow(b, e, m))

debut = time.perf_counter()
puissance_mod_naive(b, e, m)
t_naive = time.perf_counter() - debut
debut = time.perf_counter()
puissance_mod(b, e, m)
t_rapide = time.perf_counter() - debut
print(f"naive {t_naive:.3f} s | rapide {t_rapide:.6f} s")
