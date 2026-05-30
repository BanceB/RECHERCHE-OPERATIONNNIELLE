"""
components/generateur_prix.py — Generateur de prix de ticket aleatoire.

Produit des prix compatibles avec les coupures SOTRA :
multiple de 50 FCFA, compris entre 200 FCFA et 20 000 FCFA.
Tous les multiples de 50 sont decomposables par les coupures disponibles
car 50 figure dans la liste [10000, 5000, 2000, 1000, 500, 200, 100, 50, ...].
"""

import random

# Bornes en nombre de multiples de 50 (200 / 50 = 4, 20000 / 50 = 400)
_BORNE_MIN = 4    # correspond a 200 FCFA
_BORNE_MAX = 400  # correspond a 20 000 FCFA


def generer_prix() -> int:
    """
    Genere un prix de ticket aleatoire.

    Retourne un entier multiple de 50, compris entre 200 et 20 000 FCFA inclus,
    garanti decomposable avec les coupures SOTRA standard.
    """
    return random.randint(_BORNE_MIN, _BORNE_MAX) * 50
