import math
import sys
from fractions import Fraction

# 1.1
dividende = 3141
diviseur = 11
quotient = dividende // diviseur
reste = dividende % diviseur
print(quotient, reste)
print(quotient * diviseur + reste == dividende)


# 1.2
grand = 987654321
print(grand % 10)
print(grand // 10)


# 2.1
cumul = 0.0
for _ in range(2500):
    cumul = cumul + 0.1
print(cumul)
print(cumul - 250)


# 2.2
def presque_egaux(x, y, seuil=1e-9):
    return abs(x - y) <= seuil # Renvoie vrai / faux selon si ils sont quasi égaux au seuil près

print(0.7 + 0.1 == 0.8)
print(presque_egaux(0.7 + 0.1, 0.8))
print(presque_egaux(2.0, 2.25))


# 3.1
for i in range(1, 11):
    print(f"9 x {i} = {9 * i}")


# 3.2
borne = 250
total = 0
for i in range(1, borne + 1):
    total = total + i
print(total)
print(borne * (borne + 1) // 2)


# 4.1
def nombre_de_chiffres(n):
    compte = 1
    while n >= 10:
        n = n // 10
        compte = compte + 1
    return compte

print(nombre_de_chiffres(31415))
print(nombre_de_chiffres(9))
print(nombre_de_chiffres(0))
print(nombre_de_chiffres(10 ** 45))


# 5.1
def heron(a, tolerance=1e-12):
    if a < 0:
        raise ValueError("pas de racine reelle pour un nombre negatif")
    if a == 0:
        return 0.0
    estim = float(a)
    while True:
        suivante = 0.5 * (estim + a / estim)
        if abs(suivante - estim) <= tolerance * abs(suivante):
            return suivante
        estim = suivante

for valeur in (3, 10, 1e6):
    print(valeur, heron(valeur), math.sqrt(valeur), math.isclose(heron(valeur), math.sqrt(valeur), rel_tol=1e-12))


# 6.1
def vers_binaire(n):
    if n == 0:
        return "0"
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n = n // 2
    return bits

print(vers_binaire(100), vers_binaire(0), vers_binaire(2048))
print(all(vers_binaire(i) == bin(i)[2:] for i in range(3000)))


# 6.2
epsilon = 1.0
while 1.0 + epsilon / 2 != 1.0:
    epsilon = epsilon / 2
print(epsilon)
print(sys.float_info.epsilon)
print(epsilon == 2 ** -52)


# 7.1
def racines_naif(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine reelle")
    rd = math.sqrt(delta)
    return (-b - rd) / (2 * a), (-b + rd) / (2 * a)

petite_n, grande_n = racines_naif(1.0, -1e7, 1.0)
print(petite_n, grande_n)
print(petite_n * grande_n)


# 7.2
def racines(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine reelle")
    rd = math.sqrt(delta)
    if b >= 0:
        sure = (-b - rd) / (2 * a)
    else:
        sure = (-b + rd) / (2 * a)
    autre = c / (a * sure)
    return min(sure, autre), max(sure, autre)

petite_s, grande_s = racines(1.0, -1e7, 1.0)
print(petite_s, grande_s)
print(petite_s * grande_s)
for r in (petite_s, grande_s):
    residu = r * r - 1e7 * r + 1
    print(f"{residu:.1e}", f"{residu / max(r * r, 1.0):.1e}")


# 7.3
somme_exacte = Fraction(0)
for _ in range(2500):
    somme_exacte = somme_exacte + Fraction(1, 10)
print(somme_exacte, somme_exacte == 250)
print(Fraction(7, 10) + Fraction(1, 10) == Fraction(8, 10))

# boo