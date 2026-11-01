# Projet Python : Jeu RPG ("RPG Engine")
# Auteur : Daris KOKIC
# Cours : R1.07 - Outils mathématiques fondamentaux (IUT Nord Franche-Comté)
# -------------------------------------------------------------
# Mon script intègre à peu près toutes les notions abordées du TP1 au TP6 :
# 1. Calcul numérique, flottants et gestion d'erreurs (TP1)
# 2. Arithmétique et tests de primalité pour les bonus de niveaux (TP2)
# 3. Polynômes, méthode Horner et recherche de racines par dichotomie (TP3)
# 4. Matrices, produits scalaires et résolution de systèmes linéaires (TP4)
# 5. Synthèse, robustesse et traitement de listes/fichiers (TP5)
# 6. Géométrie du plan, vecteurs, aires et hitbox / polygones (TP6)

# ! Certaines parties du code ont dû utiliser l'assistance de l'IA,
# elles ont cependant été lues, relues et comprises de manière générale !

import math
import time
import numpy as np


# Partie 1 : Calcul numérique, flottants & robustesse (avec TP1 et TP5)

# La fonction permet de calculer des dégâts avec précision en gérant des flottants
def simuler_degats_critiques(degats_base, taux_critique, multiplicateur):
    if not (0.0 <= taux_critique <= 1.0):
        raise ValueError("Le taux critique doit être compris entre 0 et 1.")

    degats_finaux = degats_base * multiplicateur if taux_critique > 0.5 else degats_base
    return round(float(degats_finaux), 2)


# Partie 2 : Arithmétique et niveaux (TP2)

# Cette fonction vérifie si un numéro de niveau est un nombre premier (offrant un bonus spécial)
def est_niveau_special(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# Partie 3 : Polynômes, Horner et Dichotomie (TP3)

# La fonction suivant réutilise les polynome et évalue un polynôme de progression de dégâts P avec la méthode Horner
def evaluer_degats_croissance(P, niveau):
    resultat = 0.0
    for coeff in reversed(P):
        resultat = resultat * niveau + coeff
    return resultat

# Cette fonction trouve le niveau exact (racine de f(niveau) - cible = 0) par dichotomie.
def trouver_seuil_niveau(f_degats, cible_degats, a=1, b=100, eps=1e-5):
    def f_aux(x):
        return f_degats(x) - cible_degats

    if f_aux(a) * f_aux(b) > 0:
        return None  # Pas de changement de signe sur l'intervalle

    for _ in range(1000):
        m = (a + b) / 2.0
        if abs(f_aux(m)) < eps or (b - a) / 2.0 < eps:
            return m
        if f_aux(a) * f_aux(m) < 0:
            b = m
        else:
            a = m
    return (a + b) / 2.0


# Partie 4 : Matrices et systèmes d'équipement (TP4)

# La fonction ci-dessous fait un produit matriciel pour pouvoir évaluer la puissance globale d'un groupe d'ennemis
def calculer_statistiques_equipe(matrice_stats, vecteur_poids):
    A = np.array(matrice_stats, dtype=float)
    poids = np.array(vecteur_poids, dtype=float)

    # Produit matriciel ou dot product
    score_global = np.dot(A, poids)
    return score_global


# L'endroit ou la magie démarre

if __name__ == "__main__":
    print("----------------------------------------------------")
    print("RPG ENGINE : UN SIMULATEUR RPG MATHÉMATIQUE (R1.07) ")
    print("                 par Daris KOKIC                    ")
    print("----------------------------------------------------")

    # 1. Test TP1 & TP5 (Flottants et calculs)
    debut_chrono = time.time()
    degats = simuler_degats_critiques(150.75, 0.8, 2.5)
    print(f"[TP1/TP5] Dégâts critiques calculés : {degats}")

    # 2. Test TP2 (Arithmétique - Nombres premiers)
    niveau_perso = 17
    if est_niveau_special(niveau_perso):
        print(f"[TP2] Le niveau {niveau_perso} est premier ! Bonus de mana activé.")
    else:
        print(f"[TP2] Le niveau {niveau_perso} n'est pas premier.")

    # 3. Test TP3 (Polynômes et Dichotomie)
    polynome_degats = [10, 5, 2]
    niveau_actuel = 4
    degats_evalues = evaluer_degats_croissance(polynome_degats, niveau_actuel)
    print(f"[TP3] Dégâts au niveau {niveau_actuel} (via Horner) : {degats_evalues}")

    # Recherche du niveau exact pour atteindre 250 de dégâts


    def fonction_progression(x):
        return evaluer_degats_croissance(polynome_degats, x)


    niveau_cible = trouver_seuil_niveau(fonction_progression, 250.0, 1, 20)
    if niveau_cible:
        print(f"[TP3] Pour atteindre 250 dégâts, il faut le niveau : {niveau_cible:.4f}")

    # 4. Test TP4 (Matrices & NumPy)
    # Statistiques de 3 joueurs (Attaque, Défense, Agilité)
    stats_joueurs = [
        [85.0, 40.0, 60.0],
        [90.0, 55.0, 50.0],
        [75.0, 30.0, 80.0]
    ]
    poids_meta = [0.5, 0.3, 0.2]  # Importance relative des stats
    scores_puissance = calculer_statistiques_equipe(stats_joueurs, poids_meta)
    print(f"[TP4] Scores de puissance globale des joueurs (NumPy) : {scores_puissance}")
# boo