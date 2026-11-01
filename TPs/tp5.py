import random
import unicodedata
from collections import Counter

# 1.1
def lettre_vers_nombre(lettre):
    return ord(lettre) - ord("A")


def nombre_vers_lettre(nombre):
    return chr(nombre % 26 + ord("A"))

print(lettre_vers_nombre("H"), nombre_vers_lettre(7))
print([nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "AGMRZ"])


# 1.2
def nettoyer(texte):
    decompose = unicodedata.normalize("NFD", texte)
    decompose = "".join(c for c in decompose if unicodedata.category(c) != "Mn")
    return "".join(c for c in decompose.upper() if "A" <= c <= "Z")

print(nettoyer("Où êtes-vous, Zoé ?"))


# 2.1
def chiffrer(texte, a, b):
    sortie = []
    for c in nettoyer(texte):
        x = lettre_vers_nombre(c)
        sortie.append(nombre_vers_lettre((a * x + b) % 26))
    return "".join(sortie)

phrase = "RENDEZVOUSALAGARE"
print(chiffrer(phrase, 7, 3))
print(chiffrer(phrase, 1, 5))


# 3.1
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

admissibles = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(admissibles)
print(len(admissibles), "valeurs possibles pour a")


# 3.2
def inverse_modulaire(a, n):
    a = a % n
    for candidat in range(1, n):
        if (a * candidat) % n == 1:
            return candidat
    raise ValueError(f"{a} n'est pas inversible modulo {n}")

print(inverse_modulaire(7, 26))
print((7 * inverse_modulaire(7, 26)) % 26)

try:
    inverse_modulaire(6, 26)
except ValueError as erreur:
    print("erreur attendue :", erreur)


# 4.1
def dechiffrer(texte, a, b):
    a_inv = inverse_modulaire(a, 26)
    sortie = []
    for c in nettoyer(texte):
        y = lettre_vers_nombre(c)
        sortie.append(nombre_vers_lettre(a_inv * (y - b) % 26))
    return "".join(sortie)

original = nettoyer("Rendez-vous a la gare")
code = chiffrer(original, 7, 3)
print(code)
print(dechiffrer(code, 7, 3))
print(dechiffrer(code, 7, 3) == original)

try:
    dechiffrer(code, 6, 2)
except ValueError as erreur:
    print("cle refusee :", erreur)


# 5.1
def toutes_les_clefs(secret):
    sortie = []
    for a in admissibles:
        for b in range(26):
            sortie.append((a, b, dechiffrer(secret, a, b)))
    return sortie

tentatives = toutes_les_clefs(code)
print(len(tentatives), "clefs essayees")
trouvees = [t for t in tentatives if t[2] == original]
print("la bonne clef :", trouvees[0][0], trouvees[0][1])


# 6.1
texte_long = nettoyer(
    "Une fois que la cle est choisie, chaque lettre du message est transformee par la meme "
    "formule, ce qui signifie que la lettre la plus frequente du texte clair devient toujours "
    "la meme lettre dans le texte chiffre. Cette regularite est une porte ouverte pour "
    "quiconque sait compter : on releve les frequences, on les compare a celles de la langue "
    "francaise, et la cle apparait presque sans effort. Les chiffrements modernes ont ete "
    "concus pour que cette information ne survive jamais dans le message chiffre, de sorte "
    "que le simple decompte des lettres ne revele plus rien a celui qui espionne la ligne."
)
secret_long = chiffrer(texte_long, 11, 8)

frequences_fr = {
    "E": 14.7, "A": 7.6, "S": 7.9, "I": 7.5, "N": 7.1, "T": 7.2, "R": 6.6, "L": 5.5,
    "U": 6.3, "O": 5.3, "D": 3.7, "C": 3.3, "M": 3.0, "P": 3.0, "V": 1.6, "Q": 1.4,
    "G": 1.1, "F": 1.1, "B": 0.9, "H": 0.7, "J": 0.5, "X": 0.4, "Y": 0.3, "Z": 0.1,
    "K": 0.05, "W": 0.04,
}

def score_francais(texte):
    return sum(frequences_fr[c] for c in texte) / len(texte)

def casser_par_frequences(secret):
    comptes = Counter(secret)
    plus_frequente = comptes.most_common(1)[0][0]
    cible = lettre_vers_nombre(plus_frequente)
    candidats = []
    for a in admissibles:
        b = (cible - 4 * a) % 26
        clair = dechiffrer(secret, a, b)
        candidats.append((score_francais(clair), a, b, clair))
    candidats.sort(reverse=True)
    return plus_frequente, candidats

lettre_top, candidats = casser_par_frequences(secret_long)
print("lettre la plus frequente du chiffre :", lettre_top)
print(len(candidats), "candidats au lieu de 312")
meilleur = candidats[0]
print("trouve :", meilleur[1], meilleur[2])
print(meilleur[3][:60])
print(meilleur[3] == texte_long)

secret_court = chiffrer("MATINALARRIVEE", 11, 8)
lettre_c, candidats_c = casser_par_frequences(secret_court)
print(lettre_c, candidats_c[0][3])
# L'attaque échoue sur un texte court : avec trop peu de lettres, la lettre la plus fréquente du chiffré n'est pas forcément l'image de E.


# 7.1
def indice_coincidence(texte):
    N = len(texte)
    occurrences = Counter(texte)
    return sum(n * (n - 1) for n in occurrences.values()) / (N * (N - 1))

random.seed(5)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bruit = "".join(random.choice(alphabet) for _ in range(len(texte_long)))

print(f"clair  : {indice_coincidence(texte_long):.4f}")
print(f"affine : {indice_coincidence(secret_long):.4f}")
print(f"hasard : {indice_coincidence(bruit):.4f}")


# 8.1
def vigenere(texte, cle):
    sortie = []
    for i, c in enumerate(nettoyer(texte)):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        sortie.append(nombre_vers_lettre(lettre_vers_nombre(c) + decalage))
    return "".join(sortie)

secret_vig = vigenere(texte_long, "NUIT")
print(secret_vig[:40])
print(f"IC vigenere : {indice_coincidence(secret_vig):.4f}")


# 8.2
for longueur in range(1, 10):
    tranches = [secret_vig[i::longueur] for i in range(longueur)]
    moyenne = sum(indice_coincidence(t) for t in tranches) / longueur
    print(f"L = {longueur} : indice moyen {moyenne:.4f}")
