import math
import random
import matplotlib.pyplot as plt

# 1.1
def vecteur(A, B):
    return (B[0] - A[0], B[1] - A[1])

def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme(u):
    return math.hypot(u[0], u[1])

def angle(u, v):
    cosinus = produit_scalaire(u, v) / (norme(u) * norme(v))
    cosinus = max(-1.0, min(1.0, cosinus))
    return math.degrees(math.acos(cosinus))

print(norme((5, 12)), produit_scalaire((2, -1), (4, 3)))
print(angle((1, 0), (-1, 1)), angle((0, 2), (3, 0)))
print(angle((3, 3), (1, 1)))


# 1.2
def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]

def distance_point_droite(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    return abs(determinant(AB, AP)) / norme(AB)

print(distance_point_droite((0, 0), (0, 2), (2, 0)), math.sqrt(2))
print(distance_point_droite((5, 7), (0, 0), (1, 0)))


# 2.1
def orientation(A, B, C):
    d = determinant(vecteur(A, B), vecteur(A, C))
    if d > 0:
        return 1
    if d < 0:
        return -1
    return 0

print(orientation((0, 0), (2, 0), (2, 3)))
print(orientation((0, 0), (2, 0), (2, -3)))
print(orientation((1, 1), (2, 2), (5, 5)))


# 2.2
def aire(sommets):
    total = 0
    n = len(sommets)
    for i in range(n):
        x1, y1 = sommets[i]
        x2, y2 = sommets[(i + 1) % n]
        total = total + (x1 * y2 - x2 * y1)
    return abs(total) / 2

rectangle = [(0, 0), (3, 0), (3, 2), (0, 2)]
triangle = [(0, 0), (5, 0), (0, 2)]
fusee = [(0, 0), (3, 0), (3, 2), (1.5, 4), (0, 2)]
print(aire(rectangle), aire(triangle), aire(fusee))
print(aire(fusee[::-1]))


# 3.1
def se_coupent(A, B, C, D):
    #Vrai si les segments [AB] et [CD] se croisent franchement.
    #Si trois des quatre points sont alignés, le cas est dégénéré et la fonction renvoie False.
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0

print(se_coupent((0, 0), (4, 4), (0, 4), (4, 0)))
print(se_coupent((0, 0), (3, 0), (0, 2), (3, 2)))
print(se_coupent((1, 1), (2, 2), (4, 4), (5, 5)))


# 3.2
def intersection(A, B, C, D):
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    denom = determinant(AB, CD)
    if denom == 0:
        return None
    AC = vecteur(A, C)
    t = determinant(AC, CD) / denom
    u = determinant(AC, AB) / denom
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (A[0] + t * AB[0], A[1] + t * AB[1])
    return None

print(intersection((0, 0), (4, 4), (0, 4), (4, 0)))
print(intersection((0, 0), (3, 0), (0, 2), (3, 2)))
print(intersection((0, 0), (2, 1), (1, -1), (1, 3)))


# 4.1
def dedans(P, sommets):
    x, y = P
    n = len(sommets)
    a_l_interieur = False
    for i in range(n):
        x1, y1 = sommets[i]
        x2, y2 = sommets[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_coupe = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_coupe:
                a_l_interieur = not a_l_interieur
    return a_l_interieur

for pt in ((1.5, 1), (1.5, 3.5), (3.5, 1), (0.2, 2.5)):
    print(pt, dedans(pt, fusee))


# 4.2
random.seed(21)
nb_tirages = 100_000
succes = 0
for _ in range(nb_tirages):
    pt = (random.uniform(0, 3), random.uniform(0, 4))
    if dedans(pt, fusee):
        succes = succes + 1
print(12 * succes / nb_tirages)

# Etape 5
def tracer_polygone(sommets, points=()):
    xs = [s[0] for s in sommets] + [sommets[0][0]]
    ys = [s[1] for s in sommets] + [sommets[0][1]]
    plt.figure(figsize=(5, 5))
    plt.plot(xs, ys, color="navy")
    for pt in points:
        couleur = "green" if dedans(pt, sommets) else "red"
        plt.scatter([pt[0]], [pt[1]], color=couleur)
    plt.axis("equal")
    plt.title("Vert : dedans, rouge : dehors")
    plt.show()

forme_l = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 3), (0, 3)]
print(aire(forme_l))
print(dedans((0.5, 2), forme_l), dedans((2, 2), forme_l), dedans((3, 0.5), forme_l))
tracer_polygone(forme_l, [(0.5, 2), (2, 2), (3, 0.5), (0.5, 0.5), (3.5, 1.5)])


# 6.1
def zone_de(P, zones):
    for indice, zone in enumerate(zones):
        if dedans(P, zone):
            return indice
    return None

cartes = [fusee, [(5, 0), (7, 0), (7, 2), (5, 2)]]
for pt in ((1.5, 1), (6, 1), (4, 1)):
    print(pt, zone_de(pt, cartes))